"""
Persistência do OCEO.

O núcleo nunca fala com banco direto: ele fala com um Repositorio. Trocar
SQLite por Postgres é escrever outra classe que cumpra o mesmo contrato,
sem encostar em nenhuma regra de negócio.

SQLite vem na stdlib do Python, então o sistema continua rodando em qualquer
máquina sem instalar nada — inclusive em teste, com banco em memória.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from .dominio import Alerta, Empresa, Evento, Fato, Pilar, Regime
from .trilha import GENESE, Conferencia, conferir, resumir

ESQUEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS empresas (
    id           TEXT PRIMARY KEY,
    cnpj         TEXT NOT NULL UNIQUE,
    razao_social TEXT NOT NULL,
    regime       TEXT NOT NULL,
    municipio    TEXT DEFAULT '',
    uf           TEXT DEFAULT '',
    abertura     TEXT
);

CREATE TABLE IF NOT EXISTS assinaturas (
    empresa_id TEXT NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    pilar      TEXT NOT NULL,
    PRIMARY KEY (empresa_id, pilar)
);

CREATE TABLE IF NOT EXISTS fatos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    evento     TEXT NOT NULL,
    empresa_id TEXT NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    origem     TEXT NOT NULL,
    dados      TEXT NOT NULL DEFAULT '{}',
    em         TEXT NOT NULL,
    -- corrente de integridade: ver oceo/trilha.py
    hash           TEXT NOT NULL DEFAULT '',
    hash_anterior  TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_fatos_empresa ON fatos(empresa_id, em);

CREATE TABLE IF NOT EXISTS alertas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id    TEXT NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    pilar         TEXT NOT NULL,
    titulo        TEXT NOT NULL,
    detalhe       TEXT NOT NULL,
    severidade    TEXT NOT NULL DEFAULT 'informativo',
    origem_evento TEXT,
    em            TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_alertas_empresa ON alertas(empresa_id, em);

CREATE TABLE IF NOT EXISTS usuarios (
    id         TEXT PRIMARY KEY,
    email      TEXT NOT NULL UNIQUE,
    nome       TEXT NOT NULL,
    senha_hash TEXT NOT NULL,
    salt       TEXT NOT NULL,
    ativo      INTEGER NOT NULL DEFAULT 1,
    criado_em  TEXT NOT NULL
);

-- Quem pode ver qual empresa. É o isolamento multiusuário.
CREATE TABLE IF NOT EXISTS acessos (
    usuario_id TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    empresa_id TEXT NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    papel      TEXT NOT NULL DEFAULT 'operador',   -- dono | operador | leitor
    PRIMARY KEY (usuario_id, empresa_id)
);

CREATE TABLE IF NOT EXISTS sessoes (
    token      TEXT PRIMARY KEY,
    usuario_id TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    criada_em  TEXT NOT NULL,
    expira_em  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sessoes_usuario ON sessoes(usuario_id);

-- Tentativas de login que falharam. Serve para travar força bruta.
-- Guarda só a chave e a hora: nenhuma senha tentada é registrada, nem o
-- registro serviria de pista para quem roubasse o banco.
CREATE TABLE IF NOT EXISTS tentativas (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    chave TEXT NOT NULL,          -- 'conta:<email>' ou 'origem:<ip>'
    em    TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tentativas ON tentativas(chave, em);

-- Pedidos de redefinição de senha.
-- O token NUNCA é guardado em claro: guarda-se o resumo dele. Quem roubar
-- o banco não consegue redefinir a senha de ninguem.
CREATE TABLE IF NOT EXISTS recuperacoes (
    token_hash TEXT PRIMARY KEY,
    usuario_id TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    criada_em  TEXT NOT NULL,
    expira_em  TEXT NOT NULL,
    usada_em   TEXT
);
CREATE INDEX IF NOT EXISTS idx_recuperacoes_usuario ON recuperacoes(usuario_id);
"""


class RepositorioSQLite:
    """Guarda o estado do OCEO. `caminho=":memory:"` dá um banco descartável."""

    def __init__(self, caminho: str | Path = ":memory:"):
        self.caminho = str(caminho)
        if self.caminho != ":memory:":
            Path(self.caminho).parent.mkdir(parents=True, exist_ok=True)
        self.con = sqlite3.connect(self.caminho, check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.con.executescript(ESQUEMA)
        self.con.commit()

    def fechar(self) -> None:
        self.con.close()

    # ------------------------------------------------------------ empresas
    def salvar_empresa(self, e: Empresa) -> None:
        self.con.execute(
            "INSERT INTO empresas (id,cnpj,razao_social,regime,municipio,uf,abertura) "
            "VALUES (?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET "
            "razao_social=excluded.razao_social, regime=excluded.regime, "
            "municipio=excluded.municipio, uf=excluded.uf, abertura=excluded.abertura",
            (e.id, e.cnpj, e.razao_social, e.regime.value, e.municipio, e.uf,
             e.abertura.isoformat() if e.abertura else None),
        )
        self.con.commit()

    def carregar_empresa(self, empresa_id: str) -> Empresa | None:
        r = self.con.execute("SELECT * FROM empresas WHERE id=?", (empresa_id,)).fetchone()
        return _para_empresa(r) if r else None

    def listar_empresas(self) -> list[Empresa]:
        return [_para_empresa(r) for r in
                self.con.execute("SELECT * FROM empresas ORDER BY razao_social")]

    # --------------------------------------------------------- assinaturas
    def salvar_assinatura(self, empresa_id: str, pilares: Iterable[Pilar]) -> None:
        self.con.execute("DELETE FROM assinaturas WHERE empresa_id=?", (empresa_id,))
        self.con.executemany(
            "INSERT INTO assinaturas (empresa_id,pilar) VALUES (?,?)",
            [(empresa_id, p.value) for p in pilares],
        )
        self.con.commit()

    def carregar_assinatura(self, empresa_id: str) -> set[Pilar]:
        return {Pilar(r["pilar"]) for r in self.con.execute(
            "SELECT pilar FROM assinaturas WHERE empresa_id=?", (empresa_id,))}

    # --------------------------------------------------------------- fatos
    def salvar_fato(self, f: Fato) -> None:
        """Grava o fato já encadeado ao anterior, formando a trilha auditável."""
        anterior = self.con.execute(
            "SELECT hash FROM fatos ORDER BY id DESC LIMIT 1").fetchone()
        hash_anterior = anterior["hash"] if anterior else GENESE
        dados = json.loads(json.dumps(f.dados, default=str))   # normaliza tipos
        em = f.em.isoformat()
        h = resumir(f.evento.value, f.empresa_id, f.origem.value,
                    dados, em, hash_anterior)
        self.con.execute(
            "INSERT INTO fatos (evento,empresa_id,origem,dados,em,hash,hash_anterior) "
            "VALUES (?,?,?,?,?,?,?)",
            (f.evento.value, f.empresa_id, f.origem.value,
             json.dumps(dados, ensure_ascii=False), em, h, hash_anterior),
        )
        self.con.commit()

    # -------------------------------------------------------------- trilha
    def conferir_trilha(self, empresa_id: str | None = None) -> Conferencia:
        """
        Refaz a corrente inteira e diz se alguém mexeu na base por fora.

        A corrente é global (um livro só para todo o sistema), então a
        conferência roda sempre sobre tudo; `empresa_id` serve para o recibo.
        """
        linhas = [
            {"id": r["id"], "evento": r["evento"], "empresa_id": r["empresa_id"],
             "origem": r["origem"], "dados": json.loads(r["dados"]),
             "em": r["em"], "hash": r["hash"], "hash_anterior": r["hash_anterior"]}
            for r in self.con.execute("SELECT * FROM fatos ORDER BY id ASC")
        ]
        return conferir(linhas)

    def listar_fatos(self, empresa_id: str | None = None, limite: int = 200) -> list[Fato]:
        if empresa_id:
            cur = self.con.execute(
                "SELECT * FROM fatos WHERE empresa_id=? ORDER BY id DESC LIMIT ?",
                (empresa_id, limite))
        else:
            cur = self.con.execute("SELECT * FROM fatos ORDER BY id DESC LIMIT ?", (limite,))
        return [Fato(evento=Evento(r["evento"]), empresa_id=r["empresa_id"],
                     origem=Pilar(r["origem"]), dados=json.loads(r["dados"]),
                     em=datetime.fromisoformat(r["em"])) for r in cur]

    def contar_fatos(self, empresa_id: str) -> int:
        return self.con.execute(
            "SELECT COUNT(*) c FROM fatos WHERE empresa_id=?", (empresa_id,)).fetchone()["c"]

    # ------------------------------------------------------------- alertas
    def salvar_alerta(self, a: Alerta) -> None:
        self.con.execute(
            "INSERT INTO alertas (empresa_id,pilar,titulo,detalhe,severidade,origem_evento,em) "
            "VALUES (?,?,?,?,?,?,?)",
            (a.empresa_id, a.pilar.value, a.titulo, a.detalhe, a.severidade,
             a.origem_evento.value if a.origem_evento else None, a.em.isoformat()),
        )
        self.con.commit()

    def listar_alertas(self, empresa_id: str, limite: int = 100) -> list[Alerta]:
        cur = self.con.execute(
            "SELECT * FROM alertas WHERE empresa_id=? ORDER BY id DESC LIMIT ?",
            (empresa_id, limite))
        return [Alerta(empresa_id=r["empresa_id"], pilar=Pilar(r["pilar"]),
                       titulo=r["titulo"], detalhe=r["detalhe"], severidade=r["severidade"],
                       origem_evento=Evento(r["origem_evento"]) if r["origem_evento"] else None,
                       em=datetime.fromisoformat(r["em"])) for r in cur]


def _para_empresa(r: sqlite3.Row) -> Empresa:
    return Empresa(
        cnpj=r["cnpj"], razao_social=r["razao_social"], regime=Regime(r["regime"]),
        municipio=r["municipio"] or "", uf=r["uf"] or "",
        abertura=date.fromisoformat(r["abertura"]) if r["abertura"] else None,
        id=r["id"],
    )

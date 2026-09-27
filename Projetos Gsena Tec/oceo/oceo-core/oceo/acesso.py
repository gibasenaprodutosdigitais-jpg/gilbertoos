"""
Login e isolamento entre clientes.

Duas responsabilidades, e as duas são de segurança:

1. Provar que a pessoa é quem diz ser (senha e sessão).
2. Garantir que ela só enxergue as empresas às quais tem acesso. Num sistema
   multiempresa, vazar dado de um cliente para outro é o pior defeito
   possível — pior que cair.

Sem dependência externa: PBKDF2-HMAC-SHA256 e `secrets` são da stdlib e são
o caminho recomendado quando não se usa uma biblioteca dedicada.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import unicodedata
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

from .repositorio import RepositorioSQLite

# OWASP recomenda, para PBKDF2-HMAC-SHA256, pelo menos 600.000 iterações.
ITERACOES = 600_000
DURACAO_SESSAO = timedelta(hours=12)
MINIMO_SENHA = 10


class FalhaDeLogin(Exception):
    """Credencial inválida, usuário inativo ou sessão expirada."""


class AcessoNegado(Exception):
    """Autenticado, mas sem permissão sobre este recurso."""


class SenhaFraca(Exception):
    """Senha abaixo da política mínima."""


@dataclass
class Usuario:
    id: str
    email: str
    nome: str
    ativo: bool = True


# --------------------------------------------------------------- senha

def _normalizar(senha: str) -> bytes:
    """NFKC para que a mesma senha digitada com acento componha igual."""
    return unicodedata.normalize("NFKC", senha).encode("utf-8")


def cifrar_senha(senha: str, salt: bytes | None = None) -> tuple[str, str]:
    if len(senha) < MINIMO_SENHA:
        raise SenhaFraca(f"A senha precisa de pelo menos {MINIMO_SENHA} caracteres.")
    salt = salt or secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", _normalizar(senha), salt, ITERACOES)
    return dk.hex(), salt.hex()


def conferir_senha(senha: str, senha_hash: str, salt_hex: str) -> bool:
    dk = hashlib.pbkdf2_hmac("sha256", _normalizar(senha), bytes.fromhex(salt_hex), ITERACOES)
    # comparação em tempo constante: evita descobrir o hash medindo o tempo
    return hmac.compare_digest(dk.hex(), senha_hash)


# --------------------------------------------------------------- serviço

class ControleDeAcesso:
    def __init__(self, repo: RepositorioSQLite):
        self.repo = repo

    # ---- usuários
    def criar_usuario(self, email: str, nome: str, senha: str) -> Usuario:
        email = email.strip().lower()
        senha_hash, salt = cifrar_senha(senha)
        uid = str(uuid.uuid4())
        try:
            self.repo.con.execute(
                "INSERT INTO usuarios (id,email,nome,senha_hash,salt,ativo,criado_em) "
                "VALUES (?,?,?,?,?,1,?)",
                (uid, email, nome, senha_hash, salt, datetime.now().isoformat()),
            )
            self.repo.con.commit()
        except Exception as erro:
            raise FalhaDeLogin(f"Não foi possível criar o usuário: {erro}") from erro
        return Usuario(id=uid, email=email, nome=nome)

    def entrar(self, email: str, senha: str) -> str:
        """Devolve o token da sessão. Mensagem de erro é sempre a mesma,
        para não revelar se o e-mail existe."""
        generico = FalhaDeLogin("E-mail ou senha incorretos.")
        r = self.repo.con.execute(
            "SELECT * FROM usuarios WHERE email=?", (email.strip().lower(),)).fetchone()
        if not r or not r["ativo"]:
            # gasta o mesmo tempo de um hash real, para não vazar por timing
            cifrar_senha("x" * MINIMO_SENHA)
            raise generico
        if not conferir_senha(senha, r["senha_hash"], r["salt"]):
            raise generico

        token = secrets.token_urlsafe(32)
        agora = datetime.now()
        self.repo.con.execute(
            "INSERT INTO sessoes (token,usuario_id,criada_em,expira_em) VALUES (?,?,?,?)",
            (token, r["id"], agora.isoformat(), (agora + DURACAO_SESSAO).isoformat()),
        )
        self.repo.con.commit()
        return token

    def sair(self, token: str) -> None:
        self.repo.con.execute("DELETE FROM sessoes WHERE token=?", (token,))
        self.repo.con.commit()

    def usuario_da_sessao(self, token: str | None) -> Usuario:
        if not token:
            raise FalhaDeLogin("Faça login para continuar.")
        r = self.repo.con.execute(
            "SELECT s.expira_em, u.* FROM sessoes s JOIN usuarios u ON u.id = s.usuario_id "
            "WHERE s.token=?", (token,)).fetchone()
        if not r:
            raise FalhaDeLogin("Sessão inválida.")
        if datetime.fromisoformat(r["expira_em"]) < datetime.now():
            self.sair(token)
            raise FalhaDeLogin("Sessão expirada. Entre novamente.")
        if not r["ativo"]:
            raise FalhaDeLogin("Usuário inativo.")
        return Usuario(id=r["id"], email=r["email"], nome=r["nome"], ativo=True)

    def limpar_sessoes_vencidas(self) -> int:
        cur = self.repo.con.execute(
            "DELETE FROM sessoes WHERE expira_em < ?", (datetime.now().isoformat(),))
        self.repo.con.commit()
        return cur.rowcount

    # ---- permissão sobre empresa
    def conceder(self, usuario_id: str, empresa_id: str, papel: str = "operador") -> None:
        if papel not in ("dono", "operador", "leitor"):
            raise ValueError(f"Papel desconhecido: {papel}")
        self.repo.con.execute(
            "INSERT INTO acessos (usuario_id,empresa_id,papel) VALUES (?,?,?) "
            "ON CONFLICT(usuario_id,empresa_id) DO UPDATE SET papel=excluded.papel",
            (usuario_id, empresa_id, papel),
        )
        self.repo.con.commit()

    def revogar(self, usuario_id: str, empresa_id: str) -> None:
        self.repo.con.execute(
            "DELETE FROM acessos WHERE usuario_id=? AND empresa_id=?",
            (usuario_id, empresa_id))
        self.repo.con.commit()

    def papel_em(self, usuario_id: str, empresa_id: str) -> str | None:
        r = self.repo.con.execute(
            "SELECT papel FROM acessos WHERE usuario_id=? AND empresa_id=?",
            (usuario_id, empresa_id)).fetchone()
        return r["papel"] if r else None

    def empresas_de(self, usuario_id: str) -> list[str]:
        return [r["empresa_id"] for r in self.repo.con.execute(
            "SELECT empresa_id FROM acessos WHERE usuario_id=?", (usuario_id,))]

    def exigir_acesso(self, usuario: Usuario, empresa_id: str,
                      escrita: bool = False) -> str:
        """
        Porta única de autorização. Toda rota que toca dado de empresa passa
        por aqui — inclusive as de leitura, senão o isolamento tem furo.
        """
        papel = self.papel_em(usuario.id, empresa_id)
        if papel is None:
            # mesma resposta de "não existe": não confirma a existência da empresa
            raise AcessoNegado("Empresa não encontrada para este usuário.")
        if escrita and papel == "leitor":
            raise AcessoNegado("Seu acesso a esta empresa é somente leitura.")
        return papel

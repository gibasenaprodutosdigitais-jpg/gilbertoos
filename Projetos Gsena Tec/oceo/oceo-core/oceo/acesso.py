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

from .correio import Enviador, EnviadorArquivo, texto_recuperacao
from .repositorio import RepositorioSQLite

# OWASP recomenda, para PBKDF2-HMAC-SHA256, pelo menos 600.000 iterações.
ITERACOES = 600_000
DURACAO_SESSAO = timedelta(hours=12)
MINIMO_SENHA = 10

# Trava de força bruta. Janela deslizante: conta as falhas recentes.
JANELA_TENTATIVAS = timedelta(minutes=15)
MAX_FALHAS_CONTA = 5      # por e-mail tentado
MAX_FALHAS_ORIGEM = 20    # por endereço de rede, contra varredura de contas

# Recuperação de senha
DURACAO_RECUPERACAO = timedelta(minutes=30)


class FalhaDeLogin(Exception):
    """Credencial inválida, usuário inativo ou sessão expirada."""


class AcessoNegado(Exception):
    """Autenticado, mas sem permissão sobre este recurso."""


class SenhaFraca(Exception):
    """Senha abaixo da política mínima."""


class ExcessoDeTentativas(Exception):
    """Tentativas demais em pouco tempo. Bloqueio temporário."""


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


def _resumo_token(token: str) -> str:
    """
    O token de recuperação é guardado resumido, nunca em claro.

    Motivo: quem roubar o banco encontra só o resumo, que não serve para
    redefinir senha nenhuma. É o mesmo princípio da senha — com a diferença
    de que aqui basta SHA-256, porque o token já é aleatório e longo, não
    precisa ser protegido contra tentativa de adivinhação.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# --------------------------------------------------------------- serviço

class ControleDeAcesso:
    def __init__(self, repo: RepositorioSQLite, enviador: Enviador | None = None,
                 base_url: str = "http://127.0.0.1:8000"):
        self.repo = repo
        self.enviador = enviador or EnviadorArquivo()
        self.base_url = base_url.rstrip("/")

    # ---- trava de força bruta
    def _falhas_recentes(self, chave: str) -> list[datetime]:
        desde = (datetime.now() - JANELA_TENTATIVAS).isoformat()
        return [datetime.fromisoformat(r["em"]) for r in self.repo.con.execute(
            "SELECT em FROM tentativas WHERE chave=? AND em>=? ORDER BY em",
            (chave, desde))]

    def _conferir_trava(self, chave: str, maximo: int) -> None:
        falhas = self._falhas_recentes(chave)
        if len(falhas) < maximo:
            return
        libera = falhas[0] + JANELA_TENTATIVAS
        faltam = max(1, int((libera - datetime.now()).total_seconds() // 60) + 1)
        raise ExcessoDeTentativas(
            f"Tentativas demais. Tente novamente em {faltam} minuto(s).")

    def _anotar_falha(self, *chaves: str) -> None:
        agora = datetime.now().isoformat()
        self.repo.con.executemany(
            "INSERT INTO tentativas (chave,em) VALUES (?,?)",
            [(c, agora) for c in chaves if c])
        self.repo.con.commit()

    def _limpar_falhas(self, chave: str) -> None:
        self.repo.con.execute("DELETE FROM tentativas WHERE chave=?", (chave,))
        self.repo.con.commit()

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

    def entrar(self, email: str, senha: str, origem: str = "") -> str:
        """
        Devolve o token da sessão. Mensagem de erro é sempre a mesma,
        para não revelar se o e-mail existe.

        `origem` é o endereço de rede de quem está tentando. Serve para
        travar quem varre muitas contas diferentes a partir do mesmo lugar —
        ataque que a trava por conta, sozinha, não pega.
        """
        generico = FalhaDeLogin("E-mail ou senha incorretos.")
        email = email.strip().lower()
        chave_conta, chave_origem = f"conta:{email}", f"origem:{origem}" if origem else ""

        # A trava é conferida ANTES de saber se o e-mail existe, e a falha é
        # anotada mesmo para e-mail inexistente. Sem isso, o bloqueio só
        # aconteceria em conta real — e virar-se-ia num jeito de descobrir
        # quem é cliente do OCEO.
        self._conferir_trava(chave_conta, MAX_FALHAS_CONTA)
        if chave_origem:
            self._conferir_trava(chave_origem, MAX_FALHAS_ORIGEM)

        r = self.repo.con.execute(
            "SELECT * FROM usuarios WHERE email=?", (email,)).fetchone()
        if not r or not r["ativo"]:
            # gasta o mesmo tempo de um hash real, para não vazar por timing
            cifrar_senha("x" * MINIMO_SENHA)
            self._anotar_falha(chave_conta, chave_origem)
            raise generico
        if not conferir_senha(senha, r["senha_hash"], r["salt"]):
            self._anotar_falha(chave_conta, chave_origem)
            raise generico

        self._limpar_falhas(chave_conta)   # acertou: o contador zera
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

    # ---- recuperação de senha
    def pedir_recuperacao(self, email: str) -> None:
        """
        Dispara o e-mail de redefinição, se a conta existir.

        Não devolve nada, e de propósito: o token só sai daqui pelo e-mail.
        Quem chama esta função — inclusive a API — nunca vê o token, então
        não há como vazá-lo numa resposta por descuido.

        Também não avisa se o e-mail existe ou não. Um formulário de
        "esqueci minha senha" que responde "este e-mail não está cadastrado"
        entrega a lista de clientes para qualquer um.
        """
        email = email.strip().lower()
        r = self.repo.con.execute(
            "SELECT id, nome, ativo FROM usuarios WHERE email=?", (email,)).fetchone()
        if not r or not r["ativo"]:
            return

        # um pedido novo invalida os anteriores: só o último link funciona
        self.repo.con.execute("DELETE FROM recuperacoes WHERE usuario_id=?", (r["id"],))

        token = secrets.token_urlsafe(32)
        agora = datetime.now()
        self.repo.con.execute(
            "INSERT INTO recuperacoes (token_hash,usuario_id,criada_em,expira_em) "
            "VALUES (?,?,?,?)",
            (_resumo_token(token), r["id"], agora.isoformat(),
             (agora + DURACAO_RECUPERACAO).isoformat()),
        )
        self.repo.con.commit()

        minutos = int(DURACAO_RECUPERACAO.total_seconds() // 60)
        self.enviador.enviar(
            email, "Redefinição de senha — OCEO",
            texto_recuperacao(r["nome"], f"{self.base_url}/?redefinir={token}", minutos),
        )

    def redefinir_senha(self, token: str, nova_senha: str) -> Usuario:
        """Troca a senha e derruba todas as sessões abertas daquele usuário."""
        invalido = FalhaDeLogin("Link inválido ou vencido. Peça um novo.")
        r = self.repo.con.execute(
            "SELECT r.*, u.email, u.nome FROM recuperacoes r "
            "JOIN usuarios u ON u.id = r.usuario_id WHERE r.token_hash=?",
            (_resumo_token(token),)).fetchone()
        if not r or r["usada_em"]:
            raise invalido
        if datetime.fromisoformat(r["expira_em"]) < datetime.now():
            raise invalido

        senha_hash, salt = cifrar_senha(nova_senha)   # levanta SenhaFraca se curta
        agora = datetime.now().isoformat()
        self.repo.con.execute(
            "UPDATE usuarios SET senha_hash=?, salt=? WHERE id=?",
            (senha_hash, salt, r["usuario_id"]))
        self.repo.con.execute(
            "UPDATE recuperacoes SET usada_em=? WHERE token_hash=?", (agora, r["token_hash"]))
        # se a conta estava tomada, o invasor perde o acesso neste instante
        self.repo.con.execute("DELETE FROM sessoes WHERE usuario_id=?", (r["usuario_id"],))
        self.repo.con.commit()
        self._limpar_falhas(f"conta:{r['email']}")
        return Usuario(id=r["usuario_id"], email=r["email"], nome=r["nome"])

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

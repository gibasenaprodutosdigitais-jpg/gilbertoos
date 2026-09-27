"""
Provas das duas travas da porta de entrada:
  - força bruta no login
  - recuperação de senha

Rodar com:  python3 testes/test_protecao_login.py
"""
from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from oceo.acesso import (DURACAO_RECUPERACAO, ExcessoDeTentativas,  # noqa: E402
                         FalhaDeLogin, MAX_FALHAS_CONTA, SenhaFraca,
                         ControleDeAcesso, _resumo_token)
from oceo.correio import EnviadorSilencioso                          # noqa: E402
from oceo.repositorio import RepositorioSQLite                       # noqa: E402

_falhas: list[str] = []
SENHA = "senhaboa2026"


def checar(cond: bool, desc: str) -> None:
    print(f"  {'ok  ' if cond else 'FALHOU'} {desc}")
    if not cond:
        _falhas.append(desc)


def cenario():
    repo = RepositorioSQLite(":memory:")
    correio = EnviadorSilencioso()
    ac = ControleDeAcesso(repo, enviador=correio)
    ac.criar_usuario("gilberto@grupo.com", "Gilberto", SENHA)
    return ac, correio


def token_do_email(correio: EnviadorSilencioso) -> str:
    _, _, corpo = correio.enviados[-1]
    return re.search(r"redefinir=([\w\-]+)", corpo).group(1)


# ---------------------------------------------------------------- força bruta
def teste_bloqueia_depois_de_n_falhas():
    print(f"\n[1] A conta trava depois de {MAX_FALHAS_CONTA} senhas erradas")
    ac, _ = cenario()
    for i in range(MAX_FALHAS_CONTA):
        try:
            ac.entrar("gilberto@grupo.com", "chute errado")
        except FalhaDeLogin:
            pass
        except ExcessoDeTentativas:
            checar(False, f"travou cedo demais, na tentativa {i+1}")
            return
    try:
        ac.entrar("gilberto@grupo.com", "chute errado")
        checar(False, "deveria ter travado e não travou")
    except ExcessoDeTentativas as erro:
        checar(True, f"travou na tentativa seguinte: {erro}")


def teste_senha_certa_tambem_barrada_enquanto_travado():
    print("\n[2] Enquanto travado, nem a senha certa entra  ← é o ponto da trava")
    ac, _ = cenario()
    for _ in range(MAX_FALHAS_CONTA):
        try:
            ac.entrar("gilberto@grupo.com", "chute errado")
        except FalhaDeLogin:
            pass
    try:
        ac.entrar("gilberto@grupo.com", SENHA)
        checar(False, "a senha certa passou durante o bloqueio")
    except ExcessoDeTentativas:
        checar(True, "a senha certa também é barrada durante o bloqueio")


def teste_acerto_zera_o_contador():
    print("\n[3] Acertar a senha zera o contador de falhas")
    ac, _ = cenario()
    for _ in range(MAX_FALHAS_CONTA - 1):
        try:
            ac.entrar("gilberto@grupo.com", "chute errado")
        except FalhaDeLogin:
            pass
    ac.entrar("gilberto@grupo.com", SENHA)          # acertou
    sobrou = ac._falhas_recentes("conta:gilberto@grupo.com")
    checar(sobrou == [], "as falhas anteriores foram apagadas")
    for _ in range(MAX_FALHAS_CONTA - 1):           # o orçamento voltou inteiro
        try:
            ac.entrar("gilberto@grupo.com", "chute errado")
        except ExcessoDeTentativas:
            checar(False, "travou antes da hora depois do acerto")
            return
        except FalhaDeLogin:
            pass
    checar(True, "depois do acerto, o orçamento de tentativas volta ao cheio")


def teste_trava_vale_para_email_inexistente():
    print("\n[4] O bloqueio vale igual para e-mail que não existe")
    ac, _ = cenario()
    for _ in range(MAX_FALHAS_CONTA):
        try:
            ac.entrar("ninguem@lugar-nenhum.com", "chute")
        except FalhaDeLogin:
            pass
    try:
        ac.entrar("ninguem@lugar-nenhum.com", "chute")
        checar(False, "e-mail inexistente não travou")
    except ExcessoDeTentativas:
        checar(True, "travou também para e-mail inexistente")
    checar(True, "logo o bloqueio não revela quem é cliente do OCEO")


def teste_trava_por_origem():
    print("\n[5] Varrer muitas contas do mesmo lugar também trava")
    ac, _ = cenario()
    travou = False
    for i in range(40):
        try:
            ac.entrar(f"alvo{i}@empresa.com", "chute", origem="203.0.113.7")
        except FalhaDeLogin:
            pass
        except ExcessoDeTentativas:
            travou = True
            checar(True, f"a origem foi travada depois de {i} contas diferentes")
            break
    if not travou:
        checar(False, "varredura de 40 contas diferentes não travou a origem")
    # e quem vem de outro lugar continua entrando normalmente
    try:
        ac.entrar("gilberto@grupo.com", SENHA, origem="198.51.100.2")
        checar(True, "outra origem não é afetada pelo bloqueio")
    except Exception as erro:
        checar(False, f"origem inocente foi barrada: {erro}")


def teste_bloqueio_expira():
    print("\n[6] O bloqueio é temporário, não permanente")
    ac, _ = cenario()
    for _ in range(MAX_FALHAS_CONTA):
        try:
            ac.entrar("gilberto@grupo.com", "chute errado")
        except FalhaDeLogin:
            pass
    # envelhece as falhas como se a janela já tivesse passado
    velho = (datetime.now() - timedelta(hours=1)).isoformat()
    ac.repo.con.execute("UPDATE tentativas SET em=?", (velho,))
    ac.repo.con.commit()
    try:
        ac.entrar("gilberto@grupo.com", SENHA)
        checar(True, "passada a janela, a conta volta a aceitar login")
    except Exception as erro:
        checar(False, f"a conta continuou travada: {erro}")


# ------------------------------------------------------------- recuperação
def teste_fluxo_de_recuperacao():
    print("\n[7] Recuperar a senha funciona ponta a ponta")
    ac, correio = cenario()
    ac.pedir_recuperacao("gilberto@grupo.com")
    checar(len(correio.enviados) == 1, "saiu um e-mail")
    ac.redefinir_senha(token_do_email(correio), "novasenha2026")
    try:
        ac.entrar("gilberto@grupo.com", "novasenha2026")
        checar(True, "a senha nova entra")
    except Exception as erro:
        checar(False, f"a senha nova não entrou: {erro}")
    try:
        ac.entrar("gilberto@grupo.com", SENHA)
        checar(False, "a senha antiga ainda funciona")
    except FalhaDeLogin:
        checar(True, "a senha antiga parou de funcionar")


def teste_token_usado_uma_vez_so():
    print("\n[8] O link só vale uma vez")
    ac, correio = cenario()
    ac.pedir_recuperacao("gilberto@grupo.com")
    tok = token_do_email(correio)
    ac.redefinir_senha(tok, "novasenha2026")
    try:
        ac.redefinir_senha(tok, "outrasenha2026")
        checar(False, "o mesmo link funcionou duas vezes")
    except FalhaDeLogin:
        checar(True, "o segundo uso do mesmo link foi recusado")


def teste_token_vence():
    print("\n[9] O link vence")
    ac, correio = cenario()
    ac.pedir_recuperacao("gilberto@grupo.com")
    tok = token_do_email(correio)
    vencido = (datetime.now() - timedelta(minutes=1)).isoformat()
    ac.repo.con.execute("UPDATE recuperacoes SET expira_em=?", (vencido,))
    ac.repo.con.commit()
    try:
        ac.redefinir_senha(tok, "novasenha2026")
        checar(False, "link vencido funcionou")
    except FalhaDeLogin:
        checar(True, f"link vencido recusado (validade: {DURACAO_RECUPERACAO})")


def teste_pedido_novo_invalida_o_anterior():
    print("\n[10] Pedir de novo invalida o link anterior")
    ac, correio = cenario()
    ac.pedir_recuperacao("gilberto@grupo.com")
    primeiro = token_do_email(correio)
    ac.pedir_recuperacao("gilberto@grupo.com")
    segundo = token_do_email(correio)
    checar(primeiro != segundo, "o segundo link é diferente do primeiro")
    try:
        ac.redefinir_senha(primeiro, "novasenha2026")
        checar(False, "o link antigo ainda funcionava")
    except FalhaDeLogin:
        checar(True, "o link antigo foi invalidado")


def teste_token_nao_fica_em_claro_no_banco():
    print("\n[11] O token não fica legível no banco  ← se roubarem a base")
    ac, correio = cenario()
    ac.pedir_recuperacao("gilberto@grupo.com")
    tok = token_do_email(correio)
    guardado = ac.repo.con.execute("SELECT token_hash FROM recuperacoes").fetchone()[0]
    checar(tok not in guardado, "o token em claro não está no banco")
    checar(guardado == _resumo_token(tok), "o banco guarda só o resumo do token")


def teste_redefinir_derruba_sessoes():
    print("\n[12] Redefinir a senha derruba as sessões abertas")
    ac, correio = cenario()
    sessao = ac.entrar("gilberto@grupo.com", SENHA)     # como se fosse o invasor
    ac.pedir_recuperacao("gilberto@grupo.com")
    ac.redefinir_senha(token_do_email(correio), "novasenha2026")
    try:
        ac.usuario_da_sessao(sessao)
        checar(False, "a sessão antiga continuou válida")
    except FalhaDeLogin:
        checar(True, "quem estava dentro com a senha antiga foi desconectado")


def teste_email_inexistente_nao_vaza():
    print("\n[13] Pedir recuperação de e-mail inexistente não revela nada")
    ac, correio = cenario()
    try:
        ac.pedir_recuperacao("ninguem@lugar-nenhum.com")
        checar(True, "não levantou erro nem mensagem diferente")
    except Exception as erro:
        checar(False, f"reagiu diferente para e-mail inexistente: {erro}")
    checar(correio.enviados == [], "e nenhum e-mail foi enviado")


def teste_senha_nova_obedece_a_politica():
    print("\n[14] A senha nova passa pela mesma política de força")
    ac, correio = cenario()
    ac.pedir_recuperacao("gilberto@grupo.com")
    tok = token_do_email(correio)
    try:
        ac.redefinir_senha(tok, "123")
        checar(False, "aceitou senha curta na redefinição")
    except SenhaFraca:
        checar(True, "senha curta recusada")
    try:
        ac.redefinir_senha(tok, "novasenha2026")
        checar(True, "e o link continua valendo depois da recusa")
    except FalhaDeLogin:
        checar(False, "a tentativa recusada queimou o link")


if __name__ == "__main__":
    print("=" * 66)
    print("OCEO — provas da porta de entrada (força bruta e recuperação)")
    print("=" * 66)
    for fn in [teste_bloqueia_depois_de_n_falhas,
               teste_senha_certa_tambem_barrada_enquanto_travado,
               teste_acerto_zera_o_contador,
               teste_trava_vale_para_email_inexistente,
               teste_trava_por_origem, teste_bloqueio_expira,
               teste_fluxo_de_recuperacao, teste_token_usado_uma_vez_so,
               teste_token_vence, teste_pedido_novo_invalida_o_anterior,
               teste_token_nao_fica_em_claro_no_banco,
               teste_redefinir_derruba_sessoes,
               teste_email_inexistente_nao_vaza,
               teste_senha_nova_obedece_a_politica]:
        fn()
    print("\n" + "=" * 66)
    if _falhas:
        print(f"{len(_falhas)} FALHA(S):")
        for f in _falhas:
            print(f"  - {f}")
        sys.exit(1)
    print("Tudo passou. A porta de entrada está travada.")

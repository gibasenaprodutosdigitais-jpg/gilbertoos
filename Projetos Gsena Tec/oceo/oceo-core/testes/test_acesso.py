"""
Provas de login, persistência e isolamento entre clientes.
Rodar com:  python3 testes/test_acesso.py

O teste mais importante deste arquivo é o [5]: um cliente não pode, em
hipótese alguma, enxergar a empresa de outro.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from oceo.acesso import (AcessoNegado, FalhaDeLogin, SenhaFraca,   # noqa: E402
                         cifrar_senha, conferir_senha)
from oceo.dominio import Empresa, Evento, Pilar, Regime            # noqa: E402
from oceo.montagem import montar                                   # noqa: E402

_falhas: list[str] = []


def checar(cond: bool, desc: str) -> None:
    print(f"  {'ok  ' if cond else 'FALHOU'} {desc}")
    if not cond:
        _falhas.append(desc)


def empresa(cnpj: str, nome: str) -> Empresa:
    return Empresa(cnpj=cnpj, razao_social=nome, regime=Regime.SIMPLES)


# --------------------------------------------------------------------------
def teste_senha():
    print("\n[1] Senha é guardada cifrada, nunca em texto")
    h, salt = cifrar_senha("senha-bem-longa-123")
    checar("senha-bem-longa-123" not in h, "a senha não aparece no hash")
    checar(len(salt) == 32, "cada senha tem salt próprio (16 bytes)")
    checar(conferir_senha("senha-bem-longa-123", h, salt), "a senha certa confere")
    checar(not conferir_senha("senha-errada-9999", h, salt), "a senha errada não confere")

    h2, _ = cifrar_senha("senha-bem-longa-123")
    checar(h2 != h, "duas contas com a MESMA senha geram hashes diferentes")

    try:
        cifrar_senha("curta")
        checar(False, "deveria recusar senha curta")
    except SenhaFraca:
        checar(True, "recusa senha abaixo do mínimo")


def teste_login():
    print("\n[2] Login, sessão e saída")
    _, acesso = montar()
    u = acesso.criar_usuario("gilberto@oceo.com.br", "Gilberto", "uma-senha-forte-1")
    token = acesso.entrar("gilberto@oceo.com.br", "uma-senha-forte-1")
    checar(bool(token) and len(token) > 30, "login devolveu token de sessão")
    checar(acesso.usuario_da_sessao(token).id == u.id, "a sessão identifica o usuário")

    try:
        acesso.entrar("gilberto@oceo.com.br", "senha-errada-aqui")
        checar(False, "deveria recusar senha errada")
    except FalhaDeLogin as e:
        checar("incorretos" in str(e), f"recusa senha errada sem dizer qual campo falhou")

    try:
        acesso.entrar("naoexiste@oceo.com.br", "uma-senha-forte-1")
        checar(False, "deveria recusar e-mail inexistente")
    except FalhaDeLogin as e:
        checar("incorretos" in str(e),
               "e-mail inexistente dá a MESMA mensagem (não revela quem é cliente)")

    acesso.sair(token)
    try:
        acesso.usuario_da_sessao(token)
        checar(False, "deveria invalidar a sessão após sair")
    except FalhaDeLogin:
        checar(True, "sair invalida a sessão")


def teste_sem_token():
    print("\n[3] Sem sessão não se entra")
    _, acesso = montar()
    for token, desc in [(None, "sem token"), ("", "token vazio"),
                        ("inventado-do-nada", "token inventado")]:
        try:
            acesso.usuario_da_sessao(token)
            checar(False, f"deveria recusar {desc}")
        except FalhaDeLogin:
            checar(True, f"recusa {desc}")


def teste_persistencia():
    print("\n[4] O dado sobrevive ao desligamento do servidor")
    with tempfile.TemporaryDirectory() as pasta:
        banco = Path(pasta) / "oceo.db"

        sis, acesso = montar(banco)
        u = acesso.criar_usuario("dono@empresa.com.br", "Dono", "senha-do-dono-1")
        e = sis.cadastrar(empresa("13.592.146/0001-15", "Empresa Um"), {Pilar.GC, Pilar.GF})
        acesso.conceder(u.id, e.id, "dono")
        sis.anunciar(Evento.FOLHA_PROCESSADA, e.id, Pilar.GC, total=38_500.0)
        sis.repo.fechar()                      # simula o servidor caindo

        sis2, acesso2 = montar(banco)          # sobe de novo
        checar(e.id in sis2.empresas, "a empresa continuou lá depois de reiniciar")
        checar(sis2.assinatura_de(e.id).tem(Pilar.GF), "os pilares ativos foram preservados")
        checar(bool(sis2.alertas_de(e.id)), "os alertas foram preservados")
        checar(sis2.repo.contar_fatos(e.id) >= 1, "o histórico de eventos foi preservado")
        token = acesso2.entrar("dono@empresa.com.br", "senha-do-dono-1")
        checar(bool(token), "o usuário consegue entrar depois do reinício")
        sis2.repo.fechar()


def teste_isolamento():
    print("\n[5] Um cliente NÃO enxerga a empresa do outro  ← o mais importante")
    sis, acesso = montar()
    ana = acesso.criar_usuario("ana@clientea.com.br", "Ana", "senha-da-ana-123")
    bruno = acesso.criar_usuario("bruno@clienteb.com.br", "Bruno", "senha-do-bruno-12")

    ea = sis.cadastrar(empresa("13.592.146/0001-15", "Cliente A"), {Pilar.GC})
    eb = sis.cadastrar(empresa("11.222.333/0001-81", "Cliente B"), {Pilar.GC})
    acesso.conceder(ana.id, ea.id, "dono")
    acesso.conceder(bruno.id, eb.id, "dono")

    checar(acesso.empresas_de(ana.id) == [ea.id], "Ana só lista a empresa dela")
    checar(acesso.empresas_de(bruno.id) == [eb.id], "Bruno só lista a empresa dele")

    checar(acesso.exigir_acesso(ana, ea.id) == "dono", "Ana acessa a própria empresa")
    try:
        acesso.exigir_acesso(ana, eb.id)
        checar(False, "VAZAMENTO: Ana acessou a empresa do Bruno")
    except AcessoNegado as erro:
        checar("não encontrada" in str(erro),
               "Ana é barrada na empresa do Bruno, sem confirmar que ela existe")


def teste_papel_leitor():
    print("\n[6] Leitor lê, mas não altera")
    sis, acesso = montar()
    contador = acesso.criar_usuario("contador@escritorio.com.br", "Contador",
                                    "senha-contador-1")
    e = sis.cadastrar(empresa("13.592.146/0001-15", "Empresa Um"), {Pilar.GC})
    acesso.conceder(contador.id, e.id, "leitor")

    checar(acesso.exigir_acesso(contador, e.id) == "leitor", "o leitor consegue ler")
    try:
        acesso.exigir_acesso(contador, e.id, escrita=True)
        checar(False, "deveria barrar escrita do leitor")
    except AcessoNegado as erro:
        checar("somente leitura" in str(erro), "o leitor é barrado ao tentar alterar")

    acesso.revogar(contador.id, e.id)
    try:
        acesso.exigir_acesso(contador, e.id)
        checar(False, "deveria barrar após revogar")
    except AcessoNegado:
        checar(True, "revogar o acesso tira o usuário da empresa na hora")


def teste_sessao_expirada():
    print("\n[7] Sessão vencida não vale")
    from datetime import datetime, timedelta
    _, acesso = montar()
    acesso.criar_usuario("z@oceo.com.br", "Z", "senha-qualquer-12")
    token = acesso.entrar("z@oceo.com.br", "senha-qualquer-12")
    vencida = (datetime.now() - timedelta(minutes=1)).isoformat()
    acesso.repo.con.execute("UPDATE sessoes SET expira_em=? WHERE token=?", (vencida, token))
    acesso.repo.con.commit()
    try:
        acesso.usuario_da_sessao(token)
        checar(False, "deveria recusar sessão vencida")
    except FalhaDeLogin as erro:
        checar("expirada" in str(erro).lower(), "sessão vencida é recusada")
    checar(acesso.limpar_sessoes_vencidas() >= 0, "faxina de sessões vencidas roda")


if __name__ == "__main__":
    print("=" * 66)
    print("OCEO — provas de login, persistência e isolamento")
    print("=" * 66)
    for fn in [teste_senha, teste_login, teste_sem_token, teste_persistencia,
               teste_isolamento, teste_papel_leitor, teste_sessao_expirada]:
        fn()
    print("\n" + "=" * 66)
    if _falhas:
        print(f"{len(_falhas)} FALHA(S):")
        for f in _falhas:
            print(f"  - {f}")
        sys.exit(1)
    print("Tudo passou. Login e isolamento de pé.")

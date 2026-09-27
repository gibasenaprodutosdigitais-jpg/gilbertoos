"""
Provas de que a trilha detecta adulteração.
Rodar com:  python3 testes/test_trilha.py

Cada teste simula alguém mexendo direto no banco, por fora do sistema —
o cenário que a corrente de hashes existe para pegar.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from oceo.dominio import Empresa, Evento, Pilar, Regime      # noqa: E402
from oceo.montagem import montar                             # noqa: E402
from oceo.trilha import recibo, resumir                      # noqa: E402

_falhas: list[str] = []


def checar(cond: bool, desc: str) -> None:
    print(f"  {'ok  ' if cond else 'FALHOU'} {desc}")
    if not cond:
        _falhas.append(desc)


def cenario(qtd: int = 4):
    """Um sistema com alguns fatos já gravados."""
    sis, acesso = montar()
    e = sis.cadastrar(Empresa(cnpj="13.592.146/0001-15", razao_social="Empresa Um",
                              regime=Regime.SIMPLES), {Pilar.GC, Pilar.GF})
    for i in range(qtd):
        sis.anunciar(Evento.FOLHA_PROCESSADA, e.id, Pilar.GC, total=1000.0 * (i + 1))
    return sis, e


# --------------------------------------------------------------------------
def teste_trilha_integra():
    print("\n[1] Trilha intacta é reconhecida como íntegra")
    sis, e = cenario()
    c = sis.repo.conferir_trilha()
    checar(c.integra, "a trilha recém-gravada está íntegra")
    checar(c.registros == 4, f"conferiu os 4 registros (viu {c.registros})")
    checar(len(c.hash_raiz) == 64, "o resumo do período tem 64 caracteres (SHA-256)")


def teste_cada_elo_aponta_para_o_anterior():
    print("\n[2] Cada registro carrega o elo do anterior")
    sis, _ = cenario(3)
    linhas = list(sis.repo.con.execute("SELECT * FROM fatos ORDER BY id"))
    checar(linhas[0]["hash_anterior"] == "0" * 64, "o primeiro aponta para a gênese")
    encadeados = all(linhas[i]["hash_anterior"] == linhas[i-1]["hash"]
                     for i in range(1, len(linhas)))
    checar(encadeados, "cada registro seguinte aponta para o hash do anterior")


def teste_alterar_valor_e_pego():
    print("\n[3] Alterar um valor no banco é detectado  ← o que importa")
    sis, _ = cenario()
    alvo = sis.repo.con.execute("SELECT id FROM fatos ORDER BY id LIMIT 1 OFFSET 1").fetchone()
    sis.repo.con.execute("UPDATE fatos SET dados=? WHERE id=?",
                         ('{"total": 999999.0}', alvo["id"]))
    sis.repo.con.commit()
    c = sis.repo.conferir_trilha()
    checar(not c.integra, "a adulteração foi detectada")
    checar(c.rompeu_em == alvo["id"], f"apontou o registro exato ({c.rompeu_em})")
    checar("alterado" in c.motivo, f"explicou o que houve: {c.motivo}")


def teste_apagar_registro_e_pego():
    print("\n[4] Apagar um registro do meio é detectado")
    sis, _ = cenario()
    alvo = sis.repo.con.execute("SELECT id FROM fatos ORDER BY id LIMIT 1 OFFSET 1").fetchone()
    sis.repo.con.execute("DELETE FROM fatos WHERE id=?", (alvo["id"],))
    sis.repo.con.commit()
    c = sis.repo.conferir_trilha()
    checar(not c.integra, "a remoção foi detectada")
    checar("removido" in c.motivo or "reordenado" in c.motivo,
           f"explicou o que houve: {c.motivo}")


def teste_recalcular_o_hash_nao_salva_o_fraudador():
    print("\n[5] Não adianta recalcular o hash do registro alterado")
    sis, _ = cenario()
    alvo = sis.repo.con.execute(
        "SELECT * FROM fatos ORDER BY id LIMIT 1 OFFSET 1").fetchone()
    novos_dados = {"total": 999999.0}
    # o fraudador refaz o hash daquele registro, para "consertar" a prova
    h = resumir(alvo["evento"], alvo["empresa_id"], alvo["origem"],
                novos_dados, alvo["em"], alvo["hash_anterior"])
    sis.repo.con.execute("UPDATE fatos SET dados=?, hash=? WHERE id=?",
                         ('{"total": 999999.0}', h, alvo["id"]))
    sis.repo.con.commit()
    c = sis.repo.conferir_trilha()
    checar(not c.integra,
           "ainda assim foi detectado: os registros seguintes apontam para o hash antigo")
    checar(c.rompeu_em == alvo["id"] + 1,
           f"a quebra aparece no registro seguinte ({c.rompeu_em})")


def teste_inserir_registro_falso():
    print("\n[6] Inserir um registro inventado é detectado")
    sis, e = cenario()
    sis.repo.con.execute(
        "INSERT INTO fatos (evento,empresa_id,origem,dados,em,hash,hash_anterior) "
        "VALUES (?,?,?,?,?,?,?)",
        ("gc.folha_processada", e.id, "GC", '{"total": 1.0}',
         "2026-01-01T00:00:00", "f" * 64, "e" * 64))
    sis.repo.con.commit()
    c = sis.repo.conferir_trilha()
    checar(not c.integra, "o registro inventado foi detectado")


def teste_recibo_nao_vaza_dado():
    print("\n[7] O recibo prova sem expor dado do cliente")
    sis, e = cenario()
    r = recibo(sis.repo.conferir_trilha(), e.id)
    texto = str(r)
    checar(r["integra"] is True, "o recibo diz que a trilha está íntegra")
    checar("1000" not in texto and "4000" not in texto,
           "nenhum valor de folha aparece no recibo")
    checar("Empresa Um" not in texto, "a razão social não aparece no recibo")
    checar(len(r["hash_raiz"]) == 64, "o recibo carrega o resumo do período")


def teste_trilha_sobrevive_ao_reinicio():
    print("\n[8] A corrente continua depois de reiniciar o servidor")
    import tempfile
    with tempfile.TemporaryDirectory() as pasta:
        banco = Path(pasta) / "oceo.db"
        sis, _ = montar(banco)
        e = sis.cadastrar(Empresa(cnpj="13.592.146/0001-15", razao_social="Empresa Um",
                                  regime=Regime.SIMPLES), {Pilar.GC})
        sis.anunciar(Evento.FOLHA_PROCESSADA, e.id, Pilar.GC, total=1000.0)
        raiz1 = sis.repo.conferir_trilha().hash_raiz
        sis.repo.fechar()

        sis2, _ = montar(banco)
        sis2.anunciar(Evento.FOLHA_PROCESSADA, e.id, Pilar.GC, total=2000.0)
        c = sis2.repo.conferir_trilha()
        checar(c.integra, "a trilha segue íntegra após o reinício")
        checar(c.registros == 2, "o registro novo entrou na mesma corrente")
        checar(c.hash_raiz != raiz1, "o resumo do período mudou, como deve")
        sis2.repo.fechar()


if __name__ == "__main__":
    print("=" * 66)
    print("OCEO — provas da trilha auditável (integridade dos dados)")
    print("=" * 66)
    for fn in [teste_trilha_integra, teste_cada_elo_aponta_para_o_anterior,
               teste_alterar_valor_e_pego, teste_apagar_registro_e_pego,
               teste_recalcular_o_hash_nao_salva_o_fraudador,
               teste_inserir_registro_falso, teste_recibo_nao_vaza_dado,
               teste_trilha_sobrevive_ao_reinicio]:
        fn()
    print("\n" + "=" * 66)
    if _falhas:
        print(f"{len(_falhas)} FALHA(S):")
        for f in _falhas:
            print(f"  - {f}")
        sys.exit(1)
    print("Tudo passou. A trilha pega adulteração.")

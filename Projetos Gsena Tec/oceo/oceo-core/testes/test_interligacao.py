"""
Provas de que a interligação funciona. Rodar com:  python3 testes/test_interligacao.py

Sem framework de propósito: qualquer máquina com Python roda, inclusive a do
Gilberto, sem instalar nada.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from oceo.dominio import Empresa, Evento, Pilar, Regime          # noqa: E402
from oceo.montagem import montar                                  # noqa: E402
from oceo.nucleo import DependenciaFaltando, PilarNaoContratado   # noqa: E402

_falhas: list[str] = []


def checar(condicao: bool, descricao: str) -> None:
    print(f"  {'ok  ' if condicao else 'FALHOU'} {descricao}")
    if not condicao:
        _falhas.append(descricao)


def nova_empresa(sis, pilares):
    e = Empresa(cnpj="13.592.146/0001-15", razao_social="Empresa Exemplo Ltda",
                regime=Regime.SIMPLES, municipio="Belo Horizonte", uf="MG")
    sis.cadastrar(e, pilares)
    return e


# --------------------------------------------------------------------------
def teste_cadastro_unico():
    print("\n[1] O cadastro do cliente é único, não um por pilar")
    sis = montar()
    e = nova_empresa(sis, {Pilar.GC, Pilar.GF})
    checar(len(sis.empresas) == 1, "uma empresa cadastrada, compartilhada pelos pilares")
    checar(e.cnpj == "13592146000115", "CNPJ normalizado (só dígitos)")
    checar(e.cnpj_formatado == "13.592.146/0001-15", "CNPJ formatado para exibição")


def teste_dependencia_entre_pilares():
    print("\n[2] Um pilar não liga sem o pré-requisito dele")
    sis = montar()
    e = nova_empresa(sis, {Pilar.GC})
    try:
        sis.assinatura_de(e.id).ativar(Pilar.GI)   # GI depende de GF
        checar(False, "deveria ter recusado GI sem GF")
    except DependenciaFaltando as erro:
        checar("GF" in str(erro), f"recusou GI sem GF: {erro}")

    sis.assinatura_de(e.id).ativar(Pilar.GF)
    sis.assinatura_de(e.id).ativar(Pilar.GI)
    checar(sis.assinatura_de(e.id).tem(Pilar.GI), "com GF ativo, GI pôde ser ligado")


def teste_cadeia_gc_gf_gi():
    print("\n[3] A cadeia atravessa três pilares: GC fecha apuração → GF → GI")
    sis = montar()
    e = nova_empresa(sis, {Pilar.GC, Pilar.GF, Pilar.GI})

    sis.anunciar(Evento.APURACAO_FECHADA, e.id, Pilar.GC,
                 competencia="09/2026", receita=120_000.0,
                 custo_fixo=70_000.0, imposto=8_000.0)
    eventos = [f.evento for f in sis.barramento.historico]
    checar(Evento.DRE_ATUALIZADA in eventos,
           "o GF reagiu sozinho à apuração do GC e atualizou a DRE")

    sis.anunciar(Evento.RESERVA_COMPLETA, e.id, Pilar.GF, meses_cobertos=3)
    eventos = [f.evento for f in sis.barramento.historico]
    checar(Evento.TRILHA_LIBERADA in eventos,
           "a reserva de 3 meses liberou a trilha do GI, em cadeia")

    trilha = [a for a in sis.alertas_de(e.id) if a.pilar == Pilar.GI]
    checar(bool(trilha), "o cliente recebeu o alerta do GI")
    checar("não constitui recomendação" in trilha[0].detalhe.lower(),
           "o disclaimer regulatório do GI veio junto (trava da CVM)")


def teste_reserva_insuficiente_nao_libera():
    print("\n[4] Reserva abaixo da política não libera a trilha")
    sis = montar()
    e = nova_empresa(sis, {Pilar.GC, Pilar.GF, Pilar.GI})
    sis.anunciar(Evento.RESERVA_COMPLETA, e.id, Pilar.GF, meses_cobertos=1)
    checar(Evento.TRILHA_LIBERADA not in [f.evento for f in sis.barramento.historico],
           "1 mês de reserva não abriu a trilha (mínimo são 3)")


def teste_pilar_nao_contratado_fica_de_fora():
    print("\n[5] Quem não contratou o pilar não recebe a saída dele")
    sis = montar()
    e = nova_empresa(sis, {Pilar.GC})          # sem GJ
    sis.anunciar(Evento.APURACAO_FECHADA, e.id, Pilar.GC,
                 competencia="09/2026", receita=100_000.0,
                 custo_fixo=50_000.0, imposto=20_000.0)   # carga de 20%
    checar(not [a for a in sis.alertas_de(e.id) if a.pilar == Pilar.GJ],
           "sem GJ contratado, nenhum alerta jurídico foi gerado")

    sis2 = montar()
    e2 = nova_empresa(sis2, {Pilar.GC, Pilar.GJ})
    sis2.anunciar(Evento.APURACAO_FECHADA, e2.id, Pilar.GC,
                  competencia="09/2026", receita=100_000.0,
                  custo_fixo=50_000.0, imposto=20_000.0)
    checar(bool([a for a in sis2.alertas_de(e2.id) if a.pilar == Pilar.GJ]),
           "com GJ contratado, a mesma apuração gerou a oportunidade tributária")


def teste_nao_deixa_pilar_desligado_publicar():
    print("\n[6] Pilar desligado não consegue publicar evento")
    sis = montar()
    e = nova_empresa(sis, {Pilar.GC})
    try:
        sis.anunciar(Evento.VENDA_FECHADA, e.id, Pilar.GM, valor=5_000.0)
        checar(False, "deveria ter recusado o GM")
    except PilarNaoContratado:
        checar(True, "recusou publicar em nome de pilar não contratado")


def teste_desativar_cai_em_cascata():
    print("\n[7] Desligar um pilar derruba quem dependia dele")
    sis = montar()
    e = nova_empresa(sis, {Pilar.GC, Pilar.GF, Pilar.GI})
    caidos = sis.assinatura_de(e.id).desativar(Pilar.GF)
    checar(Pilar.GI in caidos, "ao desligar GF, o GI caiu junto")
    checar(not sis.assinatura_de(e.id).tem(Pilar.GI), "GI ficou inativo")
    checar(sis.assinatura_de(e.id).tem(Pilar.GC), "GC, que não dependia, seguiu ativo")


def teste_painel_do_portal():
    print("\n[8] O portal recebe tudo o que precisa numa chamada")
    sis = montar()
    e = nova_empresa(sis, {Pilar.GC, Pilar.GF})
    sis.anunciar(Evento.FOLHA_PROCESSADA, e.id, Pilar.GC, total=38_500.0)
    p = sis.painel(e.id)
    checar(p["empresa"]["cnpj"] == "13.592.146/0001-15", "dados da empresa no painel")
    checar(len(p["pilares"]) == 5, "os 5 pilares aparecem, com ativo/inativo")
    checar(bool(p["alertas"]), "os alertas chegaram ao painel")


if __name__ == "__main__":
    print("=" * 66)
    print("OCEO — provas de interligação entre os pilares")
    print("=" * 66)
    for fn in [teste_cadastro_unico, teste_dependencia_entre_pilares,
               teste_cadeia_gc_gf_gi, teste_reserva_insuficiente_nao_libera,
               teste_pilar_nao_contratado_fica_de_fora,
               teste_nao_deixa_pilar_desligado_publicar,
               teste_desativar_cai_em_cascata, teste_painel_do_portal]:
        fn()
    print("\n" + "=" * 66)
    if _falhas:
        print(f"{len(_falhas)} FALHA(S):")
        for f in _falhas:
            print(f"  - {f}")
        sys.exit(1)
    print("Tudo passou. Os pilares estão conversando.")

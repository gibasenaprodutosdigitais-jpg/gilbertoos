"""
As reações de cada pilar aos fatos dos outros. É a interligação em si.

Cada função aqui responde a uma regra que já estava fechada nos documentos
dos pilares (05/ago/2026). O comentário de cada bloco aponta a regra de
origem, pra que ninguém mude o comportamento sem saber de onde ele veio.

Nenhum pilar importa outro pilar. Todos falam só com o barramento.
"""
from __future__ import annotations

from ..dominio import Alerta, Evento, Fato, Pilar
from ..nucleo import Barramento, Sistema

# Parâmetros de negócio, num lugar só, para não ficarem espalhados em ifs.
MESES_DE_RESERVA_PADRAO = 3          # "três meses de ponto de equilíbrio" (Pilar 2)
MARGEM_ALERTA_FLUXO = 0.10           # caixa abaixo de 10% do PE liga alerta
DISCLAIMER_GI = (
    "Conteúdo educacional e informativo. Não constitui recomendação "
    "individualizada de investimento."
)


def registrar_todas(barramento: Barramento) -> None:
    """Liga todas as reações no barramento. Chamado uma vez, na montagem."""

    # ---------------------------------------------------------------- GC → GF
    # Pilar 2: "Relação com o Pilar 1 — quem faz o quê, pra não duplicar
    # escopo". O GC apura; o GF lê a apuração e atualiza a leitura financeira.
    @barramento.quando(Evento.APURACAO_FECHADA, Pilar.GF)
    def gf_atualiza_dre(fato: Fato, sis: Sistema) -> None:
        receita = fato.dados.get("receita", 0.0)
        custo_fixo = fato.dados.get("custo_fixo", 0.0)
        ponto_equilibrio = custo_fixo
        sis.anunciar(
            Evento.DRE_ATUALIZADA, fato.empresa_id, Pilar.GF,
            receita=receita, ponto_equilibrio=ponto_equilibrio,
            competencia=fato.dados.get("competencia"),
        )

    # ---------------------------------------------------------------- GC → GJ
    # Pilar 3: "Divisão de escopo com Pilar 1/2: Fiscal (Pilar 1) apura e
    # calcula; o Jurídico aponta a oportunidade de redução."
    @barramento.quando(Evento.APURACAO_FECHADA, Pilar.GJ)
    def gj_procura_oportunidade(fato: Fato, sis: Sistema) -> None:
        receita = fato.dados.get("receita", 0.0)
        imposto = fato.dados.get("imposto", 0.0)
        if receita <= 0:
            return
        carga = imposto / receita
        if carga > 0.12:
            sis.alertar(Alerta(
                empresa_id=fato.empresa_id, pilar=Pilar.GJ,
                titulo="Carga tributária acima do esperado para o regime",
                detalhe=(
                    f"A apuração de {fato.dados.get('competencia','período')} fechou "
                    f"em {carga:.1%} da receita. Vale revisar enquadramento e "
                    f"aproveitamento de créditos antes da próxima competência."
                ),
                severidade="atencao", origem_evento=fato.evento,
            ))
            sis.anunciar(
                Evento.OPORTUNIDADE_TRIBUTARIA, fato.empresa_id, Pilar.GJ,
                carga=carga, competencia=fato.dados.get("competencia"),
            )

    # ---------------------------------------------------------------- GC → GF
    # Divergência fiscal vira risco de caixa, porque multa e juros saem do caixa.
    @barramento.quando(Evento.DIVERGENCIA_FISCAL, Pilar.GF)
    def gf_reserva_para_divergencia(fato: Fato, sis: Sistema) -> None:
        valor = fato.dados.get("valor", 0.0)
        sis.alertar(Alerta(
            empresa_id=fato.empresa_id, pilar=Pilar.GF,
            titulo="Provisionar divergência apontada pela contabilidade",
            detalhe=(
                f"A contabilidade apontou divergência de R$ {valor:,.2f}. "
                f"Enquanto não for resolvida, trate como saída provável do caixa."
            ),
            severidade="atencao", origem_evento=fato.evento,
        ))

    # ---------------------------------------------------------------- GF → GI
    # Pilar 5: "Pré-requisito: ativação em cadeia com o Pilar 2". A trilha
    # educacional só abre depois que a casa está em ordem — reserva formada.
    @barramento.quando(Evento.RESERVA_COMPLETA, Pilar.GI)
    def gi_libera_trilha(fato: Fato, sis: Sistema) -> None:
        meses = fato.dados.get("meses_cobertos", 0)
        if meses < MESES_DE_RESERVA_PADRAO:
            return
        sis.alertar(Alerta(
            empresa_id=fato.empresa_id, pilar=Pilar.GI,
            titulo="Trilha de educação financeira liberada",
            detalhe=(
                f"A reserva cobre {meses} meses de ponto de equilíbrio, o mínimo "
                f"definido na política. A trilha educacional foi liberada. "
                f"{DISCLAIMER_GI}"
            ),
            severidade="informativo", origem_evento=fato.evento,
        ))
        sis.anunciar(
            Evento.TRILHA_LIBERADA, fato.empresa_id, Pilar.GI,
            meses_cobertos=meses, disclaimer=DISCLAIMER_GI,
        )

    # ---------------------------------------------------------------- GF → GJ
    @barramento.quando(Evento.MISTURA_PF_PJ, Pilar.GJ)
    def gj_alerta_mistura(fato: Fato, sis: Sistema) -> None:
        sis.alertar(Alerta(
            empresa_id=fato.empresa_id, pilar=Pilar.GJ,
            titulo="Patrimônio pessoal exposto por mistura de PF e PJ",
            detalhe=(
                "Movimentações pessoais na conta da empresa enfraquecem a "
                "separação patrimonial e facilitam desconsideração da "
                "personalidade jurídica. Vale regularizar o pró-labore."
            ),
            severidade="critico", origem_evento=fato.evento,
        ))

    # ---------------------------------------------------------------- GM → GF
    # Venda fechada entra na projeção de caixa do financeiro.
    @barramento.quando(Evento.VENDA_FECHADA, Pilar.GF)
    def gf_projeta_venda(fato: Fato, sis: Sistema) -> None:
        valor = fato.dados.get("valor", 0.0)
        sis.alertar(Alerta(
            empresa_id=fato.empresa_id, pilar=Pilar.GF,
            titulo="Nova venda entrou na projeção de caixa",
            detalhe=f"Venda de R$ {valor:,.2f} registrada pelo comercial.",
            severidade="informativo", origem_evento=fato.evento,
        ))

    # ---------------------------------------------------------------- GF → GM
    # Fluxo em risco segura investimento em mídia. Evita queimar caixa em
    # tráfego quando a empresa não tem fôlego.
    @barramento.quando(Evento.FLUXO_EM_RISCO, Pilar.GM)
    def gm_segura_midia(fato: Fato, sis: Sistema) -> None:
        sis.alertar(Alerta(
            empresa_id=fato.empresa_id, pilar=Pilar.GM,
            titulo="Revisar verba de mídia antes de novo aporte",
            detalhe=(
                "O financeiro sinalizou risco no fluxo de caixa. Antes de "
                "aumentar investimento em tráfego, confirme o caixa disponível."
            ),
            severidade="atencao", origem_evento=fato.evento,
        ))

    # ---------------------------------------------------------------- GC → GF
    @barramento.quando(Evento.FOLHA_PROCESSADA, Pilar.GF)
    def gf_folha_no_fluxo(fato: Fato, sis: Sistema) -> None:
        total = fato.dados.get("total", 0.0)
        sis.alertar(Alerta(
            empresa_id=fato.empresa_id, pilar=Pilar.GF,
            titulo="Folha lançada no fluxo de caixa",
            detalhe=f"Folha de R$ {total:,.2f} processada pelo DP e refletida no caixa.",
            severidade="informativo", origem_evento=fato.evento,
        ))

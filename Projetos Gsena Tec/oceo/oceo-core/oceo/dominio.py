"""
Domínio compartilhado do OCEO.

Este é o vocabulário único do sistema. Todo pilar fala esta linguagem, e é
por isso que eles conseguem conversar entre si sem virar cinco sistemas
separados com cinco cadastros do mesmo cliente.

Sem dependência externa de propósito: o miolo do OCEO tem que rodar em
qualquer máquina, com Python puro, e ser testável sem subir servidor.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any


# --------------------------------------------------------------- os pilares

class Pilar(str, Enum):
    """Os cinco pilares do OCEO. O código curto é o que circula no sistema."""
    GC = "GC"   # Contabilidade e BI      (Contábil, Fiscal, DP, RH, Legalização)
    GF = "GF"   # Gestão Financeira       (ERP + banco, DRE, fundo de reserva)
    GJ = "GJ"   # Jurídico                (consultivo interno)
    GM = "GM"   # Marketing e Vendas      (agência + comercial)
    GI = "GI"   # Educação Pré-Investimento

    @property
    def nome(self) -> str:
        return {
            "GC": "Contabilidade e BI",
            "GF": "Gestão Financeira",
            "GJ": "Jurídico",
            "GM": "Marketing e Vendas",
            "GI": "Educação Pré-Investimento",
        }[self.value]


# Dependências declaradas, extraídas das regras já fechadas nos documentos
# dos pilares (05/ago/2026). Não é enfeite: o sistema recusa ativar um pilar
# cujo pré-requisito não esteja ativo — ver nucleo.Assinatura.ativar.
DEPENDENCIAS: dict[Pilar, tuple[Pilar, ...]] = {
    Pilar.GC: (),
    Pilar.GF: (Pilar.GC,),           # "Relação com o Pilar 1, pra não duplicar escopo"
    Pilar.GJ: (Pilar.GC,),           # fiscal apura no GC; GJ busca a oportunidade
    Pilar.GM: (),
    Pilar.GI: (Pilar.GF,),           # "Pré-requisito: ativação em cadeia com o Pilar 2"
}


# --------------------------------------------------------------- o cliente

class Regime(str, Enum):
    SIMPLES = "simples_nacional"
    PRESUMIDO = "lucro_presumido"
    REAL = "lucro_real"
    MEI = "mei"


@dataclass
class Empresa:
    """
    O cadastro único. Existe UMA empresa no sistema, não uma cópia por pilar.
    É o que impede o cliente de recadastrar o CNPJ em cada módulo.
    """
    cnpj: str
    razao_social: str
    regime: Regime
    municipio: str = ""
    uf: str = ""
    abertura: date | None = None
    id: str = ""

    def __post_init__(self) -> None:
        self.cnpj = so_digitos(self.cnpj)
        if len(self.cnpj) != 14:
            raise ValueError(f"CNPJ precisa ter 14 dígitos, veio {len(self.cnpj)}")
        if not self.id:
            self.id = self.cnpj

    @property
    def cnpj_formatado(self) -> str:
        c = self.cnpj
        return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"


def so_digitos(texto: str) -> str:
    return "".join(c for c in texto if c.isdigit())


# --------------------------------------------------------------- os eventos

class Evento(str, Enum):
    """
    O que um pilar anuncia ao resto do sistema. É por aqui que a interligação
    acontece: o pilar que produz o fato não sabe (nem precisa saber) quem vai
    reagir a ele.
    """
    # GC — Contabilidade e BI
    APURACAO_FECHADA = "gc.apuracao_fechada"
    DIVERGENCIA_FISCAL = "gc.divergencia_fiscal"
    FOLHA_PROCESSADA = "gc.folha_processada"

    # GF — Gestão Financeira
    DRE_ATUALIZADA = "gf.dre_atualizada"
    FLUXO_EM_RISCO = "gf.fluxo_em_risco"
    RESERVA_COMPLETA = "gf.reserva_completa"     # gatilho do GI
    MISTURA_PF_PJ = "gf.mistura_pf_pj"

    # GJ — Jurídico
    OPORTUNIDADE_TRIBUTARIA = "gj.oportunidade_tributaria"
    RISCO_CONTRATUAL = "gj.risco_contratual"

    # GM — Marketing e Vendas
    LEAD_QUALIFICADO = "gm.lead_qualificado"
    VENDA_FECHADA = "gm.venda_fechada"

    # GI — Educação Pré-Investimento
    TRILHA_LIBERADA = "gi.trilha_liberada"


@dataclass
class Fato:
    """Um evento que aconteceu, com quem o gerou e os dados que carrega."""
    evento: Evento
    empresa_id: str
    origem: Pilar
    dados: dict[str, Any] = field(default_factory=dict)
    em: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"[{self.origem.value}] {self.evento.value} · {self.empresa_id}"


@dataclass
class Alerta:
    """
    O que o sistema devolve ao cliente. Nasce da reação de um pilar a um fato
    de outro — é a prova visível de que a interligação funcionou.
    """
    empresa_id: str
    pilar: Pilar
    titulo: str
    detalhe: str
    severidade: str = "informativo"       # informativo | atencao | critico
    origem_evento: Evento | None = None
    em: datetime = field(default_factory=datetime.now)

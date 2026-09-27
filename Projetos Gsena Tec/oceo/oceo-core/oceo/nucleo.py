"""
O núcleo do OCEO: o barramento de eventos e o controle de assinatura.

É aqui que "interligar os produtos" deixa de ser conversa e vira código.

A ideia é simples: nenhum pilar chama outro pilar diretamente. Quem apura o
imposto (GC) não sabe que existe um módulo jurídico. Ele apenas ANUNCIA que
fechou a apuração, e quem tiver interesse reage. Isso é o que permite ligar,
desligar ou vender um pilar separado sem quebrar os outros.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Callable

from .dominio import DEPENDENCIAS, Alerta, Empresa, Evento, Fato, Pilar

Reacao = Callable[[Fato, "Sistema"], None]


class PilarNaoContratado(Exception):
    """Alguém tentou usar um pilar que o cliente não assinou."""


class DependenciaFaltando(Exception):
    """Tentou ativar um pilar sem o pré-requisito dele."""


# --------------------------------------------------------------- assinatura

class Assinatura:
    """
    Quais pilares esta empresa contratou. O OCEO é vendido por pilar, então o
    sistema precisa saber o que está ligado — e recusar o que não está.
    """

    def __init__(self, empresa: Empresa, pilares: set[Pilar] | None = None):
        self.empresa = empresa
        self.pilares: set[Pilar] = set()
        for p in sorted(pilares or set(), key=_ordem_dependencia):
            self.ativar(p)

    def ativar(self, pilar: Pilar) -> None:
        faltando = [d for d in DEPENDENCIAS[pilar] if d not in self.pilares]
        if faltando:
            nomes = ", ".join(f"{d.value} ({d.nome})" for d in faltando)
            raise DependenciaFaltando(
                f"{pilar.value} ({pilar.nome}) depende de {nomes}. "
                f"Ative o pré-requisito antes."
            )
        self.pilares.add(pilar)

    def desativar(self, pilar: Pilar) -> list[Pilar]:
        """Desliga o pilar e, em cascata, quem dependia dele."""
        caidos = []
        for outro, deps in DEPENDENCIAS.items():
            if pilar in deps and outro in self.pilares:
                caidos += [outro, *self.desativar(outro)]
        self.pilares.discard(pilar)
        return caidos

    def tem(self, pilar: Pilar) -> bool:
        return pilar in self.pilares


def _ordem_dependencia(p: Pilar) -> int:
    """
    Profundidade da cadeia de pré-requisitos, para ativar na ordem certa.

    Contar só as dependências diretas não basta: GF e GI têm uma cada, mas o
    GI depende do GF, então precisa entrar depois. É profundidade, não
    quantidade.
    """
    deps = DEPENDENCIAS[p]
    return 0 if not deps else 1 + max(_ordem_dependencia(d) for d in deps)


# --------------------------------------------------------------- barramento

class Barramento:
    """
    O canal por onde os fatos circulam. Guarda quem reage a quê.

    Uma reação só roda se o pilar dono dela estiver contratado pela empresa —
    é a trava que impede um cliente de receber saída de módulo que não pagou.
    """

    def __init__(self) -> None:
        self._reacoes: dict[Evento, list[tuple[Pilar, Reacao]]] = defaultdict(list)
        self.historico: list[Fato] = []

    def quando(self, evento: Evento, pilar: Pilar) -> Callable[[Reacao], Reacao]:
        """Decorador: registra que `pilar` reage a `evento`."""
        def registrar(fn: Reacao) -> Reacao:
            self._reacoes[evento].append((pilar, fn))
            return fn
        return registrar

    def publicar(self, fato: Fato, sistema: "Sistema") -> None:
        self.historico.append(fato)
        assinatura = sistema.assinatura_de(fato.empresa_id)
        for pilar, reagir in self._reacoes[fato.evento]:
            if assinatura and assinatura.tem(pilar):
                reagir(fato, sistema)

    def reacoes_de(self, evento: Evento) -> list[Pilar]:
        return [p for p, _ in self._reacoes[evento]]


# --------------------------------------------------------------- o sistema

class Sistema:
    """
    A composição de tudo: empresas, assinaturas, barramento e alertas.

    É o ponto único de entrada. A API e o portal conversam só com ele, nunca
    com os pilares direto.

    Sem repositório, roda em memória (útil em teste). Com repositório, tudo
    sobrevive ao desligamento do servidor. As regras de negócio não mudam
    entre os dois modos, porque elas não sabem onde o dado é guardado.
    """

    def __init__(self, repo=None) -> None:
        self.barramento = Barramento()
        self.repo = repo
        self.empresas: dict[str, Empresa] = {}
        self.assinaturas: dict[str, Assinatura] = {}
        self.alertas: list[Alerta] = []
        if repo:
            self._recarregar()

    def _recarregar(self) -> None:
        """Traz do banco o que já existia. Chamado ao subir o sistema."""
        for empresa in self.repo.listar_empresas():
            self.empresas[empresa.id] = empresa
            a = Assinatura.__new__(Assinatura)      # sem revalidar dependência
            a.empresa = empresa
            a.pilares = self.repo.carregar_assinatura(empresa.id)
            self.assinaturas[empresa.id] = a
        self.barramento.historico = self.repo.listar_fatos()

    # ---- cadastro
    def cadastrar(self, empresa: Empresa, pilares: set[Pilar] | None = None) -> Empresa:
        assinatura = Assinatura(empresa, pilares)   # valida dependências aqui
        self.empresas[empresa.id] = empresa
        self.assinaturas[empresa.id] = assinatura
        if self.repo:
            self.repo.salvar_empresa(empresa)
            self.repo.salvar_assinatura(empresa.id, assinatura.pilares)
        return empresa

    def assinatura_de(self, empresa_id: str) -> Assinatura | None:
        return self.assinaturas.get(empresa_id)

    def salvar_assinatura(self, empresa_id: str) -> None:
        """Persiste a assinatura depois de ligar ou desligar um pilar."""
        if self.repo and empresa_id in self.assinaturas:
            self.repo.salvar_assinatura(empresa_id, self.assinaturas[empresa_id].pilares)

    def exigir(self, empresa_id: str, pilar: Pilar) -> None:
        a = self.assinatura_de(empresa_id)
        if not a or not a.tem(pilar):
            raise PilarNaoContratado(
                f"A empresa {empresa_id} não tem o pilar {pilar.value} ({pilar.nome}) ativo."
            )

    # ---- eventos
    def anunciar(self, evento: Evento, empresa_id: str, origem: Pilar, **dados) -> Fato:
        self.exigir(empresa_id, origem)
        fato = Fato(evento=evento, empresa_id=empresa_id, origem=origem, dados=dados)
        if self.repo:
            self.repo.salvar_fato(fato)
        self.barramento.publicar(fato, self)
        return fato

    # ---- saída para o cliente
    def alertar(self, alerta: Alerta) -> Alerta:
        self.alertas.append(alerta)
        if self.repo:
            self.repo.salvar_alerta(alerta)
        return alerta

    def alertas_de(self, empresa_id: str) -> list[Alerta]:
        if self.repo:
            return self.repo.listar_alertas(empresa_id)
        return [a for a in self.alertas if a.empresa_id == empresa_id]

    def painel(self, empresa_id: str) -> dict:
        """O que o portal mostra na tela inicial do cliente."""
        empresa = self.empresas[empresa_id]
        assinatura = self.assinaturas[empresa_id]
        alertas = self.alertas_de(empresa_id)
        return {
            "empresa": {
                "id": empresa.id,
                "cnpj": empresa.cnpj_formatado,
                "razao_social": empresa.razao_social,
                "regime": empresa.regime.value,
            },
            "pilares": [
                {
                    "codigo": p.value,
                    "nome": p.nome,
                    "ativo": assinatura.tem(p),
                    "depende_de": [d.value for d in DEPENDENCIAS[p]],
                }
                for p in Pilar
            ],
            "alertas": [
                {
                    "pilar": a.pilar.value,
                    "titulo": a.titulo,
                    "detalhe": a.detalhe,
                    "severidade": a.severidade,
                    "origem": a.origem_evento.value if a.origem_evento else None,
                    "em": a.em.isoformat(timespec="seconds"),
                }
                for a in sorted(alertas, key=lambda x: x.em, reverse=True)
            ],
            "eventos_no_periodo": (
                self.repo.contar_fatos(empresa_id) if self.repo
                else len([f for f in self.barramento.historico
                          if f.empresa_id == empresa_id])
            ),
        }

"""
Montagem do sistema: o único lugar que sabe juntar as peças.

A API, o portal e os testes chamam `montar()` e recebem um sistema pronto,
com todas as reações já ligadas no barramento.
"""
from __future__ import annotations

from .nucleo import Sistema
from .pilares import reacoes


def montar() -> Sistema:
    sistema = Sistema()
    reacoes.registrar_todas(sistema.barramento)
    return sistema

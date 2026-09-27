"""
Montagem do sistema: o único lugar que sabe juntar as peças.

A API, o portal e os testes chamam `montar()` e recebem um sistema pronto,
com todas as reações já ligadas no barramento.
"""
from __future__ import annotations

from pathlib import Path

from .acesso import ControleDeAcesso
from .nucleo import Sistema
from .pilares import reacoes
from .repositorio import RepositorioSQLite


def montar(banco: str | Path | None = None) -> tuple[Sistema, ControleDeAcesso]:
    """
    `banco=None` roda tudo em memória (teste, demonstração).
    `banco="oceo.db"` persiste em disco.
    """
    repo = RepositorioSQLite(banco or ":memory:")
    sistema = Sistema(repo)
    reacoes.registrar_todas(sistema.barramento)
    return sistema, ControleDeAcesso(repo)

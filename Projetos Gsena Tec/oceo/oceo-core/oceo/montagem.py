"""
Montagem do sistema: o único lugar que sabe juntar as peças.

A API, o portal e os testes chamam `montar()` e recebem um sistema pronto,
com todas as reações já ligadas no barramento.
"""
from __future__ import annotations

from pathlib import Path

from .acesso import ControleDeAcesso
from .correio import Enviador
from .nucleo import Sistema
from .pilares import reacoes
from .repositorio import RepositorioSQLite


def montar(banco: str | Path | None = None, enviador: Enviador | None = None,
           base_url: str = "http://127.0.0.1:8000") -> tuple[Sistema, ControleDeAcesso]:
    """
    `banco=None` roda tudo em memória (teste, demonstração).
    `banco="oceo.db"` persiste em disco.

    `enviador=None` grava os e-mails em arquivo em vez de enviar — ver
    `correio.py`. O envio de verdade ainda não está ligado.
    """
    repo = RepositorioSQLite(banco or ":memory:")
    sistema = Sistema(repo)
    reacoes.registrar_todas(sistema.barramento)
    return sistema, ControleDeAcesso(repo, enviador=enviador, base_url=base_url)

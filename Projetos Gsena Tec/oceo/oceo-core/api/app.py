"""
A API do OCEO. É a única porta entre o mundo de fora e o núcleo.

O portal, o app e qualquer integração futura falam com isto aqui — nunca
com os pilares direto. Trocar o portal por outro não encosta no miolo.

Subir:  python3 api/app.py      (ou: uvicorn api.app:app --reload)
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from fastapi import FastAPI, HTTPException                      # noqa: E402
from fastapi.responses import FileResponse                       # noqa: E402
from pydantic import BaseModel, Field                            # noqa: E402

from oceo.dominio import Empresa, Evento, Pilar, Regime          # noqa: E402
from oceo.montagem import montar                                 # noqa: E402
from oceo.nucleo import DependenciaFaltando, PilarNaoContratado  # noqa: E402

app = FastAPI(
    title="OCEO",
    description="Núcleo de interligação dos cinco pilares.",
    version="0.1.0",
)

# Uma instância em memória. Trocar por banco é substituir este objeto —
# o resto do código não muda, porque todo mundo conversa via Sistema.
sistema = montar()


# ------------------------------------------------------------------ modelos

class EmpresaEntrada(BaseModel):
    cnpj: str
    razao_social: str
    regime: Regime = Regime.SIMPLES
    municipio: str = ""
    uf: str = ""
    pilares: list[Pilar] = Field(default_factory=list)


class EventoEntrada(BaseModel):
    evento: Evento
    origem: Pilar
    dados: dict = Field(default_factory=dict)


# ------------------------------------------------------------------- rotas

@app.get("/api/saude")
def saude() -> dict:
    return {"ok": True, "empresas": len(sistema.empresas),
            "eventos": len(sistema.barramento.historico)}


@app.get("/api/pilares")
def listar_pilares() -> list[dict]:
    from oceo.dominio import DEPENDENCIAS
    return [{"codigo": p.value, "nome": p.nome,
             "depende_de": [d.value for d in DEPENDENCIAS[p]]} for p in Pilar]


@app.post("/api/empresas", status_code=201)
def cadastrar_empresa(entrada: EmpresaEntrada) -> dict:
    try:
        empresa = Empresa(cnpj=entrada.cnpj, razao_social=entrada.razao_social,
                          regime=entrada.regime, municipio=entrada.municipio,
                          uf=entrada.uf)
        sistema.cadastrar(empresa, set(entrada.pilares))
    except DependenciaFaltando as erro:
        raise HTTPException(409, str(erro))
    except ValueError as erro:
        raise HTTPException(422, str(erro))
    return sistema.painel(empresa.id)


@app.get("/api/empresas")
def listar_empresas() -> list[dict]:
    return [{"id": e.id, "cnpj": e.cnpj_formatado, "razao_social": e.razao_social,
             "pilares_ativos": sorted(p.value for p in sistema.assinaturas[e.id].pilares)}
            for e in sistema.empresas.values()]


@app.get("/api/empresas/{empresa_id}/painel")
def painel(empresa_id: str) -> dict:
    if empresa_id not in sistema.empresas:
        raise HTTPException(404, "Empresa não encontrada.")
    return sistema.painel(empresa_id)


@app.post("/api/empresas/{empresa_id}/pilares/{codigo}")
def ativar_pilar(empresa_id: str, codigo: Pilar) -> dict:
    if empresa_id not in sistema.empresas:
        raise HTTPException(404, "Empresa não encontrada.")
    try:
        sistema.assinatura_de(empresa_id).ativar(codigo)
    except DependenciaFaltando as erro:
        raise HTTPException(409, str(erro))
    return sistema.painel(empresa_id)


@app.delete("/api/empresas/{empresa_id}/pilares/{codigo}")
def desativar_pilar(empresa_id: str, codigo: Pilar) -> dict:
    if empresa_id not in sistema.empresas:
        raise HTTPException(404, "Empresa não encontrada.")
    caidos = sistema.assinatura_de(empresa_id).desativar(codigo)
    painel = sistema.painel(empresa_id)
    painel["desativados_em_cascata"] = sorted({p.value for p in caidos})
    return painel


@app.post("/api/empresas/{empresa_id}/eventos")
def publicar_evento(empresa_id: str, entrada: EventoEntrada) -> dict:
    if empresa_id not in sistema.empresas:
        raise HTTPException(404, "Empresa não encontrada.")
    try:
        sistema.anunciar(entrada.evento, empresa_id, entrada.origem, **entrada.dados)
    except PilarNaoContratado as erro:
        raise HTTPException(402, str(erro))
    return sistema.painel(empresa_id)


# ------------------------------------------------------------------ portal

@app.get("/")
def portal() -> FileResponse:
    return FileResponse(RAIZ / "portal" / "index.html")


if __name__ == "__main__":
    import uvicorn
    print("OCEO no ar em http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

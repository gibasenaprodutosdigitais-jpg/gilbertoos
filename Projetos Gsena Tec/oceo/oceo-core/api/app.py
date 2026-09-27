"""
A API do OCEO. É a única porta entre o mundo de fora e o núcleo.

Toda rota que toca dado de empresa passa por duas portas, nesta ordem:
  1. quem é você        -> usuario_logado
  2. você pode ver esta empresa? -> acesso.exigir_acesso

Subir:  python3 api/app.py      (ou: uvicorn api.app:app --reload)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response   # noqa: E402
from fastapi.responses import FileResponse                              # noqa: E402
from pydantic import BaseModel, Field                                   # noqa: E402

from oceo.acesso import (AcessoNegado, FalhaDeLogin, SenhaFraca,        # noqa: E402
                         Usuario)
from oceo.dominio import DEPENDENCIAS, Empresa, Evento, Pilar, Regime   # noqa: E402
from oceo.montagem import montar                                        # noqa: E402
from oceo.nucleo import DependenciaFaltando, PilarNaoContratado         # noqa: E402
from oceo.trilha import recibo                                          # noqa: E402

BANCO = os.environ.get("OCEO_BANCO", str(RAIZ / "dados" / "oceo.db"))
sistema, acesso = montar(BANCO)

app = FastAPI(title="OCEO", version="0.2.0",
              description="Núcleo de interligação dos cinco pilares.")


# ------------------------------------------------------------- porta 1: quem é

def usuario_logado(oceo_sessao: str | None = Cookie(default=None)) -> Usuario:
    try:
        return acesso.usuario_da_sessao(oceo_sessao)
    except FalhaDeLogin as erro:
        raise HTTPException(401, str(erro))


# ---------------------------------------------------- porta 2: pode ver isto?

def liberar(usuario: Usuario, empresa_id: str, escrita: bool = False) -> None:
    try:
        acesso.exigir_acesso(usuario, empresa_id, escrita=escrita)
    except AcessoNegado as erro:
        # 404 e não 403: não confirmamos sequer que a empresa existe
        raise HTTPException(404, str(erro))


# ------------------------------------------------------------------ modelos

class Credencial(BaseModel):
    email: str
    senha: str


class Cadastro(BaseModel):
    email: str
    nome: str
    senha: str


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


# -------------------------------------------------------------- sessão

@app.post("/api/conta", status_code=201)
def criar_conta(dados: Cadastro) -> dict:
    try:
        u = acesso.criar_usuario(dados.email, dados.nome, dados.senha)
    except SenhaFraca as erro:
        raise HTTPException(422, str(erro))
    except FalhaDeLogin:
        raise HTTPException(409, "Já existe uma conta com este e-mail.")
    return {"id": u.id, "email": u.email, "nome": u.nome}


@app.post("/api/entrar")
def entrar(cred: Credencial, resposta: Response) -> dict:
    try:
        token = acesso.entrar(cred.email, cred.senha)
    except FalhaDeLogin as erro:
        raise HTTPException(401, str(erro))
    resposta.set_cookie("oceo_sessao", token, httponly=True, samesite="lax", max_age=43200)
    u = acesso.usuario_da_sessao(token)
    return {"nome": u.nome, "email": u.email}


@app.post("/api/sair")
def sair(resposta: Response, oceo_sessao: str | None = Cookie(default=None)) -> dict:
    if oceo_sessao:
        acesso.sair(oceo_sessao)
    resposta.delete_cookie("oceo_sessao")
    return {"ok": True}


@app.get("/api/eu")
def eu(usuario: Usuario = Depends(usuario_logado)) -> dict:
    return {"nome": usuario.nome, "email": usuario.email,
            "empresas": len(acesso.empresas_de(usuario.id))}


# -------------------------------------------------------------- catálogo

@app.get("/api/saude")
def saude() -> dict:
    return {"ok": True, "banco": Path(BANCO).name}


@app.get("/api/pilares")
def listar_pilares() -> list[dict]:
    return [{"codigo": p.value, "nome": p.nome,
             "depende_de": [d.value for d in DEPENDENCIAS[p]]} for p in Pilar]


# -------------------------------------------------------------- empresas

@app.post("/api/empresas", status_code=201)
def cadastrar_empresa(entrada: EmpresaEntrada,
                      usuario: Usuario = Depends(usuario_logado)) -> dict:
    try:
        empresa = Empresa(cnpj=entrada.cnpj, razao_social=entrada.razao_social,
                          regime=entrada.regime, municipio=entrada.municipio,
                          uf=entrada.uf)
        if empresa.id in sistema.empresas:
            raise HTTPException(409, "Este CNPJ já está cadastrado.")
        sistema.cadastrar(empresa, set(entrada.pilares))
    except DependenciaFaltando as erro:
        raise HTTPException(409, str(erro))
    except ValueError as erro:
        raise HTTPException(422, str(erro))
    acesso.conceder(usuario.id, empresa.id, "dono")   # quem cadastra vira dono
    return sistema.painel(empresa.id)


@app.get("/api/empresas")
def listar_empresas(usuario: Usuario = Depends(usuario_logado)) -> list[dict]:
    meus = set(acesso.empresas_de(usuario.id))
    return [{"id": e.id, "cnpj": e.cnpj_formatado, "razao_social": e.razao_social,
             "papel": acesso.papel_em(usuario.id, e.id),
             "pilares_ativos": sorted(p.value for p in sistema.assinaturas[e.id].pilares)}
            for e in sistema.empresas.values() if e.id in meus]


@app.get("/api/empresas/{empresa_id}/painel")
def painel(empresa_id: str, usuario: Usuario = Depends(usuario_logado)) -> dict:
    liberar(usuario, empresa_id)
    if empresa_id not in sistema.empresas:
        raise HTTPException(404, "Empresa não encontrada.")
    dados = sistema.painel(empresa_id)
    dados["meu_papel"] = acesso.papel_em(usuario.id, empresa_id)
    return dados


@app.post("/api/empresas/{empresa_id}/pilares/{codigo}")
def ativar_pilar(empresa_id: str, codigo: Pilar,
                 usuario: Usuario = Depends(usuario_logado)) -> dict:
    liberar(usuario, empresa_id, escrita=True)
    try:
        sistema.assinatura_de(empresa_id).ativar(codigo)
    except DependenciaFaltando as erro:
        raise HTTPException(409, str(erro))
    sistema.salvar_assinatura(empresa_id)
    return painel(empresa_id, usuario)


@app.delete("/api/empresas/{empresa_id}/pilares/{codigo}")
def desativar_pilar(empresa_id: str, codigo: Pilar,
                    usuario: Usuario = Depends(usuario_logado)) -> dict:
    liberar(usuario, empresa_id, escrita=True)
    caidos = sistema.assinatura_de(empresa_id).desativar(codigo)
    sistema.salvar_assinatura(empresa_id)
    dados = painel(empresa_id, usuario)
    dados["desativados_em_cascata"] = sorted({p.value for p in caidos})
    return dados


@app.post("/api/empresas/{empresa_id}/eventos")
def publicar_evento(empresa_id: str, entrada: EventoEntrada,
                    usuario: Usuario = Depends(usuario_logado)) -> dict:
    liberar(usuario, empresa_id, escrita=True)
    try:
        sistema.anunciar(entrada.evento, empresa_id, entrada.origem, **entrada.dados)
    except PilarNaoContratado as erro:
        raise HTTPException(402, str(erro))
    return painel(empresa_id, usuario)


@app.get("/api/empresas/{empresa_id}/auditoria")
def auditoria(empresa_id: str, usuario: Usuario = Depends(usuario_logado)) -> list[dict]:
    """Trilha de tudo o que os pilares trocaram. Já nasce da persistência."""
    liberar(usuario, empresa_id)
    return [{"evento": f.evento.value, "origem": f.origem.value,
             "dados": f.dados, "em": f.em.isoformat(timespec="seconds")}
            for f in sistema.repo.listar_fatos(empresa_id)]


@app.get("/api/empresas/{empresa_id}/integridade")
def integridade(empresa_id: str, usuario: Usuario = Depends(usuario_logado)) -> dict:
    """
    Confere a trilha e devolve o comprovante. É o que prova ao cliente que
    ninguém alterou o histórico dele — nem nós.
    """
    liberar(usuario, empresa_id)
    return recibo(sistema.repo.conferir_trilha(), empresa_id)


# ------------------------------------------------------------------ portal

@app.get("/")
def portal() -> FileResponse:
    return FileResponse(RAIZ / "portal" / "index.html")


if __name__ == "__main__":
    import uvicorn
    print(f"OCEO no ar em http://127.0.0.1:8000   (banco: {BANCO})")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

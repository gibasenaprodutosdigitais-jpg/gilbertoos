"""
Trilha auditável: prova de que nenhum registro foi adulterado.

Esta é a parte da blockchain que serve ao OCEO — o encadeamento de hashes —
sem as partes que atrapalham (replicar dado de cliente em vários nós e
impedir a eliminação exigida pela LGPD).

Como funciona, em uma frase: cada fato guarda o resumo criptográfico do fato
anterior. Mudar qualquer registro antigo quebra a corrente a partir dali, e
a quebra aponta exatamente onde.

Dois usos práticos:
  1. Auditoria interna. Ninguém altera a base por fora sem deixar rastro —
     nem quem tem acesso ao banco.
  2. Prova para terceiro. O `hash_raiz` de um período é um número curto que
     resume tudo. Publicado em qualquer lugar com data confiável (cartório,
     e-mail, ou uma blockchain pública), prova depois que aqueles registros
     já existiam naquela data, sem expor nenhum dado do cliente.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime

GENESE = "0" * 64      # o elo anterior do primeiro registro


def resumir(evento: str, empresa_id: str, origem: str, dados: dict,
            em: str, hash_anterior: str) -> str:
    """
    SHA-256 do conteúdo do fato somado ao elo anterior.

    `sort_keys` é essencial: a mesma informação precisa gerar sempre o mesmo
    resumo, independentemente da ordem em que os campos aparecerem.
    """
    corpo = json.dumps(
        {"evento": evento, "empresa": empresa_id, "origem": origem,
         "dados": dados, "em": em, "anterior": hash_anterior},
        sort_keys=True, ensure_ascii=False, default=str, separators=(",", ":"),
    )
    return hashlib.sha256(corpo.encode("utf-8")).hexdigest()


@dataclass
class Conferencia:
    """Resultado da verificação da trilha."""
    integra: bool
    registros: int
    hash_raiz: str
    rompeu_em: int | None = None          # id do registro onde a corrente quebrou
    motivo: str = ""

    def __str__(self) -> str:
        if self.integra:
            return (f"Trilha íntegra: {self.registros} registro(s) conferido(s). "
                    f"Resumo do período: {self.hash_raiz[:16]}…")
        return (f"ADULTERAÇÃO DETECTADA no registro {self.rompeu_em}: {self.motivo}")


def conferir(linhas: list[dict]) -> Conferencia:
    """
    Refaz a conta de toda a corrente e compara com o que está gravado.

    `linhas` vem do banco em ordem cronológica, cada uma com: id, evento,
    empresa_id, origem, dados, em, hash, hash_anterior.
    """
    anterior = GENESE
    for linha in linhas:
        if linha["hash_anterior"] != anterior:
            return Conferencia(
                False, len(linhas), anterior, linha["id"],
                "o elo com o registro anterior não bate — registro removido ou reordenado",
            )
        esperado = resumir(linha["evento"], linha["empresa_id"], linha["origem"],
                           linha["dados"], linha["em"], linha["hash_anterior"])
        if esperado != linha["hash"]:
            return Conferencia(
                False, len(linhas), anterior, linha["id"],
                "o conteúdo do registro foi alterado depois de gravado",
            )
        anterior = linha["hash"]
    return Conferencia(True, len(linhas), anterior)


def recibo(conf: Conferencia, empresa_id: str) -> dict:
    """
    O comprovante que se entrega ao cliente ou ao auditor.

    Só o resumo sai daqui. Nenhum dado da empresa é exposto — é exatamente
    isso que permite publicar o recibo em lugar público, se um dia quiser
    ancorar a prova numa blockchain ou registrar em cartório.
    """
    dados = {
        "empresa": empresa_id,
        "registros_conferidos": conf.registros,
        "integra": conf.integra,
        "hash_raiz": conf.hash_raiz,
        "conferido_em": datetime.now().isoformat(timespec="seconds"),
        "algoritmo": "SHA-256 encadeado",
    }
    if conf.integra:
        dados["observacao"] = (
            "O hash_raiz resume todos os registros do período sem revelar "
            "nenhum deles. Guarde-o para provar, no futuro, que esta trilha "
            "não foi alterada."
        )
    else:
        # o auditor precisa saber onde olhar, não só que algo está errado
        dados["rompeu_no_registro"] = conf.rompeu_em
        dados["motivo"] = conf.motivo
        dados["observacao"] = (
            f"A corrente é válida até antes do registro {conf.rompeu_em}. "
            "Dali em diante o histórico não pode ser considerado confiável: "
            "compare com o último hash_raiz que você guardou."
        )
    return dados

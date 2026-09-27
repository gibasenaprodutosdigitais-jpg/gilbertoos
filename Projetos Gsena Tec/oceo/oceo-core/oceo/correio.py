"""
Saída de e-mail do OCEO.

Estado honesto: **o envio real ainda não está ligado.** Não há servidor de
e-mail configurado, e inventar um seria pior que não ter — daria a impressão
de que a recuperação de senha funciona ponta a ponta quando não funciona.

O que existe aqui é o contrato. Trocar o `EnviadorArquivo` por um que fale
com o serviço de e-mail escolhido é escrever uma classe com o mesmo método
`enviar`, sem encostar em nenhuma regra de segurança.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path


class Enviador:
    """Contrato. Quem envia e-mail no OCEO cumpre isto."""

    def enviar(self, para: str, assunto: str, corpo: str) -> None:
        raise NotImplementedError


class EnviadorArquivo(Enviador):
    """
    Grava a mensagem em arquivo, em vez de enviar. É o padrão enquanto não
    houver serviço de e-mail: permite testar o fluxo inteiro sem depender
    de rede e sem mandar mensagem para endereço de verdade por engano.
    """

    def __init__(self, pasta: str | Path = "dados/emails"):
        self.pasta = Path(pasta)

    def enviar(self, para: str, assunto: str, corpo: str) -> None:
        self.pasta.mkdir(parents=True, exist_ok=True)
        carimbo = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        arquivo = self.pasta / f"{carimbo}.txt"
        arquivo.write_text(
            f"Para: {para}\nAssunto: {assunto}\n\n{corpo}\n", encoding="utf-8")


class EnviadorSilencioso(Enviador):
    """Descarta a mensagem. Usado em teste."""

    def __init__(self) -> None:
        self.enviados: list[tuple[str, str, str]] = []

    def enviar(self, para: str, assunto: str, corpo: str) -> None:
        self.enviados.append((para, assunto, corpo))


def texto_recuperacao(nome: str, link: str, minutos: int) -> str:
    return (
        f"Olá, {nome}.\n\n"
        f"Alguém pediu a redefinição da senha da sua conta no OCEO.\n\n"
        f"Para escolher uma senha nova, acesse:\n{link}\n\n"
        f"Este link vale por {minutos} minutos e só pode ser usado uma vez.\n\n"
        f"Se não foi você que pediu, ignore esta mensagem — sua senha atual "
        f"continua valendo e ninguém teve acesso à sua conta.\n\n"
        f"OCEO. Simples. Mais completo."
    )

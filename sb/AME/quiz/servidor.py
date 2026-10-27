"""Servidor local do quiz da Imersão AME.

Mostra o quiz em http://localhost:5180 e anota cada resposta numa linha
de respostas.csv, nesta mesma pasta (abre no Excel ou no Numbers).

Rodar:  python3 servidor.py
Parar:  Ctrl+C
"""
import csv
import json
import os
import threading
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PASTA = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(PASTA, "site")
PLANILHA = os.path.join(PASTA, "respostas.csv")
PORTA = int(os.environ.get("PORTA", "5180"))

CAMPOS = ["enviado_em", "nome", "whatsapp", "instagram", "nicho",
          "faturamento", "dificuldade", "dificuldade_texto", "versao"]
trava = threading.Lock()


class Quiz(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=SITE, **k)

    def do_POST(self):
        if self.path != "/api/inscricao":
            self.send_error(404)
            return
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            if tamanho > 20000:
                raise ValueError("grande demais")
            dados = json.loads(self.rfile.read(tamanho) or b"{}")
            linha = {c: str(dados.get(c, ""))[:2000] for c in CAMPOS}
            linha["enviado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            if not linha["nome"].strip():
                raise ValueError("sem nome")
            with trava:
                novo = not os.path.exists(PLANILHA)
                # utf-8-sig: o Excel abre os acentos certos
                with open(PLANILHA, "a", newline="", encoding="utf-8-sig") as f:
                    w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
                    if novo:
                        w.writeheader()
                    w.writerow(linha)
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode())
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    print(f"Quiz da Imersão AME no ar: http://localhost:{PORTA}")
    print(f"Respostas em: {PLANILHA}")
    ThreadingHTTPServer(("127.0.0.1", PORTA), Quiz).serve_forever()

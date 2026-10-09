"""
Junta os capitulos escritos da parte do Gilberto num PDF so, na ordem do
plano, para analise. O miolo sai nas mesmas normas da editora.
"""
import io
import re
from pathlib import Path

from _formatador import ESTILO, limpar, partir

AQUI = Path(__file__).parent

# ordem do plano em a-parte-do-gilberto.md
ORDEM = [
    ("capitulos/07-do-zero-ao-grupo-sena.md", "Do zero ao Grupo Sena"),
    ("capitulos/06-o-diagnostico-do-executivo.md", "O diagnóstico do executivo"),
    ("capitulos/saude-fisica-da-empresa.md", "A saúde física da empresa"),
    ("capitulos/saude-mental-da-empresa.md", "A saúde mental da empresa"),
    ("capitulos/saude-espiritual-da-empresa.md", "A saúde espiritual da empresa"),
    ("capitulos/09-check-up-completo.md", "Check-up completo"),
]

FALTAM = [
    "Dois caminhos, a metade dele do capítulo 1",
    "As sete quedas",
    "O check-up que não foi feito, a metade dele do capítulo 4",
    "Recomeço, a metade dele do capítulo 8",
]


def inline(t):
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    return t


def corpo_html(blocos):
    out, lista = [], None
    for tipo, conteudo in blocos:
        if tipo in ("num", "item"):
            tag = "ol" if tipo == "num" else "ul"
            if lista != tag:
                if lista:
                    out.append(f"</{lista}>")
                out.append(f"<{tag}>")
                lista = tag
            out.append(f"<li>{inline(conteudo)}</li>")
            continue
        if lista:
            out.append(f"</{lista}>")
            lista = None
        if tipo == "h1":
            out.append(f"<h1>{inline(conteudo)}</h1>")
        elif tipo == "h2":
            out.append(f"<h2>{inline(conteudo)}</h2>")
        elif tipo == "h3":
            out.append(f"<h3>{inline(conteudo)}</h3>")
        elif tipo == "p":
            out.append(f"<p>{inline(conteudo)}</p>")
        elif tipo == "cita":
            out.append(f"<blockquote><p>{inline(conteudo)}</p></blockquote>")
        elif tipo == "tabela":
            linhas = [l for l in conteudo if not re.match(r"^\|[\s|:-]+\|$", l)]
            cels = [[c.strip() for c in l.strip("|").split("|")] for l in linhas]
            if not cels:
                continue
            out.append("<table>")
            for i, linha in enumerate(cels):
                tag = "th" if i == 0 else "td"
                out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in linha) + "</tr>")
            out.append("</table>")
    if lista:
        out.append(f"</{lista}>")
    return "".join(out)


partes, sumario = [], []
for caminho, nome in ORDEM:
    md = limpar(io.open(AQUI / caminho, encoding="utf-8").read())
    partes.append('<section class="cap">' + corpo_html(partir(md)) + "</section>")
    sumario.append(nome)

capa = f"""<section class="capa">
<h1 class="titulo">O Médico e o Executivo</h1>
<p class="sub">A parte do Gilberto Sena</p>
<p class="linha">Versão de trabalho para análise · 09/out/2026</p>
<p class="linha">Formatado nas normas da editora: Times New Roman 12,
espaçamento 1,5, margens 3/3/2/2, justificado, recuo de 1,25 cm.</p>
<h2 class="s">Neste caderno</h2>
<ol class="s">{''.join(f'<li>{n}</li>' for n in sumario)}</ol>
<h2 class="s">Ainda por escrever</h2>
<ul class="s">{''.join(f'<li>{n}</li>' for n in FALTAM)}</ul>
<p class="linha nota">As notas de redação de cada capítulo ficam de fora
deste caderno, nos arquivos de trabalho. Lá está o que é frase dele, o que
eu acrescentei e o que precisa da palavra dele.</p>
</section>"""

ESTILO_EXTRA = """
.cap{page-break-before:always}
.capa{text-align:left}
.capa .titulo{font-size:22pt;text-transform:none;margin:3cm 0 0.4cm}
.capa .sub{font-size:14pt;text-indent:0;margin-bottom:1.2cm}
.capa .linha{text-indent:0;font-size:11pt;margin-bottom:.5cm}
.capa .nota{margin-top:1.2cm;font-style:italic}
.capa h2.s{font-size:12pt;margin:1.2cm 0 .3cm}
.capa ol.s,.capa ul.s{margin-left:1.25cm}
"""

io.open(AQUI / "formatado" / "_caderno.html", "w", encoding="utf-8").write(
    f"""<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>O Médico e o Executivo — a parte do Gilberto</title>
<style>{ESTILO}{ESTILO_EXTRA}</style></head><body>
{capa}{''.join(partes)}
</body></html>"""
)
print("caderno montado com", len(ORDEM), "capitulos")

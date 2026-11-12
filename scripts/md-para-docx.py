"""Converte um .md simples (títulos, parágrafos, listas numeradas, citações e tabelas) em .docx editável.

Uso: python3 scripts/md-para-docx.py <entrada.md> [saida.docx]

Usa o textutil do macOS. Feito para os contratos e propostas de saidas/NEGOCIOS-E-MARCA/.
"""
import html
import os
import re
import subprocess
import sys
import tempfile


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)\*", r"<i>\1</i>", t)
    return re.sub(r"`(.+?)`", r"\1", t)


def tabela(linhas):
    linhas = [l for l in linhas if not re.match(r"^\|[\s\-|]+\|$", l)]
    h = '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse;width:100%;font-size:10pt">'
    for i, l in enumerate(linhas):
        tag = "th" if i == 0 else "td"
        celulas = [c.strip() for c in l.strip().strip("|").split("|")]
        h += "<tr>" + "".join(f'<{tag} valign="top" style="text-align:left">{inline(c)}</{tag}>' for c in celulas) + "</tr>"
    return h + "</table>"


def converter(md):
    out, lista, tab = [], None, []
    for linha in md.split("\n") + [""]:
        s = linha.strip()
        if s.startswith("|"):
            tab.append(s)
            continue
        if tab:
            out.append(tabela(tab))
            tab = []
        if lista and not re.match(r"^\d+\. ", s):
            out.append(f"</{lista}>")
            lista = None
        if not s:
            continue
        if s == "[[quebra]]":
            out.append('<div style="page-break-before:always"></div>')
            continue
        if s == "---":
            out.append("<hr>")
        elif s.startswith("# "):
            out.append(f'<h1 style="text-align:center">{inline(s[2:])}</h1>')
        elif s.startswith("### "):
            out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("## "):
            quebra = ' style="page-break-before:always"' if s[3:].startswith("Anexo") else ""
            out.append(f"<h2{quebra}>{inline(s[3:])}</h2>")
        elif s.startswith("> "):
            out.append(f'<p style="margin-left:20px"><i>{inline(s[2:])}</i></p>')
        elif re.match(r"^\d+\. ", s):
            if lista != "ol":
                out.append("<ol>")
                lista = "ol"
            out.append(f"<li>{inline(re.sub(r'^\d+\. ', '', s))}</li>")
        else:
            out.append(f"<p>{inline(s)}</p>")
    if lista:
        out.append(f"</{lista}>")
    return ('<html><head><meta charset="utf-8"></head>'
            '<body style="font-family:Arial;font-size:11pt;line-height:1.45">' + "\n".join(out) + "</body></html>")


if __name__ == "__main__":
    entrada = sys.argv[1]
    saida = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(entrada)[0] + ".docx"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(converter(open(entrada, encoding="utf-8").read()))
    subprocess.run(["textutil", "-convert", "docx", "-output", saida, f.name], check=True)
    os.unlink(f.name)
    print(saida)

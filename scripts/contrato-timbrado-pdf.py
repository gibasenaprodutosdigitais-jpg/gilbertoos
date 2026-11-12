"""Gera o PDF em papel timbrado de um contrato/proposta em .md (logo no topo, marca d'água no centro, rodapé com página).

Uso: python3 scripts/contrato-timbrado-pdf.py <entrada.md> <saida.pdf> <logo-cabecalho.png> <marca-dagua.png> "<rodapé>"

Par do contrato-timbrado.js (que faz o .docx). Criado em 12/nov/2026.
"""
import base64, html, importlib.util, os, subprocess, sys, tempfile

entrada, saida, logo, marca, rodape = sys.argv[1:6]
aqui = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("m", os.path.join(aqui, "md-para-docx.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
corpo = m.converter(open(entrada, encoding="utf-8").read())
corpo = corpo[corpo.index("<body"):]; corpo = corpo[corpo.index(">") + 1:corpo.rindex("</body>")]
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
css = """@page{size:A4;margin:42mm 22mm 25mm 22mm}
body{font-family:Georgia,serif;font-size:10.5pt;line-height:1.5;color:#1E2328;text-align:justify}
.wm{position:fixed;top:50%;left:50%;width:125mm;transform:translate(-50%,-50%);z-index:-1}
h1{text-align:center;font-size:16pt;margin:0 0 4mm}
h2{font-size:11pt;text-transform:uppercase;border-bottom:0.6pt solid #B9BDC2;padding-bottom:1mm;margin:7mm 0 3mm;page-break-after:avoid}
h3{font-size:11pt;margin:5mm 0 2mm;page-break-after:avoid}
table{border-collapse:collapse;width:100%;font-size:9pt;text-align:left;page-break-inside:avoid}
th{background:#F1F2F3} th,td{border:0.6pt solid #B9BDC2;padding:1.5mm 2mm;vertical-align:top}
hr{border:0;border-top:0.6pt solid #B9BDC2;margin:5mm 0} p{margin:0 0 2.5mm} li{margin-bottom:1mm}"""
d = tempfile.mkdtemp()
open(f"{d}/c.html", "w").write(f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><img class="wm" src="data:image/png;base64,{b64(marca)}">{corpo}</body></html>')
open(f"{d}/h.html", "w").write(f'<div style="width:100%;text-align:center;padding-top:6mm"><img src="data:image/png;base64,{b64(logo)}" style="height:22mm"><div style="margin:2mm 22mm 0;border-bottom:0.6pt solid #B9BDC2"></div></div>')
open(f"{d}/f.html", "w").write(f'<div style="width:100%;font-family:Georgia,serif;font-size:7.5pt;color:#6B7078;text-align:center;margin:0 22mm;border-top:0.6pt solid #B9BDC2;padding-top:1.5mm">{html.escape(rodape)}<br>Página <span class="pageNumber"></span> de <span class="totalPages"></span></div>')
env = dict(os.environ, NODE_PATH=os.path.join(aqui, "node_modules"))
subprocess.run(["node", os.path.join(aqui, "html-para-pdf-timbrado.js"), f"{d}/c.html", f"{d}/h.html", f"{d}/f.html", os.path.abspath(saida)], check=True, env=env)

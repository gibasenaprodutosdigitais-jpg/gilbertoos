"""
Transforma o termo-de-compromisso-sbs.md em PDF na identidade da SBS.

Não tem conversor de markdown instalado nesta máquina, e o documento usa um
punhado pequeno de marcações: título, parágrafo, tabela, lista, negrito,
itálico, código, citação e risco. Converter só isso é mais curto e mais
previsível que instalar biblioteca.
"""
import html
import io
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent
ENTRADA = AQUI / "termo-de-compromisso-sbs.md"
HTML_SAIDA = AQUI / "termo-de-compromisso-sbs.html"
PDF_SAIDA = AQUI / "SBS - Termo de Compromisso e NDA.pdf"


def inline(t: str) -> str:
    """negrito, itálico, código, risco e link — nessa ordem, pra não se comerem"""
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"~~([^~]+)~~", r"<s>\1</s>", t)
    return t


def converter(md: str) -> str:
    linhas = md.split("\n")
    out, i = [], 0
    lista_aberta = None

    def fecha_lista():
        nonlocal lista_aberta
        if lista_aberta:
            out.append(f"</{lista_aberta}>")
            lista_aberta = None

    while i < len(linhas):
        ln = linhas[i]
        cru = ln.rstrip()

        # tabela: cabeçalho, separador, corpo
        if cru.startswith("|") and i + 1 < len(linhas) and re.match(r"^\|[\s:|-]+\|$", linhas[i + 1].strip()):
            fecha_lista()
            cab = [c.strip() for c in cru.strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in cab) + "</tr></thead><tbody>")
            i += 2
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                cel = [c.strip() for c in linhas[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cel) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        if not cru.strip():
            fecha_lista()
            i += 1
            continue

        if re.match(r"^---+$", cru.strip()):
            fecha_lista()
            out.append('<hr>')
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", cru)
        if m:
            fecha_lista()
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
            continue

        if cru.startswith(">"):
            fecha_lista()
            bloco = []
            while i < len(linhas) and linhas[i].startswith(">"):
                bloco.append(linhas[i].lstrip("> ").rstrip())
                i += 1
            out.append(f"<blockquote>{inline(' '.join(bloco))}</blockquote>")
            continue

        m = re.match(r"^(\s*)[-*]\s+(.*)$", cru)
        if m:
            if lista_aberta != "ul":
                fecha_lista()
                out.append("<ul>")
                lista_aberta = "ul"
            texto = [m.group(2)]
            i += 1
            while i < len(linhas) and re.match(r"^\s{2,}\S", linhas[i]) and not re.match(r"^\s*[-*]\s", linhas[i]):
                texto.append(linhas[i].strip())
                i += 1
            out.append(f"<li>{inline(' '.join(texto))}</li>")
            continue

        m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", cru)
        if m:
            if lista_aberta != "ol":
                fecha_lista()
                # o HTML reinicia a contagem a cada <ol>; o markdown nao.
                # Carrego o numero de cada item pra lista sair igual ao original.
                out.append("<ol>")
                lista_aberta = "ol"
            numero = m.group(2)
            texto = [m.group(3)]
            i += 1
            while i < len(linhas) and re.match(r"^\s{3,}\S", linhas[i]) and not re.match(r"^\s*(\d+\.|[-*])\s", linhas[i]):
                texto.append(linhas[i].strip())
                i += 1
            out.append(f'<li value="{numero}">{inline(" ".join(texto))}</li>')
            continue

        fecha_lista()
        par = [cru.strip()]
        i += 1
        while i < len(linhas) and linhas[i].strip() and not re.match(
                r"^(\s*[-*]\s|\s*\d+\.\s|#{1,4}\s|>|\||---+$)", linhas[i]):
            par.append(linhas[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(par))}</p>")

    return "\n".join(out)


ESTILO = """
:root{ --grafite:#0C1A2E; --ouro:#C9A24B; --ouro-escuro:#8C7A4A;
       --tinta:#1A1A1A; --cinza:#5E5E5E; --linha:#DAD6CC; --claro:#F2F0EC; }
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#FFFFFF}
body{font-family:"Helvetica Neue",Arial,sans-serif;color:var(--tinta);
     font-size:11.5px;line-height:1.62}
.pagina{max-width:760px;margin:0 auto;padding:26px 4px;position:relative;z-index:1}
.capa{background:var(--grafite);color:var(--claro);padding:48px 44px 42px;
      text-align:center;margin-bottom:26px;position:relative}
.mono{display:block;height:58px;width:auto;margin:0 auto 18px}
.capa .marca{font-family:Georgia,serif;font-size:20px;letter-spacing:.2em;
             color:var(--ouro);margin-bottom:7px}
.capa .sub{font-size:8px;letter-spacing:.3em;text-transform:uppercase;color:#9FB0C4;
           padding-top:8px;border-top:1px solid #2A4062;display:inline-block;padding-left:14px;padding-right:14px}
.capa h1{font-family:Georgia,serif;font-size:30px;font-weight:400;margin:24px 0 6px}
.capa .quem{font-size:11px;color:#9FB0C4}
h1,h2,h3,h4{font-family:Georgia,serif;font-weight:400;line-height:1.25}
h2{font-size:19px;margin:28px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--linha);
   page-break-after:avoid}
h3{font-size:14.5px;margin:20px 0 7px;page-break-after:avoid}
h4{font-size:12.5px;margin:15px 0 5px;page-break-after:avoid}
p{margin:0 0 9px}
ul,ol{margin:0 0 11px 19px}
li{margin-bottom:3px}
b{color:#000}
code{font-family:Menlo,Consolas,monospace;font-size:10px;background:#F4F2EC;
     padding:1px 4px;color:#55502F}
s{color:#9A9A9A}
blockquote{border-left:3px solid var(--ouro);background:#FAF8F3;padding:11px 16px;
           margin:0 0 16px;font-size:10.8px;color:#3C3C3C}
blockquote b{color:var(--tinta)}
hr{border:0;border-top:1px solid var(--linha);margin:22px 0}
table{width:100%;border-collapse:collapse;margin:12px 0 16px;font-size:10.5px;
      page-break-inside:avoid}
th{background:var(--grafite);color:var(--claro);padding:7px 9px;text-align:left;
   font-size:8.5px;letter-spacing:.1em;text-transform:uppercase;font-weight:700}
td{border:1px solid var(--linha);padding:7px 9px;vertical-align:top}
tbody tr:nth-child(even) td{background:#FAF9F6}
.dagua{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
       width:560px;z-index:0;pointer-events:none}
/* position:fixed se repete em toda folha no PDF do Chromium. Conferi
   descomprimindo os fluxos: as 7 paginas desenham a imagem. */
.rodape{margin-top:26px;padding-top:9px;border-top:1px solid var(--linha);
        font-size:8.5px;color:#9A9A9A;text-align:center;letter-spacing:.04em}
"""

md = io.open(ENTRADA, encoding="utf-8").read()
# o título e a assinatura do topo viram capa; o resto segue como corpo
corpo = md.split("---", 1)[1] if md.startswith("# ") else md
corpo = converter(corpo.lstrip("\n-"))

pagina = f"""<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>Plano de Mentoria — Sena, Bittar e Simões</title><style>{ESTILO}</style></head><body>
<img class="dagua" src="../marca/sbs-marca-dagua.png" alt="">
<div class="pagina">
  <div class="capa">
    <img class="mono" src="../marca/sbs-logo.png" alt="">
    <div class="marca">SENA, BITTAR E SIMÕES</div>
    <div class="sub">Consultoria e assessoria médica empresarial</div>
    <h1>Termo de compromisso</h1>
    <div class="quem">Responsabilidades, parceria e confidencialidade &nbsp;·&nbsp; minuta 1, 06/out/2026</div>
  </div>
  {corpo}
  <div class="rodape">Sena, Bittar e Simões · Documento de trabalho dos sócios · Confidencial</div>
</div></body></html>"""

io.open(HTML_SAIDA, "w", encoding="utf-8").write(pagina)

io.open(AQUI / "_render_termo.js", "w", encoding="utf-8").write("""
const path=require('path'); const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.join(__dirname,'termo-de-compromisso-sbs.html'));
await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:path.join(__dirname,'SBS - Termo de Compromisso e NDA.pdf'),
  format:'A4',printBackground:true,
  margin:{top:'14mm',bottom:'14mm',left:'15mm',right:'15mm'}});
await b.close();console.log('PDF ok');})();
""")
print("HTML pronto:", HTML_SAIDA.name)

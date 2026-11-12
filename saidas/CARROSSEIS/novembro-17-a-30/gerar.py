"""Gera os 14 carrosséis de 17 a 30/nov a partir de textos.md (direção 3: Suíço, uma cor por tema).

Cada dia: pasta DD-slug/ com carrossel.html, legenda.md e instagram/slide-NN.png (render.js, Playwright).
Uso: python3 gerar.py   (depois: NODE_PATH=../../../scripts/node_modules node render.js)
"""
import base64, html, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = "/Users/gilbertosena/Desktop/GilbertoOS/identidade/logo-transparente-crop.png"

# dia: (slug, rótulo curto, fundo, tinta, acento, hashtags)
TEMAS = {
    17: ("o-ego-do-dono", "O EGO DO DONO", "#3A1F5D", "#F3EFE6", "#F2B84B",
         "#gestaoempresarial #lideranca #donodeempresa #mentalidade #empreendedorismo #gestao #negocios #empresario #autoconhecimento #gilbertosena"),
    18: ("pejotizacao", "PEJOTIZAÇÃO", "#9E2A1F", "#F6EEE6", "#F7D27A",
         "#pejotizacao #gestaodepessoas #trabalhista #donodeempresa #gestaoempresarial #contratacao #rh #empresario #riscotrabalhista #gilbertosena"),
    19: ("o-crepe-do-vizinho", "IMPULSO", "#B84F17", "#FFF4EA", "#22130A",
         "#empreendedorismo #planejamento #abrirempresa #pequenasempresas #gestaoempresarial #negocios #donodeempresa #pesquisademercado #empresario #gilbertosena"),
    20: ("a-conta-de-telefone", "AS CONTAS", "#12404D", "#EAF2F1", "#8FE3D6",
         "#reducaodecustos #gestaofinanceira #custos #donodeempresa #gestaoempresarial #auditoria #telecom #economia #empresario #gilbertosena"),
    21: ("a-diaria-de-6-mil", "O PREÇO", "#C08A2E", "#1B1408", "#6E1A10",
         "#precificacao #pontodeequilibrio #margem #gestaofinanceira #donodeempresa #vendas #negocios #empresario #lucro #gilbertosena"),
    22: ("faltou-contrato", "O CONTRATO", "#1F4A3A", "#F1EEE4", "#E9B949",
         "#contrato #gestaoempresarial #consultoria #negocios #donodeempresa #juridico #empresario #reestruturacao #gestao #gilbertosena"),
    23: ("saia-do-operacional", "OPERAÇÃO", "#252A33", "#EDEFF2", "#4FC3A1",
         "#gestaoempresarial #delegar #lideranca #donodeempresa #gestaodeequipes #processos #operacional #empresario #gestao #gilbertosena"),
    24: ("o-imposto-e-biblico", "O IMPOSTO", "#5B1A2A", "#F4ECE4", "#E8C07A",
         "#imposto #fluxodecaixa #gestaofinanceira #reformatributaria #donodeempresa #tributario #fe #empresario #gestaoempresarial #gilbertosena"),
    25: ("a-oportunidade-perdida", "OPORTUNIDADE", "#1E3FA0", "#F2F4FA", "#FFA98A",
         "#oportunidade #decisao #investimento #mentalidade #empreendedorismo #donodeempresa #negocios #empresario #alphaville #gilbertosena"),
    26: ("a-contratacao-comeca-antes", "CONTRATAÇÃO", "#4E5A1E", "#F4F2E6", "#F0B33F",
         "#contratacao #recrutamento #rh #gestaodepessoas #donodeempresa #gestaoempresarial #equipe #empresario #lideranca #gilbertosena"),
    27: ("a-culpa-e-do-empresario", "A CULPA", "#2B1414", "#F3E9E4", "#E2553A",
         "#gestaoempresarial #responsabilidade #conhecimento #donodeempresa #empresario #lideranca #negocios #empreendedorismo #mentoria #gilbertosena"),
    28: ("treinamento", "TREINAMENTO", "#0F5E66", "#EEF6F5", "#FFB547",
         "#treinamento #culturaorganizacional #gestaodepessoas #equipe #donodeempresa #lideranca #gestaoempresarial #empresario #desenvolvimento #gilbertosena"),
    29: ("vender-a-qualquer-custo", "PROPÓSITO", "#7A1E4E", "#F7ECF1", "#FFD166",
         "#proposito #vendas #qualidade #atendimento #varejo #donodeempresa #gestaoempresarial #lideranca #empresario #gilbertosena"),
    30: ("prosperar-aqui", "PROSPERAR", "#1E6B3A", "#F2F5EC", "#F5C542",
         "#empreendedorismo #brasil #prosperidade #donodeempresa #negocios #mentalidade #empresario #gestaoempresarial #pequenasempresas #gilbertosena"),
}
# o número grande das lâminas NÚMERO
NUMEROS = {20: "R$ 15 mil → R$ 3 mil", 22: "R$ 2 milhões → R$ 700 mil", 26: "10 → 6"}
# lâminas LISTA: (introdução, itens)
LISTAS = {
    19: ("Você não sabe se ele está:", ["apertado", "alavancado", "devendo pro banco", "vendendo o almoço pra pagar a janta"]),
    27: ("É de quem não:", ["toma postura", "busca conhecimento", "procura quem já passou pelo processo",
                            "contrata quem pode tirar a empresa do buraco"]),
}


def ler():
    txt = open(os.path.join(AQUI, "textos.md"), encoding="utf-8").read()
    dias = {}
    for bloco in re.split(r"\n## ", txt)[1:]:
        m = re.match(r"(\d\d)/11 — (.+?)(?: \(reel.*)?\n", bloco)
        if not m:
            continue
        dia = int(m.group(1))
        lam = []
        for l in bloco.splitlines()[1:]:
            mm = re.match(r"\d+\. (?:([A-ZÇÃÉÚ ]+) — )?(.+)", l.strip())
            if mm:
                lam.append(((mm.group(1) or "TEXTO").strip(), mm.group(2).strip()))
        dias[dia] = (m.group(2), lam)
    return dias


def e(s):
    # valores não quebram no meio: "R$ 6 mil", "2 milhões"
    s = re.sub(r"R\$ (\d)", "R$\u00a0\\1", s)
    s = re.sub(r"(\d) (mil|milhões)", "\\1\u00a0\\2", s)
    return html.escape(s)


def lamina(dia, i, n, tipo, texto, t):
    slug, rot, bg, ink, ac, _ = t
    fora = ""
    topo = (f'<div class="topo"><span>Nº {dia} · {e(rot)}</span><span>{i:02d}/{n:02d}</span></div>')
    if tipo == "CAPA":
        corpo = f'<div class="barra"></div><h1 class="capa fit">{e(texto)}</h1>'
        fora = '<div class="pe"><span>Gilberto Sena</span><span>arrasta →</span></div>'
    elif tipo == "DECLARAÇÃO":
        corpo = f'<p class="decl fit">{e(texto)}</p>'
    elif tipo == "NÚMERO":
        corpo = f'<div class="num">{e(NUMEROS[dia])}</div><p class="txt fit">{e(texto)}</p>'
    elif tipo == "CONTRASTE":
        a, b = texto.split(". ", 1)
        corpo = f'<p class="txt">{e(a)}.</p><div class="fio"></div><p class="txt forte">{e(b)}</p>'
    elif tipo == "LISTA":
        intro, itens = LISTAS[dia]
        li = "".join(f'<li><span class="idx">{k:02d}</span>{e(x)}</li>' for k, x in enumerate(itens, 1))
        corpo = f'<p class="txt">{e(intro)}</p><ul>{li}</ul>'
    elif tipo == "RESPIRO":
        corpo = f'<p class="respiro fit">{e(texto)}</p>'
    elif tipo == "O QUE FAZER":
        corpo = f'<div class="tag">O QUE FAZER</div><p class="txt fit">{e(texto)}</p>'
    elif tipo == "FINAL":
        corpo = f'<p class="final fit">{e(texto)}</p>'
        fora = ('<div class="assina"><div class="leao"></div><div><b>@gilbertosenaoficial</b><br>'
                'Gilberto Sena · Grupo Sena Soluções Empresariais</div></div>')
    else:
        corpo = f'<p class="txt fit">{e(texto)}</p>'
    return f'<div class="slide t-{tipo.lower().replace(" ", "-")}">{topo}<div class="miolo">{corpo}</div>{fora}</div>'


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#777}
.slide{width:1080px;height:1350px;background:var(--bg);color:var(--ink);font-family:'Helvetica Neue',Helvetica,sans-serif;
  position:relative;overflow:hidden;padding:96px 96px 110px;display:flex;flex-direction:column;margin-bottom:20px}
.topo{display:flex;justify-content:space-between;font-family:Menlo,monospace;font-size:26px;letter-spacing:.06em;opacity:.85}
.miolo{position:absolute;left:96px;right:96px;top:250px;bottom:150px;display:flex;flex-direction:column;justify-content:flex-start}
.barra{width:140px;height:18px;background:var(--ac);margin-bottom:56px}
h1.capa{font-weight:700;font-size:112px;line-height:1.02;letter-spacing:-.025em}
.pe{position:absolute;left:96px;right:96px;bottom:84px;display:flex;justify-content:space-between;font-family:Menlo,monospace;font-size:28px}
.txt{font-weight:500;font-size:62px;line-height:1.16;letter-spacing:-.01em}
.txt.forte{font-weight:700;color:var(--ac)}
.decl{font-weight:700;font-size:92px;line-height:1.05;letter-spacing:-.02em}
.num{font-weight:700;font-size:120px;line-height:1;color:var(--ac);letter-spacing:-.03em;margin-bottom:56px}
.fio{height:10px;width:100%;background:var(--ac);margin:56px 0}
ul{list-style:none;margin-top:40px}
li{font-weight:700;font-size:58px;line-height:1.12;padding:22px 0;border-top:3px solid var(--ink);display:flex;gap:28px}
li:last-child{border-bottom:3px solid var(--ink)}
.idx{font-family:Menlo,monospace;font-weight:500;font-size:30px;color:var(--ac);padding-top:14px;min-width:52px}
.t-respiro .miolo{justify-content:center}
.respiro{font-style:italic;font-weight:400;font-size:84px;line-height:1.12;color:var(--ac)}
.tag{display:inline-block;align-self:flex-start;background:var(--ac);color:var(--bg);font-family:Menlo,monospace;
  font-size:30px;letter-spacing:.12em;padding:14px 22px;margin-bottom:56px}
.final{font-weight:700;font-size:96px;line-height:1.04;letter-spacing:-.02em}
.assina{position:absolute;left:96px;right:96px;bottom:84px;display:flex;align-items:center;gap:28px;font-size:28px;line-height:1.4}
.assina b{font-family:Menlo,monospace;font-weight:500;font-size:30px;color:var(--ac)}
.leao{width:96px;height:85px;background:var(--ink);-webkit-mask:url(LOGO) center/contain no-repeat;mask:url(LOGO) center/contain no-repeat}
"""

FIT = """<script>
document.fonts.ready.then(()=>{document.querySelectorAll('.miolo').forEach(m=>{
 const f=m.querySelector('.fit'); if(!f) return; let s=parseFloat(getComputedStyle(f).fontSize);
 while(m.scrollHeight>m.clientHeight+2 && s>40){s-=2; f.style.fontSize=s+'px';}
}); document.body.dataset.pronto='1';});
</script>"""

RENDER = """const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  for (const pasta of process.argv.slice(2)) {
    const dir = path.join(__dirname, pasta), out = path.join(dir, 'instagram');
    fs.mkdirSync(out, { recursive: true });
    const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
    await page.goto('file://' + path.join(dir, 'carrossel.html'));
    await page.waitForSelector('body[data-pronto="1"]', { timeout: 20000 });
    const slides = await page.$$('.slide');
    for (let i = 0; i < slides.length; i++)
      await slides[i].screenshot({ path: path.join(out, `slide-${String(i + 1).padStart(2, '0')}.png`) });
    console.log(pasta, slides.length);
    await page.close();
  }
  await browser.close();
})();
"""


def legenda(titulo, lam, tags):
    textos = dict()
    for tipo, t in lam:
        textos.setdefault(tipo, t)
    capa = textos["CAPA"]
    meio = [t for tipo, t in lam if tipo not in ("CAPA", "FINAL", "O QUE FAZER", "NÚMERO", "LISTA")][:2]
    fazer = textos.get("O QUE FAZER", "")
    final = textos["FINAL"]
    partes = [capa, " ".join(meio), "O que fazer: " + fazer, "Arrasta pro lado e guarda.", final,
              "Gilberto Sena. Grupo Sena Soluções Empresariais.", tags]
    return "\n\n".join(p for p in partes if p)


def main():
    dias = ler()
    open(os.path.join(AQUI, "render.js"), "w").write(RENDER)
    pastas = []
    for dia, (titulo, lam) in sorted(dias.items()):
        t = TEMAS[dia]
        slug, rot, bg, ink, ac, tags = t
        pasta = f"{dia}-{slug}"
        os.makedirs(os.path.join(AQUI, pasta), exist_ok=True)
        css = CSS.replace("LOGO", "data:image/png;base64," + base64.b64encode(open(LOGO, "rb").read()).decode())
        sl = "".join(lamina(dia, i, len(lam), tipo, txt, t) for i, (tipo, txt) in enumerate(lam, 1))
        doc = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>:root{{--bg:{bg};--ink:{ink};--ac:{ac}}}'
               f'{css}</style></head><body>{sl}{FIT}</body></html>')
        open(os.path.join(AQUI, pasta, "carrossel.html"), "w", encoding="utf-8").write(doc)
        open(os.path.join(AQUI, pasta, "legenda.md"), "w", encoding="utf-8").write(legenda(titulo, lam, tags) + "\n")
        pastas.append(pasta)
    print(" ".join(pastas))


if __name__ == "__main__":
    main()

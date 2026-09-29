# -*- coding: utf-8 -*-
"""
Gera os dois PDFs do inventario a partir de UMA fonte de dados.

Fonte: "Inventario Gilberto - Republica -SP.pdf", enviado pelo Gilberto em
29/09/2026. Substitui a lista de 24/09/2026 ("Mini Inventario para Praca
Rebublica.pdf"), que tinha 57 linhas. Na origem, o numero vem ANTES do item
(coluna "Q" = quantidade). Grafia normalizada aqui (Parled's -> Par LED,
caisses -> cases, foros -> forros, Bias -> baias, escrivanias -> escrivaninhas).

Saidas:
  Inventario para Parceria.pdf                       (completo, com campos e assinaturas)
  Inventario para Parceria - Itens e Quantidades.pdf  (resumido)
  Check-list do Inventario.pdf                        (caixinha pra ticar item por item)
  anexo-i.md                                          (trecho pra colar na minuta)
"""
import json, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).parent

# (categoria, [(quantidade, item, observacao)])
# quantidade None = lote / a contar
INVENTARIO = [
    ("Painel de LED e projeção", [
        (12, "Placas de painel de LED", ""),
        (2,  "Cases para painel de LED", ""),
        (12, "Cabos de sinal", "do painel"),
        (12, "Cabos de energia", "do painel"),
        (1,  "Suporte de fixação do painel de LED", ""),
        (1,  "Computador do telão", "CPU"),
        (2,  "TVs de retorno", ""),
        (1,  "Tela interativa", ""),
        (1,  "Suporte para tela interativa", ""),
    ]),
    ("Captação de vídeo", [
        (3, "Câmeras do auditório", ""),
        (3, "Suportes tripé para câmeras", ""),
        (3, "Placas de captura de vídeo", ""),
        (3, "Cabos HDMI longos", ""),
        (2, "Cabos HDMI do palco", ""),
    ]),
    ("Áudio", [
        (1, "Caixa JBL PA", "com tripé"),
        (1, "Caixa JBL menor", ""),
        (1, "Caixa subwoofer Frahm", ""),
        (1, "Mesa de som Soundcraft UI16", ""),
        (1, "Mesa de som NXA MSX Player", ""),
        (3, "Microfones bastão", ""),
        (1, "Base EW135G4 Sennheiser", ""),
        (6, "Cabos longos de áudio", ""),
        (6, "Cabos de energia", "ligação dos áudios"),
    ]),
    ("Iluminação", [
        (12, "Luzes Par LED", ""),
        (4,  "Luzes COB ST-MN200BFQ", ""),
        (1,  "Mesa de iluminação", ""),
    ]),
    ("Informática e acessórios", [
        (2, "Notebooks", ""),
        (3, "Teclados", ""),
        (2, "Mouses", ""),
        (3, "Passadores de slides", ""),
        (4, "Baterias AA recarregáveis", "com carregador"),
        (1, "Transformador 220V para 127V", ""),
        (None, "Cabos HDMI avulsos", "lote"),
        (None, "Cabos e cabos de energia avulsos", "lote"),
    ]),
    ("Auditório", [
        (20,  "Mesas de auditório", ""),
        (20,  "Forros de mesa de auditório", ""),
        (120, "Cadeiras de auditório", ""),
        (3,   "Palcos", ""),
    ]),
    ("Mobiliário de escritório", [
        (1,  "Sofá preto", "dois lugares"),
        (1,  "Mesa de reunião retangular", ""),
        (6,  "Cadeiras", "da mesa de reunião"),
        (10, "Cadeiras brancas com rodas", ""),
        (5,  "Cadeiras pretas com rodas", ""),
        (2,  "Jogos de bistrô", "com 8 cadeiras no total"),
        (8,  "Cadeiras de bistrô", "dos jogos acima"),
        (1,  "Mesa em L", "para house"),
        (4,  "Mesas com pufes", ""),
        (16, "Pufes", "das mesas acima"),
        (2,  "Mesas pretas retangulares com rodas", ""),
        (1,  "Móvel aparador", ""),
        (5,  "Escrivaninhas", ""),
        (2,  "Armários marrons", ""),
        (2,  "Baias de atendimento duplas", ""),
        (7,  "Armários médios", ""),
        (1,  "Armário grande", ""),
        (7,  "Armários arquivo", ""),
        (1,  "Mesa redonda", ""),
        (1,  "Mesa média retangular", ""),
        (1,  "Mesa grande oval cinza jumbo", ""),
        (1,  "Mesa de escritório com escrivaninha", ""),
        (1,  "Armário preto com 6 portas", ""),
        (1,  "Aparador", ""),
        (1,  "Cadeira com rodas", ""),
    ]),
    ("Cortinas", [
        (8, "Bastões de cortina", ""),
        (9, "Cortinas", ""),
    ]),
    ("Eletrodomésticos", [
        (1, "Geladeira", ""),
        (1, "Geladeira de duas portas", ""),
        (1, "Purificador IBBL Vivax", ""),
    ]),
]

total_pecas = sum(q for _, itens in INVENTARIO for q, _, _ in itens if q)
total_linhas = sum(len(itens) for _, itens in INVENTARIO)
lotes = sum(1 for _, itens in INVENTARIO for q, _, _ in itens if q is None)

CSS_BASE = """
  :root{ --papel:#F2F0EB; --tinta:#16161A; --acento:#D6412B;
         --linha:#C9C5BC; --fraco:#6E6A63; }
  *{margin:0; padding:0; box-sizing:border-box;}
  body{ font-family:'Archivo',sans-serif; color:var(--tinta); background:var(--papel);
        -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  header{ border-bottom:2.5pt solid var(--tinta); padding-bottom:7pt; margin-bottom:12pt; }
  .kicker{ font-size:7.5pt; font-weight:700; letter-spacing:.18em; text-transform:uppercase;
           color:var(--acento); margin-bottom:5pt; }
  h1{ font-weight:700; letter-spacing:-.02em; line-height:1.08; }
  .sub{ color:var(--fraco); margin-top:5pt; max-width:150mm; }
  h2{ font-weight:700; letter-spacing:.15em; text-transform:uppercase; }
  table{ width:100%; border-collapse:collapse; }
  tr, td, th{ page-break-inside:avoid; }
  thead{ display:table-header-group; }
  footer{ margin-top:14pt; padding-top:5pt; border-top:.7pt solid var(--linha);
          font-size:7pt; color:var(--fraco); display:flex; justify-content:space-between; }
"""

FONTES = ("<link rel='preconnect' href='https://fonts.googleapis.com'>"
          "<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
          "<link href='https://fonts.googleapis.com/css2?"
          "family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600"
          "&display=swap' rel='stylesheet'>")


def q_txt(q, obs):
    if q is not None:
        return str(q)
    return "lote" if "lote" in obs else "a contar"


# ----------------------------------------------------------------- completo
def html_completo():
    linhas = []
    n = 0
    for cat, itens in INVENTARIO:
        linhas.append(f'<tr class="cat"><td colspan="7">{cat}</td></tr>')
        for q, item, obs in itens:
            n += 1
            o = f' <span class="obs">({obs})</span>' if obs and "lote" not in obs else ""
            if obs and "lote" in obs and obs != "lote":
                o = f' <span class="obs">({obs.replace(" — lote", "")})</span>'
            linhas.append(
                f'<tr><td class="n">{n:02d}</td><td class="item">{item}{o}</td>'
                f'<td class="qtd">{q_txt(q, obs)}</td>'
                f'<td class="campo">&nbsp;</td><td class="campo">&nbsp;</td>'
                f'<td class="campo">&nbsp;</td><td class="col-valor campo">&nbsp;</td></tr>')
    for extra in range(n + 1, n + 5):
        linhas.append(
            f'<tr class="vazia"><td class="n">{extra:02d}</td><td class="campo">&nbsp;</td>'
            f'<td class="campo">&nbsp;</td><td class="campo">&nbsp;</td>'
            f'<td class="campo">&nbsp;</td><td class="campo">&nbsp;</td>'
            f'<td class="col-valor campo">&nbsp;</td></tr>')

    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Inventário para Parceria</title>{FONTES}<style>
  @page {{ size:A4; margin:13mm 11mm; }}
  {CSS_BASE}
  body{{ font-size:8.5pt; line-height:1.4; }}
  h1{{ font-size:18pt; }} .sub{{ font-size:8pt; }}
  .partes{{ display:flex; gap:7pt; margin-bottom:10pt; }}
  .parte{{ flex:1; border:.7pt solid var(--linha); padding:6pt 7pt; }}
  .parte .rot{{ font-size:6.5pt; font-weight:700; letter-spacing:.13em;
    text-transform:uppercase; color:var(--acento); margin-bottom:3pt; }}
  .parte .nome{{ font-size:9pt; font-weight:700; }}
  .parte .det{{ font-size:7pt; color:var(--fraco); margin-top:2pt; line-height:1.3; }}
  .meta{{ display:flex; gap:7pt; margin-bottom:11pt; }}
  .meta div{{ flex:1; border-bottom:.7pt solid var(--linha); padding-bottom:3pt; }}
  .meta .r{{ font-size:6.5pt; font-weight:700; letter-spacing:.13em;
    text-transform:uppercase; color:var(--fraco); }}
  .meta .v{{ min-height:12pt; }}
  h2{{ font-size:7.5pt; margin:0 0 5pt; padding-bottom:3pt;
       border-bottom:1.2pt solid var(--tinta); }}
  thead th{{ font-size:6.3pt; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
    color:var(--fraco); text-align:left; padding:3pt; border-bottom:.7pt solid var(--linha); }}
  tbody td{{ padding:3.6pt 3pt; border-bottom:.5pt solid var(--linha); vertical-align:middle; }}
  tbody tr.cat td{{ background:rgba(22,22,26,.055); font-weight:700; font-size:7pt;
    letter-spacing:.1em; text-transform:uppercase; padding:3.5pt 3pt;
    border-bottom:.7pt solid var(--linha); }}
  tbody tr.vazia td{{ height:18pt; }}
  .n{{ width:7mm; font-family:'IBM Plex Mono',monospace; font-size:7.5pt; color:var(--fraco); }}
  .item{{ font-weight:500; font-size:8.5pt; }}
  .item .obs{{ color:var(--fraco); font-weight:400; font-size:7pt; }}
  .qtd{{ width:12mm; text-align:center; font-family:'IBM Plex Mono',monospace;
         font-weight:600; font-size:8.5pt; }}
  .campo{{ border-bottom:.5pt solid var(--linha); }}
  th:nth-child(4),td:nth-child(4){{ width:31mm; }}
  th:nth-child(5),td:nth-child(5){{ width:27mm; }}
  th:nth-child(6),td:nth-child(6){{ width:18mm; }}
  .col-valor{{ width:24mm; }}
  .total{{ display:flex; justify-content:flex-end; gap:10pt; align-items:baseline;
    margin-top:7pt; padding-top:6pt; border-top:2pt solid var(--tinta); }}
  .total .r{{ font-size:7pt; font-weight:700; letter-spacing:.13em; text-transform:uppercase; }}
  .total .v{{ font-family:'IBM Plex Mono',monospace; font-size:10pt; min-width:42mm;
    text-align:right; border-bottom:.7pt solid var(--linha); }}
  .decl{{ margin-top:11pt; border-left:2.5pt solid var(--acento); padding:6pt 0 6pt 9pt;
    font-size:7.5pt; line-height:1.45; max-width:168mm; }}
  .assin{{ display:flex; gap:14pt; margin-top:16pt; }}
  .assin div{{ flex:1; text-align:center; }}
  .assin .linha{{ border-top:.7pt solid var(--tinta); margin-bottom:3pt; }}
  .assin .q{{ font-size:7pt; font-weight:700; }}
  .assin .p{{ font-size:6.5pt; color:var(--fraco); }}
</style></head><body>
<header>
  <div class="kicker">Anexo I · Contrato de Parceria Comercial</div>
  <h1>Inventário de equipamentos e mobiliário</h1>
  <div class="sub">Espaço de eventos <strong>"Kairós"</strong> (denominação provisória)
    — Praça da República. Relação a ser conferida item a item na apuração física,
    preenchendo marca, número de série, estado e valor de reposição.</div>
</header>
<div class="partes">
  <div class="parte"><div class="rot">Proprietário dos bens</div>
    <div class="nome">Gilberto Luis de Sena</div>
    <div class="det">CPF 850.812.306-00 — aporta os bens em comodato, mantendo a
      propriedade exclusiva, nos termos da Cláusula 5 do contrato.</div></div>
  <div class="parte"><div class="rot">Depositário dos bens</div>
    <div class="nome">______________________________</div>
    <div class="det">CPF ______________________ — responde pela guarda e conservação
      enquanto os bens permanecerem no espaço.</div></div>
</div>
<div class="meta">
  <div><div class="r">Local da apuração</div><div class="v">&nbsp;</div></div>
  <div><div class="r">Data</div><div class="v">&nbsp;</div></div>
  <div><div class="r">Registro fotográfico</div><div class="v">&nbsp;</div></div>
</div>
<h2>Relação de bens</h2>
<table><thead><tr>
  <th class="n">#</th><th>Item</th><th class="qtd">Qtd.</th>
  <th>Marca / modelo</th><th>Nº de série</th><th>Estado</th>
  <th class="col-valor">Valor de reposição</th>
</tr></thead><tbody>{''.join(linhas)}</tbody></table>
<div class="total"><div class="r">Valor total de reposição</div><div class="v">&nbsp;</div></div>
<div class="decl">
  Os signatários declaram que os bens acima foram conferidos item a item nesta data.
  Os bens são de <b>propriedade exclusiva de Gilberto Luis de Sena</b>, permanecem assim
  em qualquer cenário e <b>não se comunicam com o imóvel</b> por acessão, benfeitoria ou
  qualquer outro título, ainda que fixados ou instalados em caráter permanente. O
  depositário responde pela guarda e conservação enquanto os bens permanecerem no espaço
  e obriga-se a comunicar em até 24 horas qualquer dano, furto, sinistro ou apreensão.
  Este inventário, uma vez assinado, <b>substitui o Anexo I</b> e integra o Contrato de
  Parceria Comercial para todos os fins.
</div>
<div class="assin">
  <div><div class="linha"></div><div class="q">GILBERTO LUIS DE SENA</div>
    <div class="p">Proprietário dos bens — CPF 850.812.306-00</div></div>
  <div><div class="linha"></div><div class="q">DEPOSITÁRIO</div>
    <div class="p">Nome e CPF</div></div>
</div>
<div class="assin" style="margin-top:12pt">
  <div><div class="linha"></div><div class="q">TESTEMUNHA 1</div><div class="p">Nome e CPF</div></div>
  <div><div class="linha"></div><div class="q">TESTEMUNHA 2</div><div class="p">Nome e CPF</div></div>
</div>
<footer><span>Anexo I — Contrato de Parceria Comercial · Espaço de eventos "Kairós"</span>
<span>{total_linhas} itens · {total_pecas} peças</span></footer>
</body></html>"""


# ----------------------------------------------------------------- resumido
def html_resumo():
    blocos = []
    for cat, itens in INVENTARIO:
        linhas = []
        for q, item, obs in itens:
            o = f' <span class="obs">({obs.replace(" — lote", "")})</span>' if obs else ""
            cls = "qtd" if q is not None else "qtd aberto"
            linhas.append(f'<tr><td class="item">{item}{o}</td>'
                          f'<td class="{cls}">{q_txt(q, obs)}</td></tr>')
        # bloco inteiro (título + tabela) não pode partir entre colunas
        blocos.append(f'<section><h2>{cat}</h2>'
                      f'<table><tbody>{"".join(linhas)}</tbody></table></section>')

    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Inventário para Parceria — Itens e Quantidades</title>{FONTES}<style>
  @page {{ size:A4; margin:15mm 14mm; }}
  {CSS_BASE}
  body{{ font-size:8.5pt; line-height:1.35; }}
  h1{{ font-size:20pt; }} .sub{{ font-size:8.5pt; }}
  /* duas colunas: 57 itens cabem numa folha só sem apertar a leitura */
  .colunas{{ column-count:2; column-gap:9mm; }}
  section{{ break-inside:avoid; page-break-inside:avoid; margin-bottom:7pt; }}
  h2{{ font-size:7.5pt; color:var(--acento); margin:0 0 3pt; }}
  tbody td{{ padding:3.2pt 2pt; border-bottom:.5pt solid var(--linha); vertical-align:baseline; }}
  .item{{ font-size:9pt; font-weight:500; }}
  .item .obs{{ color:var(--fraco); font-weight:400; font-size:7pt; }}
  .qtd{{ width:16mm; text-align:right; font-family:'IBM Plex Mono',monospace;
         font-size:10pt; font-weight:600; }}
  .qtd.aberto{{ color:var(--fraco); font-weight:400; font-size:8pt; }}
  .totais{{ margin-top:14pt; border-top:2.5pt solid var(--tinta); padding-top:9pt;
    display:flex; gap:9mm; }}
  .totais div{{ flex:1; }}
  .totais .r{{ font-size:7pt; font-weight:700; letter-spacing:.14em;
    text-transform:uppercase; color:var(--fraco); margin-bottom:2pt; }}
  .totais .v{{ font-family:'IBM Plex Mono',monospace; font-size:15pt; font-weight:600; }}
  .totais .v small{{ font-family:'Archivo',sans-serif; font-size:8pt; font-weight:400;
    color:var(--fraco); }}
  .nota{{ margin-top:13pt; border-left:2.5pt solid var(--acento); padding:5pt 0 5pt 9pt;
    font-size:8pt; line-height:1.45; color:var(--fraco); max-width:168mm; }}
</style></head><body>
<header>
  <div class="kicker">Parceria · Espaço de eventos "Kairós" — Praça da República</div>
  <h1>Itens e quantidades</h1>
  <div class="sub">Relação dos equipamentos e do mobiliário aportados por
    Gilberto Luis de Sena.</div>
</header>
<div class="colunas">{''.join(blocos)}</div>
<div class="totais">
  <div><div class="r">Tipos de item</div><div class="v">{total_linhas}</div></div>
  <div><div class="r">Total de peças</div>
    <div class="v">{total_pecas} <small>unidades contadas</small></div></div>
  <div><div class="r">Lotes a detalhar</div>
    <div class="v">{lotes} <small>cabeamento avulso</small></div></div>
</div>
<div class="nota">
  Documento de referência, sem valor de conferência. A relação com marca, modelo,
  número de série, estado e valor de reposição — que é a que vale como Anexo I do
  contrato e como termo de depósito — está no documento
  <b>"Inventário para Parceria"</b>, assinado pelas partes e por duas testemunhas.
</div>
<footer><span>Parceria — Espaço de eventos "Kairós" · Itens e quantidades</span>
<span>Atualizar após a apuração física</span></footer>
</body></html>"""


# ----------------------------------------------------------------- anexo md
def html_checklist():
    """
    Check-list de conferencia: uma caixinha por item, pra ticar na entrega e
    outra na devolucao. O mesmo papel serve nas duas pontas do comodato, e e
    na devolucao que costuma faltar item.

    Duas paginas de proposito, com a quebra decidida aqui e nao pelo
    navegador: pagina 1 e a estrutura tecnica (o que quebra e o que some),
    pagina 2 e o mobiliario. Apertar os 68 itens numa folha so deixaria a
    linha fina demais pra ticar a mao, que e o unico uso deste papel.
    """
    def bloco_cat(cat, itens, contador):
        linhas = []
        for q, item, obs in itens:
            contador[0] += 1
            o = f' <span class="obs">({obs.replace(" — lote", "")})</span>' if obs else ""
            linhas.append(
                f'<tr><td class="cx"><span class="caixa"></span></td>'
                f'<td class="cx"><span class="caixa"></span></td>'
                f'<td class="qtd">{q_txt(q, obs)}</td>'
                f'<td class="item">{item}{o}</td></tr>')
        # bloco com muitos itens PRECISA poder fluir entre as colunas: Mobiliario
        # tem 25 linhas e, travado, jogava a folha inteira pra fora da pagina
        cls = ' class="longa"' if len(itens) > 14 else ""
        return (f'<section{cls}><h2>{cat}</h2>'
                f'<table><tbody>{"".join(linhas)}</tbody></table></section>')

    TECNICO = {"Painel de LED e projeção", "Captação de vídeo", "Áudio",
               "Iluminação", "Informática e acessórios", "Auditório"}
    cont = [0]
    p1 = "".join(bloco_cat(c, i, cont) for c, i in INVENTARIO if c in TECNICO)
    itens_p1 = cont[0]
    p2 = "".join(bloco_cat(c, i, cont) for c, i in INVENTARIO if c not in TECNICO)
    itens_p2 = cont[0] - itens_p1

    cabecalho = """<div class="rodape-cabecalho">
  <div><div class="r">Data da conferência</div><div class="linha"></div></div>
  <div><div class="r">Quem conferiu</div><div class="linha"></div></div>
  <div><div class="r">Local</div><div class="linha"></div></div>
</div>
<div class="legenda">
  <span><b>1ª caixa:</b> entrega</span>
  <span><b>2ª caixa:</b> devolução</span>
  <span><b>Qtd.:</b> quantidade que tem que estar lá</span>
</div>"""

    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Check-list do Inventário</title>{FONTES}<style>
  @page {{ size:A4; margin:12mm 12mm; }}
  {CSS_BASE}
  body{{ font-size:8.5pt; line-height:1.3; }}
  h1{{ font-size:19pt; }} .sub{{ font-size:8pt; }}
  .folha{{ page-break-after:always; }}
  .folha:last-child{{ page-break-after:auto; }}
  .legenda{{ display:flex; gap:7mm; margin:0 0 8pt; font-size:7.5pt; color:var(--fraco); }}
  .legenda b{{ color:var(--tinta); }}
  .colunas{{ column-count:2; column-gap:8mm; }}
  section{{ break-inside:avoid; page-break-inside:avoid; margin-bottom:7pt; }}
  section.longa{{ break-inside:auto; page-break-inside:auto; }}
  section.longa h2{{ break-after:avoid; }}
  h2{{ font-size:7.5pt; color:var(--acento); margin:0 0 3pt;
       border-bottom:.7pt solid var(--linha); padding-bottom:2pt; }}
  tbody td{{ padding:3pt 2pt; border-bottom:.4pt solid var(--linha);
             vertical-align:middle; }}
  td.cx{{ width:7mm; text-align:center; }}
  .caixa{{ display:inline-block; width:4mm; height:4mm;
           border:.9pt solid var(--tinta); }}
  .qtd{{ width:11mm; text-align:right; font-family:'IBM Plex Mono',monospace;
         font-size:9pt; font-weight:600; padding-right:3pt; }}
  .item{{ font-size:8.6pt; font-weight:500; }}
  .item .obs{{ color:var(--fraco); font-weight:400; font-size:7pt; }}
  .rodape-cabecalho{{ display:flex; gap:6pt; margin-bottom:8pt; }}
  .rodape-cabecalho div{{ flex:1; border:.7pt solid var(--linha); padding:5pt 6pt; }}
  .rodape-cabecalho .r{{ font-size:6.5pt; font-weight:700; letter-spacing:.14em;
    text-transform:uppercase; color:var(--fraco); }}
  .rodape-cabecalho .linha{{ border-bottom:.7pt solid var(--linha); height:12pt; }}
  .assina{{ margin-top:14pt; border-top:2.5pt solid var(--tinta); padding-top:12pt;
    display:flex; gap:9mm; }}
  .assina div{{ flex:1; }}
  .assina .risco{{ border-bottom:.9pt solid var(--tinta); height:22pt; }}
  .assina .r{{ font-size:7pt; color:var(--fraco); margin-top:4pt; }}
  .nota{{ margin-top:11pt; border-left:2.5pt solid var(--acento); padding:5pt 0 5pt 9pt;
    font-size:7.6pt; line-height:1.45; color:var(--fraco); }}
  .cont{{ font-size:7pt; color:var(--fraco); margin-top:5pt; }}
</style></head><body>

<div class="folha">
<header>
  <div class="kicker">Parceria · Espaço de eventos "Kairós" — Praça da República</div>
  <h1>Check-list do inventário <span style="font-size:10pt;color:var(--fraco)">· 1 de 2 · estrutura técnica e auditório</span></h1>
  <div class="sub">Confira item por item na <b>entrega</b> e de novo na
    <b>devolução</b>. O que não for ticado nas duas colunas é item a
    justificar, e a justificativa vale no mesmo dia.</div>
</header>
{cabecalho}
<div class="colunas">{p1}</div>
<div class="cont">Página 1 — {itens_p1} linhas de {total_linhas}.</div>
<footer><span>Check-list do inventário · Parceria "Kairós"</span>
<span>Página 1 de 2</span></footer>
</div>

<div class="folha">
<header>
  <div class="kicker">Parceria · Espaço de eventos "Kairós" — Praça da República</div>
  <h1>Check-list do inventário <span style="font-size:10pt;color:var(--fraco)">· 2 de 2 · auditório e mobiliário</span></h1>
</header>
<div class="colunas">{p2}</div>
<div class="cont">Página 2 — {itens_p2} linhas de {total_linhas}.</div>

<div class="assina">
  <div><div class="risco"></div><div class="r">Gilberto Luis de Sena — p. Espaço Kairós Ltda</div></div>
  <div><div class="risco"></div><div class="r">p. Motor em Ação Distribuição Ltda</div></div>
</div>

<div class="nota"><b>{total_linhas} linhas · {total_pecas} peças contadas · {lotes} lotes de
  cabeamento a detalhar.</b> Lote não tem quantidade fechada: conte e anote na
  hora, porque item sem número não se cobra depois. Divergência encontrada deve
  ser anotada no verso e assinada pelos dois no mesmo dia — conferência que fica
  pra semana seguinte não vale nada.</div>

<footer><span>Check-list do inventário · Parceria "Kairós"</span>
<span>Página 2 de 2 · {total_linhas} itens · {total_pecas} peças</span></footer>
</div>

</body></html>"""


def markdown_anexo():
    out = ["| # | Item | Qtd. | Marca/modelo | Nº de série | Estado | Valor de reposição |",
           "|---|---|---|---|---|---|---|"]
    n = 0
    for cat, itens in INVENTARIO:
        out.append(f"| | **{cat.upper()}** | | | | | |")
        for q, item, obs in itens:
            n += 1
            nome = f"{item}" + (f" ({obs.replace(' — lote', '')})" if obs else "")
            out.append(f"| {n} | {nome} | {q_txt(q, obs)} | `[ ]` | `[ ]` | `[ ]` | R$ `[ ]` |")
    out.append("")
    out.append(f"**{total_linhas} itens · {total_pecas} peças contadas · "
               f"{lotes} lotes de cabeamento a detalhar**")
    return "\n".join(out)


def atualizar_resumo_parceria():
    """O resumo de 1 pagina cita a contagem do inventario. Como a lista vai
    crescer, o numero e reescrito aqui, senao os dois documentos divergem —
    foi o que aconteceu com as 120 cadeiras."""
    import re
    alvo = AQUI / "resumo.html"
    if not alvo.exists():
        return
    s = alvo.read_text(encoding="utf-8")
    novo = f"Equipamentos e mobiliário: {total_linhas} itens, {total_pecas} peças (Anexo I)"
    s2 = re.sub(r"Equipamentos e mobiliário: \d+ itens, \d+ peças \(Anexo I\)", novo, s)
    if s2 != s:
        alvo.write_text(s2, encoding="utf-8")
        print(f"resumo.html atualizado -> {total_linhas} itens, {total_pecas} pecas")


if __name__ == "__main__":
    (AQUI / "inventario.html").write_text(html_completo(), encoding="utf-8")
    (AQUI / "inventario-resumo.html").write_text(html_resumo(), encoding="utf-8")
    (AQUI / "checklist.html").write_text(html_checklist(), encoding="utf-8")
    (AQUI / "anexo-i.md").write_text(markdown_anexo(), encoding="utf-8")
    atualizar_resumo_parceria()
    print(f"{total_linhas} itens | {total_pecas} pecas | {lotes} lotes")
    print("\nDepois de rodar, regerar os PDFs:")
    print('  inventario.html          -> "Inventario para Parceria.pdf"')
    print('  inventario-resumo.html   -> "Inventario para Parceria - Itens e Quantidades.pdf"')
    print('  checklist.html           -> "Check-list do Inventario.pdf"')
    print('  resumo.html              -> "Resumo da Parceria - 1 pagina.pdf"')

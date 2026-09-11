# -*- coding: utf-8 -*-
"""
OCEO — A Obra Completa : apresentacao em PowerPoint (16:9) com animacao.
A logo aparece animada (zoom + fade) em TODOS os slides; titulo e conteudo
entram em fade logo depois. Transicao de fade entre slides.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import nsdecls
from pptx.oxml import parse_xml

HERE = os.path.dirname(os.path.abspath(__file__))
IDV  = os.path.normpath(os.path.join(HERE, "..", "identidade-visual"))
LOGO_FULL = os.path.join(IDV, "LOGO-OCEO.png")
LOGO_MARK = os.path.join(IDV, "LOGO-OCEO-mark.png")
OUT = os.path.join(HERE, "OCEO - A Obra Completa (apresentacao).pptx")

# ---- paleta ----
PAPEL  = RGBColor(0xF4, 0xF1, 0xEA)
INK    = RGBColor(0x15, 0x15, 0x15)
BODY   = RGBColor(0x33, 0x35, 0x2F)
GOLD   = RGBColor(0xC9, 0xA2, 0x27)
DARK   = RGBColor(0x0F, 0x14, 0x19)
MUTE   = RGBColor(0x8A, 0x83, 0x74)
AZUL   = RGBColor(0x2C, 0x58, 0x96)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

SERIF = "Georgia"
SANS  = "Calibri"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

SW, SH = prs.slide_width, prs.slide_height

# mark: 769 x 698  -> ratio
MARK_RATIO = 698 / 769
FULL_RATIO = 998 / 1237


# ============================================================= helpers

def bg(slide, color):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    r.fill.solid(); r.fill.fore_color.rgb = color
    r.line.fill.background()
    r.shadow.inherit = False
    slide.shapes._spTree.remove(r._element)
    slide.shapes._spTree.insert(2, r._element)
    return r


def rect(slide, x, y, w, h, color, line=None):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    r.fill.solid(); r.fill.fore_color.rgb = color
    if line is None:
        r.line.fill.background()
    else:
        r.line.color.rgb = line; r.line.width = Pt(1)
    r.shadow.inherit = False
    return r


def tb(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    return box, tf


def setrun(p, text, size, color, font=SANS, bold=False, italic=False, spacing=None):
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.color.rgb = color
    r.font.name = font; r.font.bold = bold; r.font.italic = italic
    if spacing is not None:
        _set_spacing(r, spacing)
    return r


def _set_spacing(run, pts):
    rPr = run._r.get_or_add_rPr()
    rPr.set('spc', str(int(pts * 100)))


def kicker(tf, text):
    p = tf.paragraphs[0]
    setrun(p, text.upper(), 12, GOLD, SANS, bold=True, spacing=2.4)


def title(tf, text, size=34, color=INK):
    p = tf.add_paragraph()
    setrun(p, text, size, color, SERIF, bold=True)
    p.space_after = Pt(6)


def bullets(tf, items, size=16, color=BODY, gap=8):
    first = tf.paragraphs[0]
    used_first = bool(first.runs)
    for k, it in enumerate(items):
        if k == 0 and not used_first:
            p = first
        else:
            p = tf.add_paragraph()
        if isinstance(it, tuple):
            lead, rest = it
            setrun(p, lead, size, INK, SANS, bold=True)
            setrun(p, rest, size, color, SANS)
        else:
            setrun(p, "—  ", size, GOLD, SANS, bold=True)
            setrun(p, it, size, color, SANS)
        p.space_after = Pt(gap)
        p.line_spacing = 1.15


# ---------------------------------------------- ANIMACAO (timing XML)

class Ids:
    def __init__(self): self.n = 2  # 1=tmRoot, 2=mainSeq
    def nxt(self):
        self.n += 1
        return self.n


def _zoom_behaviors(ids, sid):
    a, b, c, d = ids.nxt(), ids.nxt(), ids.nxt(), ids.nxt()
    return f"""
      <p:set><p:cBhvr>
        <p:cTn id="{a}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
        <p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>
        <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
      </p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
      <p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base">
        <p:cTn id="{b}" dur="600" fill="hold"/>
        <p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>
        <p:attrNameLst><p:attrName>ppt_w</p:attrName></p:attrNameLst>
      </p:cBhvr><p:tavLst>
        <p:tav tm="0"><p:val><p:fltVal val="0.3"/></p:val></p:tav>
        <p:tav tm="100000"><p:val><p:fltVal val="1"/></p:val></p:tav>
      </p:tavLst></p:anim>
      <p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base">
        <p:cTn id="{c}" dur="600" fill="hold"/>
        <p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>
        <p:attrNameLst><p:attrName>ppt_h</p:attrName></p:attrNameLst>
      </p:cBhvr><p:tavLst>
        <p:tav tm="0"><p:val><p:fltVal val="0.3"/></p:val></p:tav>
        <p:tav tm="100000"><p:val><p:fltVal val="1"/></p:val></p:tav>
      </p:tavLst></p:anim>
      <p:animEffect transition="in" filter="fade"><p:cBhvr>
        <p:cTn id="{d}" dur="600"/>
        <p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>
      </p:cBhvr></p:animEffect>"""


def _fade_behaviors(ids, sid, dur=400):
    a, b = ids.nxt(), ids.nxt()
    return f"""
      <p:set><p:cBhvr>
        <p:cTn id="{a}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
        <p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>
        <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
      </p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
      <p:animEffect transition="in" filter="fade"><p:cBhvr>
        <p:cTn id="{b}" dur="{dur}"/>
        <p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>
      </p:cBhvr></p:animEffect>"""


def _effect_par(ids, preset, subtype, delay, behaviors):
    eid = ids.nxt()
    return f"""
    <p:par><p:cTn id="{eid}" presetID="{preset}" presetClass="entr" presetSubtype="{subtype}"
                  fill="hold" grpId="0" nodeType="afterEffect">
      <p:stCondLst><p:cond delay="{delay}"/></p:stCondLst>
      <p:childTnLst>{behaviors}</p:childTnLst>
    </p:cTn></p:par>"""


def animate(slide, sids, logo_sid=None):
    """logo (so na capa/fecho): zoom+fade @0 ; sids: fade em cascata."""
    ids = Ids()
    grp = ids.nxt()  # click-group cTn id
    pars = []
    delay = 0
    if logo_sid is not None:
        pars.append(_effect_par(ids, 23, 16, 0, _zoom_behaviors(ids, logo_sid)))
        delay = 350
    for sid in sids:
        pars.append(_effect_par(ids, 10, 0, delay, _fade_behaviors(ids, sid)))
        delay += 250
    xml = f"""<p:timing {nsdecls('p')}>
  <p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>
    <p:seq concurrent="1" nextAc="seek">
      <p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>
        <p:par><p:cTn id="{grp}" fill="hold" nodeType="afterEffect">
          <p:stCondLst><p:cond delay="0"/></p:stCondLst>
          <p:childTnLst>{''.join(pars)}</p:childTnLst>
        </p:cTn></p:par>
      </p:childTnLst></p:cTn>
      <p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
      <p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
    </p:seq>
  </p:childTnLst></p:cTn></p:par></p:tnLst>
</p:timing>"""
    slide._element.append(parse_xml(xml))


def add_transition(slide):
    xml = (f'<p:transition {nsdecls("p")} spd="med"><p:fade/></p:transition>')
    # inserir logo apos clrMapOvr (antes de timing)
    slide._element.append(parse_xml(xml))


# ---------------------------------------------- construtores de slide

def logo_mark(slide):
    w = Inches(1.15)
    h = Emu(int(w * MARK_RATIO))
    pic = slide.shapes.add_picture(LOGO_MARK, SW - w - Inches(0.55), Inches(0.5), w, h)
    return pic.shape_id


def content_slide(kick, ttl, body_builder, ttl_size=32):
    s = prs.slides.add_slide(BLANK)
    bg(s, PAPEL)
    # faixa lateral fina
    rect(s, 0, 0, Inches(0.16), SH, GOLD)
    # cabecalho
    hbox, htf = tb(s, Inches(0.9), Inches(0.62), Inches(9.7), Inches(1.7))
    kicker(htf, kick)
    title(htf, ttl, ttl_size)
    hsid = hbox.shape_id
    rect(s, Inches(0.92), Inches(2.15), Inches(2.2), Pt(3), GOLD)
    # corpo
    cbox, ctf = tb(s, Inches(0.92), Inches(2.5), Inches(11.3), Inches(4.5))
    body_builder(ctf)
    csid = cbox.shape_id
    add_transition(s)
    animate(s, [hsid, csid])
    return s


def divider_slide(code, ttl, sub):
    s = prs.slides.add_slide(BLANK)
    bg(s, DARK)
    rect(s, Inches(1.0), Inches(2.9), Inches(2.2), Pt(3), GOLD)
    box, tf = tb(s, Inches(0.98), Inches(3.15), Inches(11), Inches(2.4))
    p = tf.paragraphs[0]
    setrun(p, code, 15, GOLD, SANS, bold=True, spacing=3.0)
    p2 = tf.add_paragraph()
    setrun(p2, ttl, 44, WHITE, SERIF, bold=True)
    p2.space_before = Pt(6)
    p3 = tf.add_paragraph()
    setrun(p3, sub, 16, RGBColor(0xC9, 0xC4, 0xB8), SANS)
    p3.space_before = Pt(10)
    p3.line_spacing = 1.2
    tsid = box.shape_id
    add_transition(s)
    animate(s, [tsid])
    return s


def comparativo_slide(kick, ttl, rows, foot):
    s = prs.slides.add_slide(BLANK)
    bg(s, PAPEL)
    rect(s, 0, 0, Inches(0.16), SH, GOLD)
    hbox, htf = tb(s, Inches(0.9), Inches(0.58), Inches(9.7), Inches(1.3))
    kicker(htf, kick)
    title(htf, ttl, 28)
    hsid = hbox.shape_id
    rect(s, Inches(0.92), Inches(1.82), Inches(2.2), Pt(3), GOLD)

    n = len(rows)
    top = 2.02
    avail = 4.65 if n <= 8 else 4.25
    row_h = min(0.52, avail / n)
    fsize = 12.5 if n <= 8 else 10.5
    tbl_shape = s.shapes.add_table(n, 2, Inches(0.92), Inches(top),
                                   Inches(11.4), Inches(row_h * n))
    table = tbl_shape.table
    table.columns[0].width = Inches(7.7)
    table.columns[1].width = Inches(3.7)
    for i, (a, b) in enumerate(rows):
        table.rows[i].height = Inches(row_h)
        for j, txt in enumerate((a, b)):
            cell = table.cell(i, j)
            cell.fill.solid()
            is_tot = txt.startswith("»")
            cell.fill.fore_color.rgb = RGBColor(0xEF, 0xE9, 0xDA) if (i == 0 or is_tot) else PAPEL
            cell.margin_left = Inches(0.14); cell.margin_right = Inches(0.14)
            cell.margin_top = Inches(0.03); cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            para = cell.text_frame.paragraphs[0]
            para.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.RIGHT
            run = para.add_run(); run.text = txt.lstrip("» ").strip()
            run.font.name = SANS
            run.font.size = Pt(fsize if i else fsize - 0.5)
            strong = (i == 0) or is_tot
            run.font.bold = strong
            run.font.color.rgb = INK if strong else BODY
    tsid = tbl_shape.shape_id

    fbox, ftf = tb(s, Inches(0.92), Inches(top + row_h * n + 0.16),
                   Inches(11.4), Inches(1.0))
    for k, line in enumerate(foot):
        p = ftf.paragraphs[0] if k == 0 else ftf.add_paragraph()
        setrun(p, line, 10, MUTE, SANS)
        p.line_spacing = 1.1
    fsid = fbox.shape_id
    add_transition(s)
    animate(s, [hsid, tsid, fsid])
    return s


# ============================================================= SLIDES

# ---- 1 · CAPA
s = prs.slides.add_slide(BLANK)
bg(s, DARK)
w = Inches(4.2); h = Emu(int(w * FULL_RATIO))
pic = s.shapes.add_picture(LOGO_FULL, (SW - w) / 2, Inches(0.62), w, h)
lsid = pic.shape_id
box, tf = tb(s, Inches(1.5), Inches(4.62), Inches(10.3), Inches(2.6), MSO_ANCHOR.TOP)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
setrun(p, "REGISTRO DE OBRA LITERÁRIA", 13, GOLD, SANS, bold=True, spacing=3.0)
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
setrun(p2, "A Obra Completa", 40, WHITE, SERIF, bold=True)
p2.space_before = Pt(8)
p3 = tf.add_paragraph(); p3.alignment = PP_ALIGN.CENTER
setrun(p3, "Concepção, arquitetura e especificação dos cinco pilares", 16,
       RGBColor(0xC9, 0xC4, 0xB8), SANS)
p3.space_before = Pt(10)
p4 = tf.add_paragraph(); p4.alignment = PP_ALIGN.CENTER
setrun(p4, "Gilberto Luís de Sena  ·  Grupo Sena  ·  www.oceo.com.br", 12, MUTE, SANS)
p4.space_before = Pt(14)
tsid = box.shape_id
add_transition(s)
animate(s, [tsid], lsid)

# ---- 2 · Sobre esta obra
def _b(tf):
    bullets(tf, [
        "Reúne, num só corpo, todo o processo de concepção do OCEO — Sistema de Gestão Empresarial.",
        "Peça de referência para registro de direito autoral e documento-mestre do produto.",
        "Origem, princípios, arquitetura dos 5 pilares, cada módulo em detalhe, comparativos de custo e leitura de mercado.",
        "Nasce de mais de 12 anos de consultoria do Grupo Sena — não de uma tese abstrata.",
        "Disciplina: onde há projeção, o texto marca que é premissa a validar — não fato.",
    ])
content_slide("A obra", "Sobre esta apresentação", _b)

# ---- 3 · O que é o OCEO
def _b(tf):
    bullets(tf, [
        ("Um ERP para PME  ", "— contábil, fiscal, financeiro, folha e obrigações num fluxo único."),
        ("Uma camada de BI  ", "— balancete, extrato e nota viram painéis que o dono entende."),
        ("Um consultor multidisciplinar de plantão  ", "— ancorado no dado da própria empresa."),
        ("Um substituto econômico de estrutura  ", "— no lugar de cinco áreas contratadas, uma mensalidade."),
    ])
    p = tf.add_paragraph(); p.space_before = Pt(10)
    setrun(p, "“O sistema orienta. Você decide.”", 18, INK, SERIF, italic=True)
content_slide("Capítulo 1", "O que é o OCEO", _b)

# ---- 4 · O que o OCEO nao e
def _b(tf):
    bullets(tf, [
        "Não é um assistente genérico de IA — opera sobre o dado real, dentro de regras de especialistas.",
        "Não é um robô que decide — investir, contratar, demitir, assinar e distribuir lucro é sempre do dono.",
        "Não dispensa profissionais regulados — o contador com CRC e o advogado com OAB seguem no circuito.",
        "Não é um ERP de indústria pesada — o alvo é a empresa enxuta a partir de R$ 50 mil/mês.",
    ])
content_slide("Capítulo 1", "O que o OCEO não é", _b)

# ---- 5 · A origem
def _b(tf):
    bullets(tf, [
        "Mais de 12 anos de consultoria a PMEs: contábil, fiscal, jurídico, trabalhista e de negócios.",
        "Padrão em quase todo cliente que quebrou: não faltava faturamento, faltava leitura.",
        "O Grupo Sena resolvia caso a caso, com gente — funcionava, mas não escalava e custava caro.",
        ("Três ativos já prontos:  ", "método consolidado · prova de conceito em produção · profissionais regulados."),
        "O OCEO é a industrialização de uma consultoria que já funcionava.",
    ])
content_slide("Capítulo 2", "A origem — 12 anos antes da primeira linha de código", _b, 28)

# ---- 6 · O problema
def _b(tf):
    p = tf.paragraphs[0]
    setrun(p, "“A pequena empresa administra no escuro.”", 20, INK, SERIF, italic=True)
    p.space_after = Pt(12)
    bullets(tf, [
        "≈ 21,7 milhões de micro e pequenas empresas no Brasil — ≈ 30% do PIB (SEBRAE).",
        "≈ 29% fecham antes de 5 anos — causa principal: gestão financeira e falta de planejamento.",
        "O dono olha o saldo do banco, não o resultado. Confunde faturamento com lucro.",
    ])
content_slide("Capítulo 3", "O problema", _b)

# ---- 7 · 5 pontos cegos
def _b(tf):
    bullets(tf, [
        ("1 · Não sabe se sobra dinheiro  ", "— sem um DRE que entenda, a resposta é sensação, não número."),
        ("2 · É surpreendido pelo imposto  ", "— guia que vence sem provisão, regime errado por anos."),
        ("3 · Assina o que não leu  ", "— contrato sem ninguém revisar reajuste, multa, rescisão."),
        ("4 · Contrata marketing sem controle  ", "— agência que não presta conta, retorno não medido."),
        ("5 · Não planeja o passo seguinte  ", "— caixa parado perdendo para a inflação ou gasto por impulso."),
    ])
    p = tf.add_paragraph(); p.space_before = Pt(8)
    setrun(p, "Cada ponto cego = um pilar do OCEO.", 15, GOLD, SANS, bold=True)
content_slide("Capítulo 3", "Os cinco pontos cegos", _b)

# ---- 8 · A tese
def _b(tf):
    p = tf.paragraphs[0]
    setrun(p, "Um sistema. Cinco frentes. Uma mensalidade.", 26, INK, SERIF, bold=True)
    p.space_after = Pt(14)
    bullets(tf, [
        "O mesmo dado nas cinco frentes — o balancete que alimenta o painel também alimenta finanças e jurídico.",
        "Uma mensalidade, não cinco contratos. Uma língua — a do dono. Um responsável — o Grupo Sena.",
        ("Ciclo completo:  ", "medir · entender e decidir · proteger · crescer · fazer o excedente trabalhar."),
        ("Modelo:  ", "tecnologia faz o volume, o humano especialista faz o julgamento e a assinatura (“Services-as-Software”)."),
    ])
content_slide("Capítulo 4", "A tese", _b)

# ---- 9 · 5 principios
def _b(tf):
    bullets(tf, [
        ("1 · O sistema orienta, não decide  ", "— toda saída é consultiva; a ação é do empresário."),
        ("2 · Separar fato de premissa, sempre  ", "— fonte pública/dado real x projeção, sempre rotulados."),
        ("3 · A voz é do dono, não do técnico  ", "— balancete, DRE e cláusula traduzidos."),
        ("4 · Anti-genérico  ", "— dado da empresa + regras de quem tem 12 anos de estrada."),
        ("5 · Respeitar a fronteira regulatória  ", "— CRC, OAB, CVM, verba de mídia: sempre do lado de dentro."),
    ])
content_slide("Capítulo 5", "Os cinco princípios fundadores", _b)

# ---- 10 · Arquitetura (tabela)
s = prs.slides.add_slide(BLANK)
bg(s, PAPEL)
rect(s, 0, 0, Inches(0.16), SH, GOLD)
hbox, htf = tb(s, Inches(0.9), Inches(0.62), Inches(9.7), Inches(1.5))
kicker(htf, "Capítulo 7")
title(htf, "Os cinco pilares e seus códigos", 30)
hsid = hbox.shape_id
rect(s, Inches(0.92), Inches(2.05), Inches(2.2), Pt(3), GOLD)
rows = [
    ("Código", "Pilar", "Função no ciclo", "Substitui"),
    ("GC", "Contabilidade e BI", "Medir", "Escritório contábil interno + fiscal, DP, RH + BI"),
    ("GF", "Gestão Financeira", "Entender e decidir", "Analista / diretor financeiro; controladoria"),
    ("GJ", "Jurídico", "Proteger", "Advogado empresarial consultivo interno"),
    ("GM", "Marketing e Vendas", "Crescer", "Agência de marketing + comercial interno"),
    ("GI", "Educação Pré-Investimento", "Fazer o excedente trabalhar", "Analista de investimentos / educação"),
]
tsh = s.shapes.add_table(len(rows), 4, Inches(0.92), Inches(2.4), Inches(11.4), Inches(3.7))
t = tsh.table
t.columns[0].width = Inches(1.2); t.columns[1].width = Inches(3.1)
t.columns[2].width = Inches(2.7); t.columns[3].width = Inches(4.4)
for i, row in enumerate(rows):
    for j, txt in enumerate(row):
        c = t.cell(i, j)
        c.fill.solid()
        c.fill.fore_color.rgb = RGBColor(0xEF, 0xE9, 0xDA) if i == 0 else PAPEL
        c.margin_left = Inches(0.12); c.margin_right = Inches(0.1)
        c.margin_top = Inches(0.05); c.margin_bottom = Inches(0.05)
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        pr = c.text_frame.paragraphs[0]
        rn = pr.add_run(); rn.text = txt
        rn.font.name = SANS
        rn.font.size = Pt(12 if i else 11.5)
        rn.font.bold = (i == 0) or (j == 0)
        rn.font.color.rgb = INK if ((i == 0) or (j == 0)) else BODY
tsid = tsh.shape_id
add_transition(s)
animate(s, [hsid, tsid])

# ---- 11 · ciclo de dado
def _b(tf):
    bullets(tf, [
        ("Entrada (GC)  ", "— a nota é capturada, classificada e escriturada; vira balancete e base fiscal."),
        ("Leitura financeira (GF)  ", "— o mesmo lançamento entra no fluxo de caixa e ajusta o DRE do mês."),
        ("Radar jurídico (GJ)  ", "— o padrão de notas x contrato aponta divergência de preço e oportunidade tributária."),
        ("Contexto de marketing (GM)  ", "— vendas por produto e canal informam onde a mídia converte."),
        ("Gatilho de excedente (GI)  ", "— quando o resultado ultrapassa a reserva-alvo, o Pilar 5 é liberado."),
    ])
    p = tf.add_paragraph(); p.space_before = Pt(8)
    setrun(p, "A integração é do sistema — o dado nasce uma vez e chega pronto a cada frente.", 14, GOLD, SANS, bold=True)
content_slide("Capítulo 8", "O ciclo de dado único", _b, 30)

# ---- 12 · ativacao em cadeia
def _b(tf):
    bullets(tf, [
        ("1º · GC  ", "— imediato. É a fundação: sem dado organizado, nada funciona."),
        ("2º · GF  ", "— após o primeiro ciclo mensal fechado e a integração bancária ligada."),
        ("3º · GJ  ", "— em paralelo ao GF, depois de carregar os contratos-chave."),
        ("4º · GM  ", "— quando o cliente decide investir em crescimento (verba de mídia à parte)."),
        ("5º · GI  ", "— só com o fundo de reserva completo e caixa livre com margem. Nunca antes."),
    ])
content_slide("Capítulo 9", "Ativação em cadeia — a ordem importa", _b, 30)

# ---- 13 · tecnologia + humano
def _b(tf):
    bullets(tf, [
        "A tecnologia elimina o trabalho repetitivo: coletar, classificar, formatar, cruzar, redigir a 1ª versão.",
        "O humano mantém o julgamento e a responsabilidade.",
        ("GC  ", "contadores com CRC · GF  controller · GJ  advogado com OAB · GM  time de conteúdo/tráfego · GI  trilha educacional."),
        "É essa divisão que permite entregar resultado de consultoria a preço de assinatura.",
    ])
content_slide("Capítulo 10", "Tecnologia + humano", _b)

# ---- 14 · precificacao
def _b(tf):
    p = tf.paragraphs[0]
    setrun(p, "Setup R$ 12.500 (único)   +   Mensalidade R$ 3.500/mês (fixa)", 20, INK, SERIF, bold=True)
    p.space_after = Pt(12)
    bullets(tf, [
        ("Inclui  ", "— os 5 pilares, a camada de BI, o consultor do sistema, a manutenção por especialistas, a coordenação do todo."),
        ("Fora  ", "— honorário do contador externo (varia por regime), verba de mídia, WhatsApp acima da franquia, ato privativo de advogado."),
        ("Portugal  ", "— setup 2.950 € + 850 €/mês, comparativo no modelo local (14 meses + TSU 23,75%)."),
    ])
content_slide("Capítulo 11", "Precificação", _b)

# =================== PILAR 1
divider_slide("Parte III  ·  Código GC", "Contabilidade e Business Intelligence",
              "O pilar-fundação. Organiza contábil, fiscal, folha, obrigações e legalização — e transforma o dado em painéis. Único com prova de conceito em produção.")

def _b(tf):
    bullets(tf, [
        ("3 camadas  ", "— escritório contábil interno · contador externo permanece (CRC) · o dado interno é poder de barganha."),
        ("Contábil  ", "— captura e classificação, conciliação, balancete gerencial contínuo, NF em lote, receita contábil x financeira."),
        ("RH  ", "— descrição de vaga, triagem, roteiro de entrevista e análise comportamental, comparativo de candidatos."),
        ("DP  ", "— admissão, folha, encargos, férias, 13º, rescisão, eSocial/DCTFWeb com prazo no radar."),
        ("Fiscal  ", "— apuração do regime, guias e calendário, SPED/Reinf/DCTF, revisão de enquadramento, radar IBS/CBS."),
        ("Legalização  ", "— abertura, alterações, licenças e alvarás, certidões negativas, enquadramento de porte, baixa."),
    ])
content_slide("Capítulo 13–18  ·  Pilar 1 · GC", "Os cinco setores", _b, 30)

def _b(tf):
    bullets(tf, [
        "Já opera para um cliente real do Grupo Sena — rede com holding e ≈ 24 unidades.",
        "Volume de Compras · Pagamento a Fornecedores (balancete e financeiro) · Receita Contabilizada.",
        "Contabilização de NFs · DRE Financeiro · Sobra de Caixa por Unidade.",
        "Distribuição de Lucros por Unidade · Volume de Compras por Fornecedor (NF-e).",
        "Painéis 1–6 comprovam a camada Contábil; painel 6 conecta ao Pilar 2; painel 8, ao Pilar 5.",
    ])
    p = tf.add_paragraph(); p.space_before = Pt(6)
    setrun(p, "Não é promessa de dashboard — é o dashboard rodando há meses.", 14, GOLD, SANS, bold=True)
content_slide("Capítulo 19  ·  Pilar 1 · GC", "A prova de conceito — 9 painéis em produção", _b, 27)

comparativo_slide("Capítulo 20  ·  Pilar 1 · GC", "Comparativo de custo do Pilar 1", [
    ("Cargo interno equivalente", "Custo total /mês"),
    ("Analista Contábil", "R$ 9.871,16"),
    ("Analista Fiscal", "R$ 8.714,75"),
    ("Analista de Departamento Pessoal (premissa)", "R$ 5.940,00"),
    ("Agente de Recrutamento e Seleção", "R$ 6.308,48"),
    ("» Total da equipe interna", "» R$ 30.834,39"),
    ("» Economia mensal vs OCEO (mensalidade única)", "» R$ 27.334,39  (88,6%)"),
    ("» Payback do setup só com o Pilar 1", "» ≈ 14 dias"),
], ["Salários: piso de referência CAGED; encargos ≈ 80%. Premissa: 1 pessoa por cargo.",
    "A mensalidade de R$ 3.500 cobre os 5 pilares — atribuí-la só ao Pilar 1 é conservador contra o OCEO."])

def _b(tf):
    bullets(tf, [
        ("Quem já está  ", "— Conta Azul, Omie, Bling, Tiny e os sistemas dos próprios escritórios (Domínio, Fortes, Alterdata)."),
        ("1 · Leitura para o dono  ", "— os concorrentes entregam a máquina de apurar; o OCEO nasce da tradução."),
        ("2 · Contabilidade é camada, não o produto  ", "— vem integrada a finanças, jurídico, marketing e planejamento."),
        ("3 · Serviço embutido  ", "— não só a licença: a operação e o julgamento humano do Grupo Sena."),
        ("4 · Prova real  ", "— 9 painéis rodando há meses sobre operação com holding e 24 unidades."),
    ])
content_slide("Capítulo 21  ·  Pilar 1 · GC", "O Pilar 1 no mercado SaaS", _b, 30)

# =================== PILAR 2
divider_slide("Parte IV  ·  Código GF", "Gestão Financeira",
              "O pilar da decisão do dia a dia. Do dado do Pilar 1 + extrato bancário para leitura de caixa, DRE explicado, alertas, PF × PJ e o fundo de reserva.")

def _b(tf):
    bullets(tf, [
        ("Integração bancária  ", "— Open Finance, consolidação multibanco, saldo real x projetado, conciliação com o contábil."),
        ("Balanço e balancete traduzidos  ", "— o que a empresa tem, o que deve, o que sobra se liquidasse hoje."),
        ("DRE explicado  ", "— caixa livre, caixa circulante, margem de contribuição, EBITDA, ROI, valuation de referência."),
        "Cada linha traz o porquê importa: “vendeu mais e financiou o cliente com o seu dinheiro”.",
    ])
content_slide("Capítulo 22–25  ·  Pilar 2 · GF", "Leitura, decisão e planejamento", _b, 30)

def _b(tf):
    bullets(tf, [
        ("Alertas de consequência  ", "— “se nada mudar, dia 20 falta caixa para a folha”, não só o fato."),
        ("PF × PJ  ", "— centro de custos que mostra, sem julgamento, quanto saiu da empresa para a vida pessoal do sócio."),
        ("Fundo de reserva  ", "— alvo padrão: 3 meses de ponto de equilíbrio; recalculado com o custo fixo."),
        "Só quando a reserva está completa o Pilar 5 é liberado.",
    ])
content_slide("Capítulo 26  ·  Pilar 2 · GF", "Alertas, PF × PJ e reserva", _b, 30)

comparativo_slide("Capítulo 27  ·  Pilar 2 · GF", "Comparativo de custo do Pilar 2", [
    ("Cargo interno equivalente", "Custo total /mês  ·  Economia"),
    ("Analista Financeiro", "R$ 8.789,90   ·   60,2%"),
    ("Diretor Financeiro", "R$ 43.391,77   ·   91,9%"),
    ("» Leitura conservadora usada no comparativo central", "» Analista Financeiro"),
], ["Poucas PMEs contratam diretor financeiro dedicado — entra como referência do valor da entrega.",
    "Mesmo trocando só a execução de nível analista, a economia já é de 60,2%."])

# =================== PILAR 3
divider_slide("Parte V  ·  Código GJ", "Jurídico",
              "O advogado consultivo interno que a PME nunca teve à mão. Gera e analisa contratos, aponta risco e oportunidade legal — do lado de dentro da linha da OAB.")

def _b(tf):
    bullets(tf, [
        ("Gera minutas  ", "— serviço, fornecimento, locação, trabalho, parceria, NDA, societário, termos de uso/privacidade."),
        "Sai preenchida com os dados da empresa e cláusulas calibradas para o lado do cliente.",
        ("Analisa contratos recebidos  ", "— mapa de risco, incoerências e lacunas, tradução das cláusulas críticas, contraproposta."),
        ("Oportunidades  ", "— regime mais eficiente, créditos não aproveitados, benefícios setoriais, impacto IBS/CBS."),
        ("Consulta livre  ", "— “posso demitir por justa causa?”, ancorada no dado da própria empresa."),
    ])
content_slide("Capítulo 30–31  ·  Pilar 3 · GJ", "Gerar, analisar, orientar", _b, 30)

def _b(tf):
    bullets(tf, [
        ("Fronteira  ", "— Lei 8.906/1994: postulação e advocacia são privativas de inscrito na OAB."),
        ("Faz  ", "— minutas a partir de modelos de advogado, análise e tradução, informação sobre legislação, organização do dado."),
        ("Não faz  ", "— não postula em juízo, não emite parecer como peça assinada pelo sistema, não se apresenta como escritório."),
        ("Comparativo  ", "— Advogado Empresarial consultivo: R$ 16.122,33/mês → economia R$ 12.622,33 (78,3%)."),
        ("Mercado  ", "— 190+ legaltechs, R$ 700 mi aportados, 3 em 4 profissionais já usam IA — mas vendem para o escritório, não para o dono."),
    ])
content_slide("Capítulo 32–33  ·  Pilar 3 · GJ", "Fronteira da OAB · custo · mercado", _b, 28)

# =================== PILAR 4
divider_slide("Parte VI  ·  Código GM", "Marketing e Vendas",
              "A agência e o comercial por dentro do sistema. Conteúdo, tráfego pago com o cliente dono do gerenciador, e um agente de IA no primeiro atendimento do WhatsApp.")

def _b(tf):
    bullets(tf, [
        ("Conteúdo e social  ", "— linha editorial, calendário, posts, legendas, roteiros; leitura do que funcionou."),
        ("Tráfego pago  ", "— campanha em Meta e Google, custo por resultado, relatório em língua de dono."),
        ("Verba de mídia é do cliente  ", "— ele é dono do Business Manager e paga a plataforma direto."),
        ("Agente comercial de IA  ", "— WhatsApp Business Cloud API (~R$ 0,15/conversa, ~1.000 grátis/mês; ajuste da Meta em 01/out/2026)."),
        ("Assessoria externa  ", "— só para campanha específica de grande porte."),
    ])
content_slide("Capítulo 34–35  ·  Pilar 4 · GM", "A agência por dentro", _b, 29)

comparativo_slide("Capítulo 36  ·  Pilar 4 · GM", "Comparativo de custo do Pilar 4", [
    ("Cargo interno equivalente", "Custo total /mês"),
    ("Analista de Marketing", "R$ 8.755,79"),
    ("Gerente de Tráfego Pago", "R$ 10.981,26"),
    ("SDR / pré-vendas (premissa)", "R$ 6.300,00"),
    ("» Total da equipe interna", "» R$ 26.037,05"),
    ("» Economia mensal vs OCEO", "» R$ 22.537,05  (86,6%)"),
    ("» Payback do setup só com o Pilar 4", "» ≈ 17 dias"),
], ["Não inclui a verba de mídia (paga pelo cliente à plataforma) nem o WhatsApp acima da franquia (repassado).",
    "≈ 79% das empresas brasileiras usam o WhatsApp para falar com clientes."])

# =================== PILAR 5
divider_slide("Parte VII  ·  Código GI", "Educação Pré-Investimento",
              "O último pilar a entrar — e só depois da reserva formada. Ensina, em rota educacional e genérica, o universo de produtos. Sem individualizar, sem corretora, sem comissão.")

def _b(tf):
    bullets(tf, [
        ("Mudança de nome  ", "— de “Criação de Renda Passiva” para “Educação Pré-Investimento”: não promete renda, não aloca."),
        ("Gatilho  ", "— reserva-alvo completa + caixa livre com margem (piso: ≥ 10% do caixa livre destinável)."),
        ("Perfil  ", "— conservador / moderado / arrojado, de forma educativa e não vinculante."),
        ("Universo  ", "— renda fixa, renda variável, fundos, criptoativos, previdência; instituições só como exemplo."),
        ("Ferramentas  ", "— estudo sobre dado público (ex.: Fibonacci em série histórica). Disclaimer em toda saída."),
    ])
content_slide("Capítulo 37–38  ·  Pilar 5 · GI", "Gatilho, perfil, universo", _b, 29)

def _b(tf):
    bullets(tf, [
        ("Fronteira  ", "— Resoluções CVM 19 e 21/2021: recomendação por perfil = consultoria regulada; AAI = 1 corretora por vez."),
        ("Decisão de escopo  ", "— rota educacional genérica pura: não individualiza, não recomenda, não vincula corretora, não recebe comissão."),
        "Se algum dia houver recomendação individualizada, será serviço separado, com registro próprio.",
        ("Comparativo  ", "— Analista de Fundos: R$ 9.604,31/mês → economia R$ 6.104,31 (63,6%) — o comparativo mais artificial dos cinco."),
        ("Mercado  ", "— B3 Educação (500+ conteúdos), escolas de investimento, robo-advisors com registro CVM."),
    ])
content_slide("Capítulo 39–40  ·  Pilar 5 · GI", "Fronteira da CVM · custo · mercado", _b, 28)

# =================== COMPARATIVO CENTRAL
comparativo_slide("Parte VIII", "O comparativo central", [
    ("Pilar · cargo(s) interno(s) equivalente(s)", "Custo total /mês"),
    ("GC · Contábil + Fiscal + DP + R&S", "R$ 30.834,39"),
    ("GF · Analista Financeiro", "R$ 8.789,90"),
    ("GJ · Advogado Empresarial consultivo", "R$ 16.122,33"),
    ("GM · Marketing + Tráfego + SDR", "R$ 26.037,05"),
    ("GI · Analista de Fundos / Educação", "R$ 9.604,31"),
    ("» Estrutura interna equivalente", "» R$ 91.387,98"),
    ("» OCEO — mensalidade única, 5 pilares", "» R$ 3.500,00"),
    ("» Economia mensal", "» R$ 87.887,98  (96,2%)"),
    ("» Economia em 12 meses  ·  payback do setup", "» ≈ R$ 1.054.656   ·   ≈ 4 dias"),
], ["“R$ 91.387 por mês para ter tudo isso dentro de casa. Ou R$ 3.500.” — cena 5 do vídeo.",
    "É a substituição de uma estrutura que a maioria das PMEs nunca poderia bancar — e por isso não tem."])

# ---- mercado
def _b(tf):
    bullets(tf, [
        "Mercado global de ERP: US$ 70–90 bi/ano, crescendo ≈ 10% a.a.",
        "Brasil: SAP e Totvs ≈ 34% cada, Oracle ≈ 10% — juntos ≈ 77%. No recorte PME, Totvs ≈ 53%.",
        "O OCEO não disputa o cliente da SAP — atende a base larga e desassistida abaixo desse recorte.",
        ("A janela  ", "— reforma tributária (IBS/CBS): nos próximos ≈ 24 meses, toda PME vai precisar entender o que muda."),
    ])
content_slide("Capítulo 44", "Mercado e a janela da reforma", _b, 30)

# ---- modelo
def _b(tf):
    bullets(tf, [
        ("Receita  ", "— setup R$ 12.500 + mensalidade R$ 3.500/mês + repasse de custo variável identificado."),
        ("Custo  ", "— dominado pelo time de especialistas do Grupo Sena + infraestrutura + terceiros."),
        ("Premissa  ", "— custo fixo operacional da ordem de R$ 150.000/mês (a validar)."),
        ("Escala  ", "— regras, modelos e trilhas construídos uma vez e reaproveitados: custo incremental por cliente cai."),
    ])
content_slide("Capítulo 45", "Modelo de negócio e escala", _b, 30)

# ---- premissas
def _b(tf):
    bullets(tf, [
        "Custo fixo operacional (≈ R$ 150 mil/mês) · CAC · churn · ponto de equilíbrio — não medidos.",
        "Encargos de 80% e 1 pessoa por cargo nos comparativos.",
        "Salário de Analista de DP e de SDR — por proporção, sem piso CAGED isolável.",
        "Viabilidade e custo da integração Open Finance em escala.",
        "Custo variável do WhatsApp dentro da margem.",
    ])
    p = tf.add_paragraph(); p.space_before = Pt(6)
    setrun(p, "Onde a premissa aparece, o valor assumido está escrito. Quem discorda troca o número.", 13, GOLD, SANS, bold=True)
content_slide("Capítulo 46", "As premissas do modelo", _b, 30)

# ---- roadmap
def _b(tf):
    p = tf.paragraphs[0]
    setrun(p, "Já existe", 15, GOLD, SANS, bold=True, spacing=2.0); p.space_after = Pt(4)
    bullets(tf, [
        "Concepção completa dos 5 pilares · camada contábil do Pilar 1 em produção (9 painéis).",
        "Plano de negócio, pitch de BI, vídeo institucional · marca e domínio · versão Portugal.",
    ], size=14, gap=4)
    p = tf.add_paragraph(); p.space_before = Pt(8)
    setrun(p, "Falta construir", 15, GOLD, SANS, bold=True, spacing=2.0); p.space_after = Pt(4)
    bullets(tf, [
        "Fiscal, DP, RH e Legalização do Pilar 1 em produção · Open Finance validada.",
        "Arranjo com advogado parceiro · custo do WhatsApp na margem · disclaimer do Pilar 5.",
        "Regerar o plano geral de 27 páginas · validar as premissas com clientes reais.",
    ], size=14, gap=4)
content_slide("Capítulo 47", "Roadmap", _b, 30)

# ---- roteiro do video
def _b(tf):
    bullets(tf, [
        ("1 · Abertura  ", "“O sistema orienta. Você decide.”"),
        ("2 · Problema  ", "“A pequena empresa administra no escuro.” + dados SEBRAE."),
        ("3 · Solução  ", "“Um sistema. Cinco frentes. Uma mensalidade.”"),
        ("4 · Os 5 pilares  ", "cada um com descrição + “substitui equipe → R$ X/mês”."),
        ("5 · Comparativo  ", "“R$ 91.387 por mês. Ou R$ 3.500.”  —  96,2%, payback ≈ 4 dias."),
        ("6 · Mercado e modelo  ", "ERP US$ 71–92 bi; alvo PME R$ 50 mil+/mês; badge “premissa” em CAC/churn/PE."),
        ("7 · Fecho  ", "“Administrar com o número na mão.”  —  www.oceo.com.br"),
    ], size=14, gap=6)
content_slide("Parte X  ·  Capítulo 48", "Roteiro do vídeo institucional — 7 cenas", _b, 26)

# ---- marca
def _b(tf):
    bullets(tf, [
        ("O nome  ", "— evoca oceano (a massa de água que o dono navega) e contrai “o CEO” (quem comanda)."),
        ("O símbolo  ", "— um anel (o ciclo de gestão que se fecha) com uma seta ascendente em colunas (o BI). Diz: dado que vira direção."),
        ("Cores  ", "— cromo/prata (a estrutura), dourado (o resultado), azul-marinho profundo (o oceano)."),
        ("Situação  ", "— domínio www.oceo.com.br registrado; marca OCEO em processo no INPI."),
    ])
content_slide("Parte XI  ·  Capítulo 49", "A marca OCEO", _b, 30)

# ---- fecho
s = prs.slides.add_slide(BLANK)
bg(s, DARK)
w = Inches(3.5); h = Emu(int(w * FULL_RATIO))
pic = s.shapes.add_picture(LOGO_FULL, (SW - w) / 2, Inches(1.25), w, h)
lsid = pic.shape_id
box, tf = tb(s, Inches(1.5), Inches(4.75), Inches(10.3), Inches(2.2), MSO_ANCHOR.TOP)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
setrun(p, "Administrar com o número na mão.", 30, WHITE, SERIF, bold=True)
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
setrun(p2, "www.oceo.com.br", 16, GOLD, SANS, bold=True, spacing=1.5)
p2.space_before = Pt(12)
p3 = tf.add_paragraph(); p3.alignment = PP_ALIGN.CENTER
setrun(p3, "Gilberto Luís de Sena  ·  Grupo Sena — Soluções Empresariais  ·  setembro de 2026", 11, MUTE, SANS)
p3.space_before = Pt(14)
tsid = box.shape_id
add_transition(s)
animate(s, [tsid], lsid)

prs.save(OUT)
print("OK ->", OUT)
print("slides:", len(prs.slides._sldIdLst))

#!/usr/bin/env python3
"""Monta os 9 e-books: capa (PNG) + miolo claro + certificado + contracapa (com foto).
Gera HTML das 2 páginas extras por livro, chama o render node, e faz o merge.
"""
import os, subprocess, sys, pymupdf

ROOT = "/Users/gilbertosena/Desktop/GilbertoOS"
LEIT = f"{ROOT}/leitura"
MIOLOS = f"{ROOT}/saidas/ebook-seja-rico-montado-2026-09-08/miolos-claros"
BUILD = f"{ROOT}/saidas/ebook-seja-rico-montado-2026-09-08/_lote"
OUT = f"{ROOT}/E-boocks prontos"
FOTO = f"{ROOT}/saidas/ebook-seja-rico-montado-2026-09-08/foto-autor.jpg"
LEAO = f"{ROOT}/saidas/ebook-seja-rico-montado-2026-09-08/leao.png"
os.makedirs(BUILD, exist_ok=True); os.makedirs(OUT, exist_ok=True)

BIO = ("Gilberto Sena é empresário e fundador do Grupo Sena — consultoria em contabilidade, "
       "tributário e gestão, com escritórios em cinco capitais. Foi de motoboy a fundador de "
       "grupo empresarial e hoje ajuda outros donos de negócio a fazer o mesmo percurso. "
       "Escreve como fala: reto, com história e com lição.")

BOOKS = {
 "startap": dict(
   cover="A Startap Unicornio.png", cert="Certificado - A Startap Unicornio.pdf",
   miolo="A Startap Unicornio.pdf", out="A Startap Unicornio - Gilberto Sena.pdf",
   title="A Startap Unicórnio", subtitle="Empreendedorismo enxuto e construção de negócios a partir do zero",
   hook="Você não precisa do Vale do Silício para construir um negócio livre.",
   p1=("Leitura aplicada de <em>A Startup de $100</em>, de Chris Guillebeau — o estudo de mais de cem "
       "pessoas comuns que ergueram negócios lucrativos com pouco ou nenhum capital. Capítulo por "
       "capítulo, os ensinamentos centrais da obra."),
   p2=("E mais: a leitura do Gilberto, como empresário que vive de entender estrutura de negócio e de "
       "imposto, sobre o que a Inteligência Artificial vai fazer com esse modelo na próxima década — "
       "a era do unicórnio de uma pessoa só."),
   quote="Liberdade é o que todo mundo busca. Valor é o caminho para chegar lá.",
   parts=[("I","Empreendedores inesperados"),("II","Apresentar seu filho ao mundo"),
          ("III","Alavancagem e próximos passos"),("+","A década dos unicórnios — IA e a próxima década"),
          ("+","Estudos de caso do Grupo Sena"),("+","Plano de 90 dias — da leitura à ação")]),

 "motoboy": dict(
   cover="De MotoBoy a Execultivo.png", cert="Certificado - De Motoboy a Executivo.pdf",
   miolo="De Motoboy a Executivo.pdf", out="De Motoboy a Executivo - Gilberto Sena.pdf",
   title="De Motoboy a Executivo", subtitle="Liderança servidora e gestão de pessoas na prática",
   hook="Autoridade de verdade não vem do cargo. Vem de servir.",
   p1=("Leitura aplicada de <em>O Monge e o Executivo</em>, de James C. Hunter — a parábola de John "
       "Daily, o gerente de sucesso aparente cuja vida desmorona por dentro, e o retiro de sete dias "
       "que reconstrói o que ele entende por liderança."),
   p2=("Cruzada com a trajetória do Gilberto: de motoboy assaltado e afastado do emprego a fundador "
       "do Grupo Sena. Os mesmos princípios — autoridade, serviço e amor — vistos dos dois lados, "
       "com aplicações bíblicas ao fim de cada bloco."),
   quote="O que faz uma pessoa seguir outra de boa vontade?",
   parts=[("·","Prólogo — “A escolha foi minha”"),("1","As Definições"),("2","O Velho Paradigma"),
          ("3","O Modelo"),("4","O Verbo — definindo amor"),("5","O Ambiente"),
          ("6","A Escolha"),("7","A Recompensa")]),

 "entenda": dict(
   cover="Entenda Suas Financas .png", cert="Certificado - Entenda Suas Financas.pdf",
   miolo="Entenda Suas Financas.pdf", out="Entenda Suas Financas - Gilberto Sena.pdf",
   title="Entenda Suas Finanças", subtitle="Orçamento, planejamento e controle financeiro para o seu negócio",
   hook="Empresa não quebra por falta de venda. Quebra por não saber ler o próprio balanço.",
   p1=("Do básico à leitura de balanço, na prática. Sem jargão: os conceitos que sustentam toda "
       "decisão de dinheiro na empresa — orçamento, financiamento, controle, fluxo de caixa."),
   p2=("Da montagem do orçamento à leitura de um balanço patrimonial e de uma DRE, com estudos de "
       "caso reais do Grupo Sena e um plano de 90 dias para sair do escuro."),
   quote="Entender finanças não é luxo. É sobrevivência.",
   parts=[("1","Planejamento financeiro"),("2","Fontes e formas de financiamento"),
          ("3","Planejamento e orçamento empresarial"),("4","Controle financeiro"),
          ("5","Fluxo de caixa"),("6","Como ler um balanço patrimonial"),("7","Como ler uma DRE")]),

 "estrategia": dict(
   cover="Estrategia da Gestao.png", cert="Certificado - Estrategia da Gestao.pdf",
   miolo="Estrategia da Gestao.pdf", out="Estrategia da Gestao - Gilberto Sena.pdf",
   title="Estratégia da Gestão", subtitle="A Arte da Guerra aplicada à liderança e à governança empresarial",
   hook="Um general chinês entende de gestão melhor que a maioria dos livros de MBA.",
   p1=("Os doze capítulos de <em>A Arte da Guerra</em>, de Sun Tzu — o tratado militar mais estudado "
       "da história — aplicados, quase sem adaptação, à cadeira de quem lidera uma empresa hoje. "
       "Uma leitura estratégica, capítulo por capítulo."),
   p2=("Cruzada com os 5 G's da Gestão Empreendedora e com a experiência do Gilberto de fundar, "
       "quebrar, reerguer e fazer crescer negócios de verdade. Para ler com caneta na mão."),
   quote="Vencer a batalha antes de lutar é planejar antes de agir.",
   parts=[("·","Os 12 capítulos de A Arte da Guerra aplicados à gestão"),
          ("·","Os 5 G's como as cinco virtudes do general"),
          ("·","Os cinco perigos do líder — releitura empresarial"),
          ("·","Estudos de caso reais do Grupo Sena"),
          ("+","Checklist estratégico e plano de 90 dias")]),

 "segredo": dict(
   cover="O Segredo Das Financas.png", cert="Certificado - O Segredo Das Financas.pdf",
   miolo="O Segredo Das Financas.pdf", out="O Segredo Das Financas - Gilberto Sena.pdf",
   title="O Segredo Das Finanças", subtitle="A matemática financeira explicada por quem vive de números todos os dias",
   hook="Juros não é opinião. É conta — e quem não sabe fazê-la paga por ela a vida inteira.",
   p1=("Juro simples e composto, equivalência de capitais, anuidades, amortização e os efeitos da "
       "inflação — a lógica que não muda com o tempo, reconstruída na voz do Gilberto, com exemplos "
       "e dados atuais."),
   p2=("O que fazer com cada fórmula na vida real: comprar à vista ou a prazo, aceitar ou recusar um "
       "empréstimo, negociar uma dívida. Inclui exercícios, gabarito, simulado final e um plano de "
       "30 dias."),
   quote="O objetivo não é fazer de você um matemático. É fazer de você alguém que nunca mais assina um contrato no escuro.",
   parts=[("·","Conceitos essenciais · Por que existe juro"),("·","Juros simples e compostos"),
          ("·","Equivalência de capitais · Anuidades · Amortização"),("·","Os efeitos da inflação"),
          ("·","Rotativo do cartão e cheque especial"),("+","Estudos de caso, tabela de fórmulas e simulado")]),

 "pilares": dict(
   cover="Os Pilares de um Homem Prospero.png", cert="Certificado - Os Pilares de um Homem Prospero.pdf",
   miolo="Os Pilares de um Homem Prospero.pdf", out="Os Pilares de um Homem Prospero - Gilberto Sena.pdf",
   title="Os Pilares de um Homem Próspero", subtitle="Sabedoria de Provérbios aplicada aos negócios e à vida",
   hook="Um livro de três mil anos ainda decide o seu próximo passo.",
   p1=("Seis pilares — o temor do Senhor, a palavra, o trabalho, o dinheiro, a casa e o legado — que "
       "separam quem prospera de forma sólida de quem prospera por um tempo e depois desmorona."),
   p2=("Cada pilar com a mesma estrutura: o que o texto bíblico ensina, o que o Gilberto viveu que "
       "confirma isso (ou que lhe custou caro por ter ignorado) e como vira decisão prática no seu "
       "negócio esta semana."),
   quote="Prosperidade, aqui, nunca é sorte. É estrutura. É pilar — e pilar se constrói, um de cada vez, antes da casa ficar de pé.",
   parts=[("1","O temor do Senhor — o alicerce que ninguém vê"),("2","A palavra — o que sai da boca constrói ou derruba"),
          ("3","O trabalho — diligência contra a preguiça"),("4","O dinheiro — prudência, não sorte"),
          ("5","A casa — família como o primeiro negócio"),("6","O legado — prosperar para servir")]),

 "posicione": dict(
   cover="Posicione-se Ou Morra.png", cert="Certificado - Posicione-se ou Morra.pdf",
   miolo="Posicione-se ou Morra.pdf", out="Posicione-se ou Morra - Gilberto Sena.pdf",
   title="Posicione-se ou Morra", subtitle="Posicionamento de marca pessoal e empresarial",
   hook="Se dez pessoas na rua não sabem dizer o que a sua empresa faz, você não existe pra elas.",
   p1=("Releitura do clássico <em>Positioning</em>, de Al Ries e Jack Trout, para o mundo de hoje — "
       "feed, Reels, algoritmo, milhões de perfis disputando o mesmo segundo de atenção. A régua "
       "mudou; o princípio, não."),
   p2=("Com casos reais dissecados — Cimed, G4, Nubank, Magalu — e o ponto que quase todo empresário "
       "ignora: você é a marca antes da empresa. Inclui os erros mais caros do posicionamento digital "
       "e um plano de 90 dias."),
   quote="Problema de posicionamento não se resolve com design novo. Resolve-se com uma decisão clara sobre que espaço você quer ocupar na cabeça de quem compra de você.",
   parts=[("1–4","O que é posicionamento · físico x digital · a era do algoritmo"),
          ("5","Caso Cimed — quando o dono vira a marca"),("6","Caso G4 — comunidade é o novo posicionamento"),
          ("7","Caso Nubank — um nome, uma promessa"),("8","Caso Magalu — o físico e o digital na mesma pele"),
          ("9","Você é a marca — antes da empresa"),("11","Os erros mais caros do posicionamento digital")]),

 "quite": dict(
   cover="Quite Suas Dividas Já.png", cert="Certificado - Quite Suas Dividas Ja.pdf",
   miolo="Quite Suas Dividas Ja.pdf", out="Quite Suas Dividas Ja - Gilberto Sena.pdf",
   title="Quite Suas Dívidas Já", subtitle="O guia completo para negociar com bancos, financeiras e credores",
   hook="Dívida não se resolve com vergonha. Resolve-se com estratégia.",
   p1=("O passo a passo para sentar na mesa com banco, consignado, cartão, financeira, agiota e Fisco "
       "sabendo o que pedir, o que é irregular no seu contrato e até onde a outra parte pode ir."),
   p2=("Sem prometer não pagar o que é devido — mostrando como pagar o correto, nem um centavo a "
       "mais. Com a Lei do Superendividamento, seus direitos diante de Serasa e SPC e o que a "
       "Constituição diz sobre isso."),
   quote="Todo endividado precisa de três coisas. A primeira é saber que não está sozinho.",
   parts=[("1","Negociando dívidas com banco"),("2","Consignados e suas irregularidades"),
          ("3","Renovação de contratos — a armadilha mais comum"),("4","Dívidas de cartão de crédito"),
          ("5–6","Financeiras e agiotas"),("7","Dívida ativa na União — a PGFN"),
          ("8","Recuperação judicial — o que existe pra você"),("9–10","Superendividamento, CDC e a Constituição")]),

 "emocoes": dict(
   cover="No Controle Das Emocoes.png", cert="Certificado - No Controle Das Emocoes.pdf",
   miolo="No Controle Das Emocoes.pdf", out="No Controle Das Emocoes - Gilberto Sena.pdf",
   title="No Controle Das Emoções", subtitle="Inteligência emocional aplicada a negócios, empresas e relacionamentos",
   hook="Decisão tomada com raiva sai cara. Sob medo, também.",
   p1=("Uma ponte entre a ciência da inteligência emocional — a mecânica de como a emoção funciona no "
       "cérebro e os cinco domínios do autodomínio — e o livro <em>Não Há Dívidas</em>, do Gilberto, "
       "sobre as cobranças invisíveis que a gente carrega sem ter assinado."),
   p2=("Da ciência vem o “como funciona”. Da vivência vem o “o que fazer com isso”. Um método prático "
       "para quem lidera pessoas, negocia, decide sob pressão — e ainda quer chegar em casa inteiro."),
   quote="Controlar não é sufocar. É usar o que você sente a favor da sua escolha.",
   parts=[("I","A máquina por dentro — o sequestro e para que serve cada emoção"),
          ("II","A conta emocional — as cobranças que você não assinou"),
          ("III","Autodomínio — os cinco domínios na prática"),
          ("IV","Nas relações — sócios, clientes, equipe, casa"),
          ("+","Ferramentas e plano de aplicação")]),
}

TPL = """<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--papel:#F4F1EA;--tinta:#151515;--corpo:#3f3f3f;--ouro:#C9A227;--linha:#d9d2c2}}
*{{margin:0;padding:0;box-sizing:border-box}}@page{{size:A4;margin:0}}
html,body{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;break-after:page}}
.page:last-child{{page-break-after:auto;break-after:auto}}
.capa{{background:#0A0A0A;display:flex;align-items:center;justify-content:center}}
.capa img{{height:100%;width:auto;max-width:100%;display:block}}
.cc{{background:var(--papel);color:var(--corpo);font-family:'Inter',sans-serif;padding:24mm 22mm 18mm;display:flex;flex-direction:column}}
.cc .kicker{{font-size:9.5pt;font-weight:700;letter-spacing:.28em;text-transform:uppercase;color:var(--ouro)}}
.cc .rule{{width:46pt;height:2.5pt;background:var(--ouro);margin:9pt 0 18pt}}
.cc h1{{font-family:'Fraunces',serif;font-weight:600;color:var(--tinta);font-size:21pt;line-height:1.26;letter-spacing:-0.01em;max-width:150mm}}
.cc .lead{{margin-top:14pt;font-size:10.5pt;line-height:1.6;color:var(--corpo)}}
.cc .lead+.lead{{margin-top:8pt}} .cc .lead em{{font-style:italic}}
.cc .quote{{margin:18pt 0;padding:12pt 0 12pt 16pt;border-left:3pt solid var(--ouro);font-family:'Fraunces',serif;font-size:12.5pt;line-height:1.5;color:var(--tinta)}}
.cc .partes{{margin-top:2pt;border-top:1pt solid var(--linha);border-bottom:1pt solid var(--linha);padding:12pt 0;display:grid;grid-template-columns:1fr 1fr;gap:6pt 20pt}}
.cc .partes div{{font-size:9pt;line-height:1.4;color:var(--corpo)}}
.cc .partes b{{color:var(--ouro);font-weight:700;margin-right:6pt}}
.cc .autor{{margin-top:16pt;display:flex;gap:15pt;align-items:flex-start}}
.cc .autor .foto{{flex:0 0 32mm;width:32mm;height:42mm;object-fit:cover;object-position:50% 22%;border-radius:4pt;border:1pt solid var(--linha);filter:grayscale(.15)}}
.cc .autor .h{{font-size:9pt;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:var(--tinta);margin-bottom:6pt}}
.cc .autor p{{font-size:9.5pt;line-height:1.56;color:var(--corpo)}}
.cc .foot{{margin-top:auto;padding-top:14pt;border-top:1pt solid var(--linha);display:flex;align-items:flex-end;justify-content:space-between;gap:14pt}}
.cc .foot .brand{{display:flex;align-items:center;gap:10pt}}
.cc .foot .brand img{{width:28pt;height:28pt;object-fit:contain}}
.cc .foot .brand .n{{font-family:'Fraunces',serif;font-weight:600;font-size:11.5pt;color:var(--tinta);letter-spacing:.02em}}
.cc .foot .meta{{text-align:right;font-size:8pt;line-height:1.6;color:#8a8374}}
.cc .foot .meta b{{color:var(--corpo);font-weight:600}}
</style></head><body>
<div class="page capa"><img src="{cover}"></div>
<div class="page cc">
  <div class="kicker">Gilberto Sena · e-book</div><div class="rule"></div>
  <h1>{hook}</h1>
  <p class="lead">{p1}</p>
  <p class="lead">{p2}</p>
  <div class="quote">{quote}</div>
  <div class="partes">{partes}</div>
  <div class="autor"><img class="foto" src="{foto}">
    <div><div class="h">Sobre o autor</div><p>{bio}</p></div></div>
  <div class="foot">
    <div class="brand"><img src="{leao}"><span class="n">GILBERTO SENA</span></div>
    <div class="meta"><b>{title}</b> · 1ª edição · 2026<br>Grupo Sena · Ideias que constroem vidas<br>@gilbertosenaoficial</div>
  </div>
</div></body></html>"""

def build_html(key, b):
    partes = "".join(f'<div><b>{n}</b>{t}</div>' for n,t in b["parts"])
    html = TPL.format(cover=f'{LEIT}/{b["cover"]}', hook=b["hook"], p1=b["p1"], p2=b["p2"],
                      quote=b["quote"], partes=partes, foto=FOTO, leao=LEAO, bio=BIO, title=b["title"])
    p = f"{BUILD}/{key}.html"; open(p,"w").write(html); return p

def main():
    keys = sys.argv[1:] or list(BOOKS)
    for key in keys:
        b = BOOKS[key]
        html = build_html(key, b)
        pdf = f"{BUILD}/{key}-extras.pdf"
        subprocess.run(["node", f"{ROOT}/saidas/ebook-seja-rico-montado-2026-09-08/render-abs.js", html, pdf],
                       check=True, env={**os.environ, "NODE_PATH": f"{ROOT}/scripts/node_modules"})
        extras = pymupdf.open(pdf)
        miolo = pymupdf.open(f"{MIOLOS}/{b['miolo']}")
        cert = pymupdf.open(f"{LEIT}/{b['cert']}")
        w = pymupdf.open()
        w.insert_pdf(extras, from_page=0, to_page=0)      # capa
        w.insert_pdf(miolo)                                # miolo claro
        w.insert_pdf(cert)                                 # certificado
        w.insert_pdf(extras, from_page=1, to_page=1)       # contracapa
        w.set_metadata({"title": b["title"], "author": "Gilberto Sena"})
        outp = f"{OUT}/{b['out']}"
        w.save(outp, garbage=4, deflate=True)
        print(f"OK {b['out']}  ({w.page_count} pgs)")

if __name__ == "__main__":
    main()

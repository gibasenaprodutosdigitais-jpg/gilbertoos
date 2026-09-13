# -*- coding: utf-8 -*-
"""
Video de ESTUDO PESSOAL para o Gilberto ensaiar o Mapa Executivo do evento
de Reengenharia Empresarial (Bloco 1, Bloco 2, Pitch, Bloco 3), a partir de
"evento Gilberto para validacao dia 27-08 .pdf".

Narracao (voz do sistema) + cartoes de estudo (kicker/titulo/bullets/frase-
chave/objetivo). Sem trilha - e material de ensaio, nao de postagem.
"""
import os, subprocess, json

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(HERE, "audio")
os.makedirs(AUD, exist_ok=True)

VOICE = os.environ.get("VOICE", "Luciana")
RATE = int(os.environ.get("RATE", "182"))
FPS = 30
W, H = 1920, 1080

# ------------------------------------------------------------------ conteudo
# cada segmento: kind = title | divider | topic
SEGMENTS = [
  dict(kind="title",
    kicker="GUIA DE ESTUDO PESSOAL",
    title="Reengenharia Empresarial",
    sub="Mapa executivo do evento — passo a passo para ensaiar a condução",
    narr="Este é o seu guia de estudo do mapa executivo do evento de Reengenharia "
         "Empresarial. Vamos passar bloco por bloco, tópico por tópico: o objetivo "
         "de cada um, a tese, e as frases-chave que você planejou dizer. Use este "
         "áudio pra internalizar o fluxo antes do dia da virada."),

  dict(kind="title",
    kicker="VISÃO GERAL DO DIA",
    title="Três blocos, um pitch, uma decisão",
    bullets=[
      "Bloco 1 · 09h00–12h30 — O Choque da Realidade",
      "Bloco 2 · 14h00–16h30 — O Diagnóstico e a Trava de Execução",
      "Pitch da Mentoria · 16h30–17h15 — R$ 30.000, 90 dias, 5 vagas",
      "Bloco 3 · 18h00–19h30 — O Repeat Emocional e a Decisão do Legado",
    ],
    narr="O dia tem uma arquitetura só. De manhã, você quebra a cegueira do "
         "empresário. À tarde, entrega um diagnóstico que ele mesmo preenche, e "
         "mostra que ele não tem como executar isso sozinho. Aí vem o pitch "
         "racional, às dezesseis e trinta. Se a sala travar, o bloco três, à "
         "noite, é a virada emocional: família, legado, e a assinatura da ficha."),

  dict(kind="divider",
    kicker="BLOCO 1 · 09H00 – 12H30",
    title="O Choque da Realidade e a Ruína da Estrutura",
    sub="Objetivo: quebrar a cegueira do empresário e instalar o pânico técnico "
        "legítimo antes do almoço.",
    narr="Bloco um. Nove às doze e meia. O objetivo aqui não é dar aula — é "
         "desmontar o sofisma da empresa lucrativa e deixar o empresário indo "
         "pro almoço com a certeza de que a estrutura atual não aguenta dois mil "
         "e vinte e sete."),

  dict(kind="topic",
    kicker="BLOCO 1 · TÓPICO 1 · 09H00–09H30",
    title="O Sofisma do Faturamento",
    bullets=[
      ("Tese", "Vender muito não significa estar seguro. Faturamento é métrica de vaidade que esconde estrutura podre."),
      ("Crença a destruir", "“Minha empresa fatura R$ 500 mil, então eu sei gerir e estou protegido.”"),
    ],
    quote="Faturamento atrai concorrente e atrai o Fisco; o que alimenta sua "
          "família é a margem líquida e a segurança do seu caixa.",
    objetivo="Quebrar a postura de “já sei de tudo” logo na abertura da sala.",
    narr="Tópico um, nove às nove e meia: o sofisma do faturamento. A tese é "
         "que vender muito não significa estar seguro — faturamento é vaidade, "
         "não segurança. Você quebra a crença de quem acha que faturar alto já "
         "é proteção, com a frase: faturamento atrai concorrente e atrai o "
         "Fisco; o que alimenta a família é a margem líquida e a segurança do "
         "caixa. O objetivo é quebrar o “já sei de tudo” logo na abertura."),

  dict(kind="topic",
    kicker="BLOCO 1 · TÓPICO 2 · 09H30–10H15",
    title="A Armadilha de 2027 e o Split Payment",
    bullets=[
      ("Tese", "A reforma não é mudança de imposto — é reajuste de sobrevivência no fluxo de caixa."),
      ("Mecanismo", "O split payment retém o imposto no ato da transação. O dinheiro não fica mais disponível pra girar caixa."),
    ],
    quote="O Leão vai morder a fatia dele no milissegundo do PIX ou do cartão. "
          "Sua empresa tem fôlego pra rodar assim?",
    objetivo="Trazer 2027 pro hoje — instalar urgência temporal.",
    narr="Tópico dois, nove e meia às dez e quinze: a armadilha de 2027 e o "
         "split payment. A reforma não é mudança de imposto, é reajuste de "
         "sobrevivência no caixa — o split payment retém o imposto no ato da "
         "transação, e o empresário perde o prazo que usava pra girar o "
         "dinheiro. A frase: o Leão vai morder a fatia dele no milissegundo do "
         "PIX ou do cartão, sua empresa tem fôlego pra rodar assim? Objetivo: "
         "trazer 2027 pro hoje."),

  dict(kind="topic",
    kicker="BLOCO 1 · TÓPICO 3 · 10H15–11H00",
    title="A Cegueira Operacional — o “Síndico de Luxo”",
    bullets=[
      ("Tese", "O dono acha que faz gestão, mas só apaga incêndio, paga conta, gera boleto."),
      ("Ancoragem no método", "Cruza Gestão de Si (G1) com Gestão de Pessoas (G3): sem processo, o dono vira refém do próprio funcionário e fornecedor."),
    ],
    quote="Você construiu uma prisão com o seu CNPJ. E o pior: se você se "
          "afastar 30 dias por saúde, a sua empresa rui.",
    objetivo="Fazer o empresário admitir, por dentro, o cansaço de carregar tudo sozinho.",
    narr="Tópico três, dez e quinze às onze: a cegueira operacional, o síndico "
         "de luxo. O dono acha que administra, mas só apaga incêndio. Você cruza "
         "gestão de si com gestão de pessoas: sem processo, ele vira refém do "
         "próprio funcionário. A frase: você construiu uma prisão com o seu "
         "CNPJ — e se você se afastar trinta dias por saúde, a empresa rui. "
         "Objetivo: fazer ele admitir o cansaço de carregar tudo sozinho."),

  dict(kind="topic",
    kicker="BLOCO 1 · TÓPICO 4 · 11H00–11H45",
    title="Os 3 Ralos Invisíveis",
    bullets=[
      ("Ralo Tributário (G4)", "Enquadramento errado mantido por anos — o contador é gerador de guia, não estrategista."),
      ("Ralo de Pessoas e Passivos (G3)", "Contrato mal estruturado, risco trabalhista acumulado em silêncio."),
      ("Ralo do Caixa Misturado (G2)", "PF e PJ confundidos — o pró-labore maquiado que expõe o patrimônio pessoal."),
    ],
    objetivo="Fazer cada um dos 20 empresários tentar adivinhar por qual ralo a própria empresa está vazando mais dinheiro.",
    narr="Tópico quatro, onze às onze e quarenta e cinco: os três ralos "
         "invisíveis. A empresa não quebra de uma vez, ela sangra por três "
         "perfurações: o ralo tributário, do enquadramento errado; o ralo de "
         "pessoas e passivos, do contrato mal feito; e o ralo do caixa "
         "misturado, de pessoa física com jurídica. Objetivo: fazer cada um dos "
         "vinte empresários tentar adivinhar por qual ralo ele está vazando "
         "mais."),

  dict(kind="topic",
    kicker="BLOCO 1 · TÓPICO 5 · 11H45–12H30",
    title="O Diagnóstico de Sobrevivência — o Quebrador de Ego",
    bullets=[
      ("A pergunta devastadora", "Se o Fisco fizer auditoria cruzada com IA hoje, ou o split payment entrar amanhã, o seu patrimônio pessoal sobrevive ou é arrastado com o CNPJ?"),
    ],
    quote="Olhem para o prato de vocês e pensem: a estrutura que vocês "
          "montaram protege o futuro da família, ou é um castelo de cartas "
          "esperando o vento de 2027?",
    objetivo="Fechar a manhã com consciência de risco — pânico técnico legítimo, não motivacional.",
    narr="Tópico cinco, onze e quarenta e cinco ao meio-dia e meia: o "
         "diagnóstico de sobrevivência, o quebrador de ego. A pergunta que "
         "fecha a manhã: se o Fisco cruzar dados com inteligência artificial "
         "hoje, seu patrimônio pessoal sobrevive ou é arrastado junto com o "
         "CNPJ? E a frase pro almoço: olhem pro prato e pensem — a estrutura "
         "que vocês montaram protege a família, ou é um castelo de cartas "
         "esperando o vento de 2027?"),

  dict(kind="title",
    kicker="FLUXO EMOCIONAL · BLOCO 1",
    title="Da curiosidade ao pânico consciente",
    bullets=[
      "09h00 — Curiosidade e ego alto",
      "10h00 — Choque de realidade (2027)",
      "11h00 — Identificação da dor (ralos e canseira)",
      "12h30 — Consciência de risco e necessidade de mudança",
    ],
    narr="Resumo emocional do bloco um: a sala entra com curiosidade e ego "
         "alto, às dez horas leva o choque de realidade de 2027, às onze "
         "identifica a própria dor nos ralos e na canseira, e sai pro almoço às "
         "doze e meia com consciência de risco e pânico técnico instalado."),

  dict(kind="divider",
    kicker="BLOCO 2 · 14H00 – 16H30",
    title="O Diagnóstico e a Trava de Execução",
    sub="Objetivo: entregar um micro-resultado com o Canvas da Reengenharia, e "
        "provar que resolver isso sozinho é o caminho mais rápido pra quebrar.",
    narr="Bloco dois. Quatorze às dezesseis e trinta. Agora o objetivo é "
         "entregar um micro-resultado de verdade, com o Canvas da Reengenharia, "
         "e em seguida provar que tentar resolver essa equação sem ajuda "
         "técnica especialista é o caminho mais rápido pra parar a operação."),

  dict(kind="topic",
    kicker="BLOCO 2 · TÓPICO 1 · 14H00–14H30",
    title="O Despertar da Tarde",
    bullets=[
      ("Conceito", "Voltam do almoço “anestesiados” — o problema já não dói de tanto acostumado."),
      ("Framework a usar", "Incompetente inconsciente → incompetente consciente → competente consciente → competente inconsciente (com o Gilberto ao lado)."),
      ("Dinâmica", "Desafio: desligar o celular e deixá-lo de cara pra baixo até o fim do evento."),
    ],
    quote="Isso é a prova viva de que a sua empresa não tem uma estrutura; tem "
          "apenas a sua força física segurando as paredes.",
    objetivo="Reconectar a sala e tirar o foco do celular antes da parte prática.",
    narr="Bloco dois, tópico um, quatorze às quatorze e trinta: o despertar da "
         "tarde. Eles voltam anestesiados do almoço. Use o framework de "
         "consciência: incompetente inconsciente, incompetente consciente, "
         "competente consciente, e por fim competente inconsciente, andando "
         "com você ao lado. A dinâmica é o desafio do celular: desligar e "
         "deixar de cara pra baixo até o fim do evento — se ele não controla "
         "nem o telefone, quem dirá a empresa. A frase: isso é a prova viva de "
         "que sua empresa não tem estrutura, tem só a sua força física "
         "segurando as paredes."),

  dict(kind="topic",
    kicker="BLOCO 2 · TÓPICO 2 · 14H30–15H15",
    title="O Canvas da Reengenharia Empresarial",
    bullets=[
      ("Ferramenta", "Roda da Conformidade e Reengenharia: nota de 1 a 10 nos 5 G's — Si, Financeira, Pessoas, Tributária, Parceiros."),
      ("Dinâmica", "Chamar 2 ou 3 empresários (o pequeno e o de R$1 milhão/semana) pra ler a nota mais baixa em voz alta."),
      ("Técnica do apadrinhamento", "Tom manso, olho no olho: “você pode mentir pra todo mundo — essa nota é verdadeira?” Depois, os 5 porquês até a ficha cair."),
    ],
    objetivo="Sair do “pressentimento de que algo vai mal” pra ter a prova cirúrgica no papel.",
    narr="Tópico dois, quatorze e trinta às quinze e quinze: o Canvas da "
         "Reengenharia. Cada um dá nota de um a dez nos cinco G's e desenha a "
         "própria roda. Você chama dois ou três à frente pra ler a nota mais "
         "baixa — usando o apadrinhamento: tom manso, olho no olho, "
         "perguntando se aquela nota é mesmo verdadeira. Depois, os cinco "
         "porquês, até a ficha cair. Objetivo: sair do pressentimento e chegar "
         "na prova cirúrgica, no papel."),

  dict(kind="topic",
    kicker="BLOCO 2 · TÓPICO 3 · 15H15–15H45",
    title="A Equação da Margem Oculta",
    bullets=[
      ("Tese", "Margem ilusória: ele acha que tem 15%, mas opera com 2% líquido — 13% vaza em passivo, retrabalho e bitributação."),
      ("Contraste", "Contabilidade de Guia (serve ao governo) x Contabilidade Estratégica (recupera a margem do dono)."),
      ("Demonstração ao vivo", "Chamar alguém da plateia, jogar os dados dele na ferramenta OCEO no telão — gera desejo nos outros. A ferramenta entra como bônus de 30–60 dias dentro da mentoria."),
    ],
    objetivo="Provar matematicamente que a mentoria recupera dinheiro que ele já está perdendo todo mês.",
    narr="Tópico três, quinze e quinze às quinze e quarenta e cinco: a equação "
         "da margem oculta. Ele acha que tem quinze por cento de margem, mas "
         "na real opera com dois por cento líquido. A diferença é contabilidade "
         "de guia, que só serve ao governo, contra contabilidade estratégica, "
         "que recupera a margem do dono. Aqui entra a demonstração ao vivo: "
         "chamar alguém da plateia e rodar os dados dele na ferramenta OCEO no "
         "telão — isso gera desejo nos outros, e a ferramenta vira bônus "
         "estratégico dentro da mentoria. Ponto de atenção: se for usar dado "
         "real de um participante ao vivo, confirme autorização dele antes, ou "
         "use um exemplo fictício em ordem de grandeza parecida."),

  dict(kind="topic",
    kicker="BLOCO 2 · TÓPICO 4 · 15H45–16H30",
    title="A Armadilha do “Faça Você Mesmo”",
    bullets=[
      ("Caminho 1 — sozinho", "“Você é o dono. Se sentar pra estudar legislação, quem vende e traz cliente?”"),
      ("Caminho 2 — contabilidade tradicional", "“Sua contabilidade teve 5, 10 anos pra fazer isso e não fez. É gerador de guia, não estrategista.”"),
      ("Caminho 3 — gerente financeiro", "“Seu funcionário não tem visão de dono nem autoridade jurídica pra renegociar dívida ou blindar patrimônio.”"),
      ("Gatilho extra", "Pergunta sobre férias de verdade + fotos das suas próprias viagens como prova de vida."),
    ],
    quote="Você já sabe onde está o furo do seu balde. Vai continuar tampando "
          "com o dedo, ou vai deixar quem tem 40 anos de estrada assumir?",
    objetivo="Instalar a consciência de incapacidade de execução solo — a ponte pro pitch.",
    narr="Tópico quatro, quinze e quarenta e cinco às dezesseis e trinta: a "
         "armadilha do faça você mesmo. Desmonte os três caminhos ingênuos: "
         "fazer sozinho, delegar pro contador tradicional, ou pro gerente "
         "financeiro — nenhum resolve. O gatilho extra é perguntar sobre "
         "férias de verdade e mostrar suas próprias fotos de viagem. A frase "
         "de fechamento, ponte pro pitch: você já sabe onde está o furo do "
         "balde — vai continuar tampando com o dedo, ou vai deixar quem tem "
         "quarenta anos de estrada assumir?"),

  dict(kind="title",
    kicker="FLUXO EMOCIONAL · BLOCO 2",
    title="Do foco restaurado à abertura pro pitch",
    bullets=[
      "14h00 — Foco restaurado",
      "14h30 — Clareza cirúrgica do erro (Canvas)",
      "15h15 — Desejo de recuperar a margem perdida",
      "15h45 — Trava da execução solo",
      "16h30 — Abertura total pro pitch",
    ],
    narr="Resumo emocional do bloco dois: foco restaurado às quatorze horas, "
         "clareza cirúrgica com o Canvas às quatorze e trinta, desejo de "
         "recuperar a margem às quinze e quinze, a trava da execução sozinho "
         "às quinze e quarenta e cinco, e abertura total pro pitch às "
         "dezesseis e trinta."),

  dict(kind="topic",
    kicker="PITCH DA MENTORIA · 16H30–17H15",
    title="O Projeto Executivo de Reengenharia",
    bullets=[
      ("Posicionamento", "Não é curso. É o Acompanhamento e Projeto Executivo de Reengenharia Empresarial, conduzido por você e seu time sênior."),
      ("Proposta", "Sentar na mesa da empresa, auditar os 5 pilares, fechar as torneiras de sangria, blindar pra 2027."),
      ("Investimento", "R$ 30.000 — 90 dias."),
      ("Escassez real", "Apenas 5 cotas, pela complexidade do acompanhamento direto."),
    ],
    objetivo="Entrada 100% fluida depois do Tópico 4 — sem pausa, sem perder o embalo.",
    narr="Dezesseis e trinta às dezessete e quinze: o pitch da mentoria. "
         "Posicione como acompanhamento e projeto executivo, não curso — "
         "noventa dias, trinta mil reais, auditando os cinco pilares e "
         "blindando a empresa pra 2027. A escassez é real: só cinco cotas, "
         "pela complexidade do acompanhamento direto com você. A entrada "
         "aqui é cem por cento fluida, direto depois do tópico quatro, sem "
         "pausa."),

  dict(kind="divider",
    kicker="BLOCO 3 · 18H00 – 19H30",
    title="O Repeat Emocional e a Decisão do Legado",
    sub="Cenário: resistência total, ninguém assinou no pré-pitch. Postura de "
        "Profeta e Mentor Sênior — a Pregação do Legado.",
    narr="Bloco três. Dezoito às dezenove e trinta. Este é o cenário de "
         "resistência total — ninguém comprou no pitch racional. Aqui você "
         "deixa a postura de consultor e assume a postura de mentor sênior, "
         "com a técnica da pregação do legado: cirurgia emocional, "
         "responsabilidade familiar, provocação ética."),

  dict(kind="topic",
    kicker="BLOCO 3 · TÓPICO 1 · 18H00–18H30",
    title="O Preço Oculto da Omissão",
    bullets=[
      ("Tese", "Não decidir agora parece seguro. Na verdade, a não-decisão é a pior decisão possível."),
      ("Ancoragem bíblica", "Mateus 25:21 — a Parábola dos Talentos. “Fiel no pouco, sobre o muito te colocarei.”"),
    ],
    quote="Você não vai pensar em nada. Vai voltar pros mesmos incêndios de "
          "sempre, até o Fisco bater na porta ou a margem zerar.",
    objetivo="Expor a omissão como risco moral, não só como risco de negócio.",
    narr="Bloco três, tópico um, dezoito às dezoito e trinta: o preço oculto "
         "da omissão. Ancore em Mateus vinte e cinco, vinte e um, a parábola "
         "dos talentos. A frase: você não vai pensar em nada, vai voltar pros "
         "mesmos incêndios até o Fisco bater na porta ou a margem zerar. "
         "Objetivo: expor a omissão como risco moral, não só de negócio."),

  dict(kind="topic",
    kicker="BLOCO 3 · TÓPICO 2 · 18H30–19H00",
    title="A Cadeira Vazia",
    bullets=[
      ("Tese", "A empresa bagunçada não rouba só dinheiro — rouba presença, sono, saúde, futuro dos filhos."),
      ("Ferida exposta", "A solidão do topo. Gancho pro ecossistema empresarial que você quer criar — indicação entre membros, ambiente seguro, acompanhamento direto seu."),
      ("Risco da herança maldita", "Deixar pra família processo trabalhista e dívida fiscal em vez de patrimônio seguro. Trazer o plano sucessório."),
    ],
    quote="Se você infartar amanhã pelo estresse dessa bagunça, sua empresa "
          "sustenta sua família por 1 ano? Ou sua esposa vai herdar fiscal na "
          "porta e advogado cobrando dívida?",
    objetivo="Mover a decisão de “gasto empresarial” pra “dever sagrado de proteção familiar”.",
    narr="Tópico dois, dezoito e trinta às dezenove: a cadeira vazia. A "
         "bagunça da empresa rouba presença, sono e futuro dos filhos. Toque "
         "na solidão do topo — é o gancho pro ecossistema empresarial que "
         "você quer criar entre os próprios participantes. A pergunta mais "
         "dura: se você infartar amanhã, sua empresa sustenta a família por "
         "um ano, ou sua esposa herda fiscal na porta e advogado cobrando "
         "dívida? Objetivo: virar a chave de gasto empresarial pra dever "
         "sagrado de proteção familiar."),

  dict(kind="topic",
    kicker="BLOCO 3 · TÓPICO 3 · 19H00–19H30",
    title="A Aliança da Reengenharia — o Re-Pitch",
    bullets=[
      ("Reframe do preço", "“R$30 mil é o valor de 1 contrato mal feito, ou metade de uma multa fiscal.”"),
      ("Convocação", "Não é venda — é convocação de liderança. As fichas já estão na mesa de cada um."),
    ],
    quote="Pega essa caneta agora. Se você tem amor pelo que construiu, pela "
          "sua família e pelo seu nome, assine essa ficha.",
    objetivo="Fechamento das 5 mentorias antes de encerrar a noite.",
    narr="Tópico três, dezenove às dezenove e trinta: a aliança da "
         "reengenharia, o re-pitch definitivo. Reformule o preço: trinta mil "
         "é o valor de um contrato mal feito, ou metade de uma multa fiscal. "
         "As fichas já estão na mesa. A frase final: pega essa caneta agora — "
         "se você tem amor pelo que construiu, pela família e pelo seu nome, "
         "assine essa ficha. Objetivo: fechar as cinco mentorias antes de "
         "encerrar a noite."),

  dict(kind="title",
    kicker="ANTES DO DIA 27",
    title="Checklist final de preparo",
    bullets=[
      "Trazer a história da “grande queda” pro Tópico 1 do Bloco 3 (ainda em aberto).",
      "Fechar o texto do disclaimer e do aplicativo de dívida aberta citado no Tópico 4 do Bloco 2.",
      "Decidir: demonstração da ferramenta OCEO com dado real de um participante exige autorização dele — ou usar exemplo fictício.",
      "Ensaiar em voz alta as frases-chave de cada tópico — são elas que carregam a virada emocional.",
    ],
    narr="Antes do dia vinte e sete, três pontos que ainda estão em aberto no "
         "seu mapa: a história da grande queda, pro primeiro tópico do bloco "
         "três; o texto do disclaimer e do aplicativo de dívida aberta; e a "
         "decisão sobre mostrar dado real de um participante na ferramenta "
         "OCEO — vale pedir autorização antes, ou usar um exemplo fictício em "
         "ordem de grandeza parecida. Por fim, ensaie em voz alta as frases-"
         "chave de cada tópico. Elas carregam a virada emocional do dia. Boa "
         "condução."),
]

# ------------------------------------------------------------------ TTS
def tts(name, text):
    aiff = os.path.join(AUD, name + ".aiff")
    wav = os.path.join(AUD, name + ".wav")
    subprocess.run(["say", "-v", VOICE, "-r", str(RATE), "-o", aiff, text], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", aiff,
                    "-ar", "48000", "-ac", "2", wav], check=True)
    os.remove(aiff)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
              "format=duration", "-of", "csv=p=0", wav],
              capture_output=True, text=True).stdout.strip())
    return wav, d

for i, seg in enumerate(SEGMENTS):
    seg["id"] = "sc%02d" % i
    wav, d = tts(seg["id"], seg["narr"])
    seg["wav"] = os.path.relpath(wav, HERE)
    seg["narr_dur"] = d

# ------------------------------------------------------------------ timeline
LEAD = 0.5
TAIL = 1.2
MIN_DUR = 4.5

t = 0.0
for seg in SEGMENTS:
    dur = max(seg["narr_dur"] + LEAD + TAIL, MIN_DUR)
    seg["start"] = round(t, 3)
    seg["dur"] = round(dur, 3)
    seg["narr_at"] = round(t + LEAD, 3)
    t += dur

TOTAL = round(t, 3)
timeline = dict(fps=FPS, w=W, h=H, total=TOTAL,
                scenes=[{k: v for k, v in s.items() if k != "narr"} for s in SEGMENTS])
json.dump(timeline, open(os.path.join(HERE, "timeline.json"), "w"),
          ensure_ascii=False, indent=1)
print("TOTAL %.1fs (%.1f min) — %d cenas" % (TOTAL, TOTAL / 60, len(SEGMENTS)))
for s in SEGMENTS:
    print("  %-6s start %7.2f  dur %5.2f  narr %5.2f  | %s" %
          (s["id"], s["start"], s["dur"], s["narr_dur"], s.get("title", "")[:40]))

# ------------------------------------------------------------------ HTML
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))

def bullets_html(bl):
    out = []
    for b in bl:
        if isinstance(b, tuple):
            lbl, txt = b
            out.append(f'<div class="bl"><span class="lbl">{esc(lbl)}</span><span class="tx">{esc(txt)}</span></div>')
        else:
            out.append(f'<div class="bl solo"><span class="tx">{esc(b)}</span></div>')
    return "".join(out)

def scene_html(s):
    kind = s["kind"]
    body = ""
    if kind == "title":
        body = f'''
      <div class="kicker">{esc(s["kicker"])}</div>
      <h1 class="tt big">{esc(s["title"])}</h1>
      <div class="rule"></div>'''
        if "sub" in s:
            body += f'<div class="sub">{esc(s["sub"])}</div>'
        if "bullets" in s:
            body += f'<div class="bullets">{bullets_html(s["bullets"])}</div>'
    elif kind == "divider":
        body = f'''
      <div class="kicker">{esc(s["kicker"])}</div>
      <h1 class="tt big">{esc(s["title"])}</h1>
      <div class="rule"></div>
      <div class="sub">{esc(s["sub"])}</div>'''
    else:  # topic
        body = f'''
      <div class="kicker">{esc(s["kicker"])}</div>
      <h1 class="tt">{esc(s["title"])}</h1>
      <div class="rule"></div>
      <div class="bullets">{bullets_html(s["bullets"])}</div>'''
        if "quote" in s:
            body += f'<div class="quote">&ldquo;{esc(s["quote"])}&rdquo;</div>'
        if "objetivo" in s:
            body += f'<div class="obj"><span>OBJETIVO&nbsp;·</span> {esc(s["objetivo"])}</div>'

    return f'''<div class="scene {kind}" id="{s["id"]}">
  <div class="brand"><img src="assets/leao.png" alt=""><span>GILBERTO SENA</span></div>
  <div class="content">{body}</div>
</div>'''

HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#0F1419}}
  #root{{position:relative;width:{W}px;height:{H}px;background:#0F1419;
        font-family:'Inter',sans-serif}}
  .scene{{position:absolute;inset:0;opacity:0}}
  .brand{{position:absolute;left:70px;top:52px;display:flex;align-items:center;gap:14px}}
  .brand img{{height:42px;width:auto}}
  .brand span{{color:#F4F1EA;font-size:17px;font-weight:800;letter-spacing:.26em}}
  .content{{position:absolute;left:70px;right:70px;top:180px;bottom:70px}}

  .kicker{{color:#C9A227;font-size:18px;font-weight:800;letter-spacing:.18em}}
  h1.tt{{margin-top:16px;font-family:'Fraunces',serif;font-weight:700;
        font-size:46px;line-height:1.15;color:#F4F1EA;letter-spacing:-.01em;
        max-width:1500px}}
  h1.tt.big{{font-size:58px}}
  .rule{{margin-top:22px;width:84px;height:3px;background:#C9A227}}
  .sub{{margin-top:22px;font-size:24px;font-weight:500;line-height:1.5;
        color:#C9C4B8;max-width:1350px}}

  .bullets{{margin-top:30px;display:flex;flex-direction:column;gap:18px;max-width:1620px}}
  .bl{{display:flex;gap:22px;align-items:baseline}}
  .bl .lbl{{flex:0 0 340px;color:#C9A227;font-size:17px;font-weight:800;
        letter-spacing:.03em;line-height:1.4}}
  .bl .tx{{flex:1;color:#EDEAE1;font-size:20px;font-weight:500;line-height:1.5}}
  .bl.solo .tx{{color:#EDEAE1;font-size:21px}}
  .bl.solo::before{{content:'—';color:#C9A227;font-weight:800;margin-right:2px}}

  .quote{{margin-top:26px;border-left:3px solid #C9A227;padding:4px 0 4px 24px;
        font-family:'Fraunces',serif;font-style:italic;font-size:25px;
        line-height:1.45;color:#F4F1EA;max-width:1450px}}
  .obj{{margin-top:22px;font-size:16px;font-weight:500;color:#9a9384;
        letter-spacing:.02em}}
  .obj span{{color:#C9A227;font-weight:800;letter-spacing:.14em}}
</style></head><body>
<div id="root">
{"".join(scene_html(s) for s in SEGMENTS)}
</div>
<script>
const TL = {json.dumps(timeline, ensure_ascii=False)};
const clamp01 = x => x < 0 ? 0 : x > 1 ? 1 : x;
function seek(t){{
  let sc = TL.scenes[0], local = 0;
  for (const s of TL.scenes){{
    if (t >= s.start){{ sc = s; local = t - s.start; }}
  }}
  for (const s of TL.scenes){{
    const el = document.getElementById(s.id);
    if (el) el.style.opacity = '0';
  }}
  const el = document.getElementById(sc.id);
  const fin = clamp01(local / .5);
  const fout = clamp01((sc.dur - local) / .4);
  el.style.opacity = Math.min(fin, fout);
}}
window.__seek = seek;
window.__ready = true;
seek(0);
</script></body></html>"""
open(os.path.join(HERE, "video.html"), "w").write(HTML)
print("video.html escrito")

# ------------------------------------------------------------------ mux.sh
inputs = []
fc = []
for i, s in enumerate(SEGMENTS):
    idx = i
    inputs.append(f'-i "{s["wav"]}"')
    ms = int(s["narr_at"] * 1000)
    fc.append(f'[{idx}]adelay={ms}|{ms}[a{idx}]')
amix_ins = "".join(f"[a{i}]" for i in range(len(SEGMENTS)))
fc.append(f'{amix_ins}amix=inputs={len(SEGMENTS)}:normalize=0,'
          f'dynaudnorm=p=0.7:s=6,alimiter=limit=0.95[mix]')
filt = ";".join(fc)

MUX = f"""#!/bin/bash
set -e
cd "$(dirname "$0")"
FPS={FPS}
TOTAL={TOTAL}

ffmpeg -y -loglevel error {" ".join(inputs)} \\
  -filter_complex "{filt}" -map "[mix]" -t $TOTAL -ar 48000 -ac 2 audio/mix.wav

ffmpeg -y -loglevel error -framerate $FPS -start_number 0 -i frames/f-%05d.png \\
  -i audio/mix.wav \\
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow \\
  -c:a aac -b:a 192k -movflags +faststart -shortest \\
  "Estudo - Reengenharia Empresarial (mapa executivo).mp4"

echo "OK -> Estudo - Reengenharia Empresarial (mapa executivo).mp4"
"""
open(os.path.join(HERE, "mux.sh"), "w").write(MUX)
os.chmod(os.path.join(HERE, "mux.sh"), 0o755)
print("mux.sh escrito")

# -*- coding: utf-8 -*-
"""
Audio-guia (locucao continua) da apresentacao de palco da Imersao
Reengenharia Empresarial, a partir dos 3 slides finais que o Gilberto
montou (Downloads: "! Bloco...1.pptx", "2 Bloco...2.pptx", "3 Bloco...3.pptx").

Narra bloco a bloco, topico a topico, na ordem exata dos slides: o que
aparece na tela + o que ele fala (das notas do apresentador) + as
citacoes de impacto na integra, pra ensaio pessoal. Audio only, sem video.
"""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(HERE, "audio")
os.makedirs(AUD, exist_ok=True)

VOICE = os.environ.get("VOICE", "Luciana")
RATE = int(os.environ.get("RATE", "182"))
GAP_S = 0.9  # silencio entre segmentos

SEGMENTS = [
("00-intro", """
Isso aqui é o áudio-guia da sua apresentação de palco pra imersão Reengenharia Empresarial.
Vou percorrer os três blocos na ordem exata dos seus slides — o que aparece na tela, e o que
você fala em cada momento. Usa pra rodar mentalmente antes do dia 27.
"""),

("01-bloco1-intro", """
Bloco um, de manhã, das nove às doze e meia. Abertura: boas-vindas aos vinte empresários,
seu posicionamento de anos de estrada, e o aviso de que isso não é palestra motivacional.
Depois, o mapa da manhã: cinco degraus até o almoço.
"""),

("02-b1-topico1", """
Tópico um, nove às nove e meia: o sofisma do faturamento, a ilusão da empresa forte. Você
quebra o ego da sala sem agressividade, com a autoridade de quem tem estrada. A pergunta
direta: "Você prefere faturar dez milhões e ver oitocentos mil sumirem em imposto errado e
passivo — ou ter uma estrutura enxuta e blindada?" Pausa. Deixa o silêncio trabalhar.

Depois você mostra a diferença entre faturamento e lucro, entre dinheiro da empresa e
dinheiro do dono. Na tela: de um lado, quinhentos mil por mês e a frase "eu faturo, então eu
sei gerir e estou protegido"; do outro, margem líquida mais caixa — é isso que alimenta a
família, não o número da nota fiscal. Fecha com: faturamento sem Reengenharia é apenas um
risco maior.

Depois entra a tabela — o mesmo mês de janeiro visto de duas óticas. Na demonstração de
resultado: lucro de quarenta mil, margem de quarenta por cento, excelente. No banco: o
cliente ainda não pagou, o fornecedor já foi pago à vista, e o caixa fica negativo em
sessenta mil. Duas fotografias da mesma empresa — uma mostra lucro, a outra mostra risco de
quebrar.
"""),

("03-b1-topico2", """
Tópico dois: a armadilha de 2027, o colapso silencioso do split payment. A reforma
tributária não é mudança de imposto, é reajuste de sobrevivência no fluxo de caixa — o
modelo atual morre em 2027.

Na tela, o mecanismo: hoje, o cliente paga cem por cento na sua conta, e o caixa trabalha
por trinta a quarenta dias até a guia vencer. Em 2027, no PIX ou no cartão, a retenção já
acontece no ato — o Leão morde primeiro, e o líquido que sobra encolhe o capital de giro.
Impacto direto no lucro presumido e no setor de serviços.

A frase: "Se você usava o prazo entre o faturamento e o vencimento da guia pra pagar a
folha, em 2027 sua empresa fecha em trinta dias. O Leão vai morder a fatia dele no
milissegundo do PIX. Sua empresa tem fôlego pra rodar assim?"

Depois, um respiro — uma boa notícia, mas com ressalva — antes de seguir pro próximo
tópico.
"""),

("04-b1-topico3", """
Tópico três: a cegueira operacional, o dono que virou síndico de luxo. Ele acha que faz
gestão, mas só apanha da operação — paga conta, gera boleto, apaga incêndio.

A tela mostra o dia do dono: quatorze horas por dia preso no operacional, isso não é
gestão. Gera boleto, apaga incêndio, paga conta, refém de fornecedor, escravo da equipe,
centraliza tudo — exaustão, sem margem real. Pergunta pra sala: alguém se identifica?

A frase: "Você não montou um negócio pra trabalhar mais do que todos os seus funcionários
juntos. Você construiu uma prisão com o seu CNPJ. Se você se afastar trinta dias pra cuidar
da saúde, a empresa rui."

Aqui entra a sua história pessoal — a distribuidora de peças, a B&B Imports. Eu sei, porque
eu já fui assim.
"""),

("05-b1-topico4", """
Tópico quatro: os três ralos invisíveis, onde o dinheiro está vazando agora. A empresa não
quebra de uma vez — sangra aos poucos por três perfurações ocultas.

Na tela, um a um: caixa misturado, G dois — pessoa física e jurídica na mesma conta,
pró-labore maquiado, patrimônio pessoal exposto ao Fisco. Pessoas e passivos, G três —
contrato mal estruturado, ação judicial acumulada em silêncio. Ralo tributário, G quatro —
enquadramento errado por anos, porque o contador é gerador de guia, não estrategista
fiscal.

Depois o número: de dez a vinte e cinco por cento do faturamento jogado no lixo por
empresas que achavam que estavam no enquadramento correto — casos reais mapeados em
diagnóstico, sem Reengenharia.
"""),

("06-b1-topico5", """
Tópico cinco: o diagnóstico, o espelho antes do almoço — com QR code na tela. A pergunta
devastadora: "Se o Fisco fizer uma auditoria cruzada hoje, com as ferramentas de
inteligência artificial de 2026 — ou se o split payment entrar em vigor amanhã — o seu
patrimônio pessoal sobrevive, ou é arrastado junto com o CNPJ?" Deixa a sala responder em
silêncio. Avisa: na volta do almoço, o mapa da rachadura exata de cada empresa.

Frase de fechamento da manhã: "Olhem pro prato de vocês e pensem: a estrutura que vocês
montaram protege o futuro da família, ou é um castelo de cartas esperando o vento de
2027?" E o gancho pra tarde: na volta, vamos abrir a caixa preta.
"""),

("07-bloco2-intro", """
Bloco dois, à tarde, das quatorze às dezesseis e trinta. O diagnóstico e a trava de
execução. Título na tela: o mapa do seu próprio negócio — e por que você não conserta
sozinho.
"""),

("08-b2-topico1", """
Tópico um: o despertar da tarde, a quebra da anestesia cerebral. "Vocês responderam
mensagem no almoço, apagaram incêndio pelo celular — isso é a prova viva de que a empresa
não tem estrutura, tem a sua força física segurando as paredes."

O desafio na tela: quem tem coragem de desligar o telefone agora, deixar de cara pra baixo,
e ficar despreocupado até o final do evento? Se você não controla nem o telefone, quem
dirá da empresa. Antes de lançar o desafio, o contexto: imagina se a Meta bloqueia por
trinta dias, se você perde o WhatsApp da empresa, se você é afastado por doença — como fica
o negócio? Pausa dramática, depois o desafio.
"""),

("09-b2-topico2", """
Tópico dois: as perguntas da Reengenharia. Diagnóstico sem ferramenta é conversa fiada —
abre a apostila no Canvas um, a roda da conformidade, os cinco G's: gestão de si,
financeira, pessoas, tributária, parceiros.

Exercício guiado de quinze minutos: nota honesta de um a dez em cada G, desenha o gráfico,
identifica a fatia mais baixa — o ponto cego de maior risco. Depois chama dois ou três à
frente — o de cinquenta mil e o de um milhão por semana — pra lerem a menor nota em voz
alta.

No palco, o apadrinhamento: mão no ombro, voz mansa, olho no olho, o participante de costas
pra turma. "Você pode mentir pra mim. Pode mentir pros seus colegas. Mas você vai conseguir
dormir com essa mentira? Essa nota é verdadeira mesmo?" Depois, os cinco porquês, até a
ficha cair — e os outros se veem naquele participante.
"""),

("10-b2-topico3", """
Tópico três: a equação da margem oculta, onde o dinheiro realmente fica. Margem ilusória:
na cabeça, quinze por cento; na realidade, dois por cento — treze pontos evaporam em
passivo, retrabalho e bitributação. Contabilidade de guia só serve pro governo;
contabilidade estratégica recupera a margem do dono.

Exemplos de reorganização societária e ajuste de regime que devolveram centenas de milhares
de reais no primeiro trimestre. E então, a demonstração ao vivo: os números de um
voluntário da plateia, no telão, na ferramenta que você desenvolveu em anos de trabalho.
Clareza que ninguém nunca deu — e a ferramenta entra como bônus estratégico da mentoria,
quinze dias de acesso. Objetivo: os outros ficam com inveja de quem foi na frente.
"""),

("11-b2-topico4", """
Tópico quatro: a armadilha do faça você mesmo, a trava da execução. Momento divisor de
águas — desmontar o "amanhã eu mando meu contador arrumar isso" antes do pitch.

Os três caminhos ingênuos, um a um: fazer sozinho — se o dono senta pra estudar legislação
e reestruturar passivo, quem vende e traz cliente? Delegar ao contador atual — ele teve
cinco, dez anos pra fazer isso e não fez, é gerador de guia, não estrategista. Entregar ao
gerente financeiro — não tem visão de dono nem autoridade jurídica pra renegociar dívida ou
blindar patrimônio.

Depois o gatilho das férias: quantos aqui tiram férias de verdade, vinte, trinta dias, sem
a empresa travar? Suas fotos viajando de moto com a esposa. É a ponte pro pitch.

A frase-ponte: "Você já sabe onde está o furo do seu balde. Vai continuar tampando com o
dedo enquanto o balde afunda, ou vai deixar quem tem estrada assumir a Reengenharia da sua
casa?"
"""),

("12-b2-pitch", """
O pitch: o projeto executivo de Reengenharia. Entrada imediata depois do tópico quatro, sem
pausa. Posicionamento: não é curso, é acompanhamento executivo — mentoria de noventa dias,
conduzida por você e seu time sênior.

A aliança de noventa dias, em três blocos na tela: na sua mesa — auditoria dos cinco
pilares dentro da empresa, com seu time jurídico e contábil; torneiras fechadas — fim da
sangria nos três ralos, lacrados; blindada pra 2027 — empresa cem por cento preparada pro
choque tributário e do split payment. Investimento: trinta mil reais. Escassez real: cinco
cotas, pelo acompanhamento direto.
"""),

("13-bloco3-intro", """
Bloco três, à noite, das dezoito às dezenove e trinta. A decisão do legado. Título na tela:
o que você construiu protege quem você ama — ou os deixa como reféns? Este é o cenário de
resistência total, se ninguém comprou no pré-pitch. Você troca a postura de consultor pela
de mentor sênior — a pregação do legado.
"""),

("14-b3-topico1", """
Tópico um: o preço oculto da omissão, a parábola da covardia. A não-decisão é a pior
decisão possível — adiar a Reengenharia é preguiça e irresponsabilidade com a própria
história. Aqui entra a história da grande queda.

Ancoragem em Mateus vinte e cinco, vinte e um, a parábola dos talentos: "foste fiel no
pouco, sobre o muito te colocarei." Deus te deu um negócio, funcionários, o pão da família
— gerir esse patrimônio com desleixo não é falta de tempo, é infidelidade na gestão do
pouco.

A frase: "Vamos ser honestos de homem pra homem? Você não vai pensar em nada. Vai voltar
pra rotina, engolido pelos mesmos incêndios de sempre, até o Fisco bater na porta ou a
margem zerar." A não-decisão é a pior decisão possível.
"""),

("15-b3-topico2", """
Tópico dois: a cadeira vazia, a família pagando a conta do CNPJ. A empresa bagunçada não
rouba só dinheiro — rouba presença, sono, saúde, o futuro dos filhos e da esposa.

Três feridas na tela: a solidão do topo, ninguém pra desabafar, o estresse descontado em
casa; a herança maldita, deixar pra família processo trabalhista e dívida fiscal em vez de
patrimônio seguro; o plano sucessório inexistente — se você faltar, quem assume? Sem
sucessão, o espólio vira campo de batalha. A resposta que você oferece: um grupo forte de
empresários de verdade, ninguém caminha mais sozinho.

Tom de voz baixo, olho no olho: "quando você chega em casa às vinte e uma, exausto, de
cabeça quente, quem paga essa conta é sua esposa e seus filhos." E a pergunta mais dura:
"Se você infartar amanhã pelo estresse dessa bagunça, sua empresa sustenta a família por um
ano? Ou sua esposa vai herdar fiscal na porta, advogado cobrando dívida, funcionário
processando o espólio?" Silêncio absoluto. A decisão vira dever sagrado de proteção
familiar, não gasto empresarial.
"""),

("16-b3-topico3", """
Tópico três: a aliança da Reengenharia, o re-pitch definitivo. Não é contratação comercial
— é uma aliança de proteção de noventa dias, você assumindo a responsabilidade junto com o
dono.

O reframe do preço: trinta mil reais é o valor de um contrato mal feito que se assina numa
semana qualquer; é metade de uma multa fiscal se a casa não estiver arrumada pra 2027; e
dizer que está caro pra salvar o patrimônio de uma vida inteira é uma piada. "Eu estou
oferecendo minha estrada, meu nome, meu time jurídico e contábil — pra sentar do seu lado,
tirar esse peso das suas costas e blindar o seu legado."

Fechamento: as fichas já estão na mesa de cada um. "Pega essa caneta agora. Se você tem
amor pelo que construiu, pela família e pelo seu nome — assine essa ficha. Nós começamos a
Reengenharia da sua empresa esta semana." E o fecho seco: eu não aceito ver empresário
sério quebrando por omissão.
"""),

("17-encerramento", """
Duas coisas rápidas pra você conferir antes do dia. No bloco dois, o material fala em
quarenta anos de estrada; já em outros pontos mais recentes, aparece vinte anos. Vale
igualar esse número em todos os blocos, pra não travar na hora H. E o percentual de
vazamento aparece como dez a dezoito por cento em algumas anotações, e dez a vinte e cinco
por cento na tela do tópico quatro do bloco um — também vale fechar um número só.

Fora isso, o fluxo está redondo: choque de manhã, diagnóstico e trava à tarde, decisão de
legado à noite. Boa condução.
"""),
]

def tts(name, text):
    text = " ".join(text.split())
    aiff = os.path.join(AUD, name + ".aiff")
    wav = os.path.join(AUD, name + ".wav")
    subprocess.run(["say", "-v", VOICE, "-r", str(RATE), "-o", aiff, text], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", aiff,
                    "-ar", "48000", "-ac", "2", wav], check=True)
    os.remove(aiff)
    return wav

wavs = []
for name, text in SEGMENTS:
    print("gerando", name, "...")
    wavs.append(tts(name, text))

# silencio entre segmentos
silence = os.path.join(AUD, "_silence.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                "-i", f"anullsrc=r=48000:cl=stereo", "-t", str(GAP_S), silence], check=True)

concat_list = os.path.join(AUD, "_concat.txt")
with open(concat_list, "w") as f:
    for i, w in enumerate(wavs):
        f.write(f"file '{os.path.abspath(w)}'\n")
        if i < len(wavs) - 1:
            f.write(f"file '{os.path.abspath(silence)}'\n")

OUT = os.path.join(HERE, "Audio-guia - Imersao Reengenharia Empresarial.mp3")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                "-i", concat_list, "-c:a", "libmp3lame", "-b:a", "192k", OUT], check=True)

dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", OUT], capture_output=True, text=True).stdout.strip()
print("OK ->", OUT)
print("duracao: %.1f min" % (float(dur) / 60))

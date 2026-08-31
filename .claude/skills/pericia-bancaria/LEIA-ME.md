# Perícia Bancária Revisional — agente do Gilberto

Skill portátil de perícia contábil-financeira de contrato bancário, para o
Gilberto usar na conta dele. **Não é aplicação**: é uma pasta com instruções,
motor de cálculo e referência jurídica, que roda no Claude.ai, no Claude Code
ou pela API sem alteração.

Origem: áudio do Gilberto em 31/08/2026, transcrito em
`dados/biblioteca/gilberto-pericia/pericia-pericia.md`. O que ele pediu:

> "eu subo o contrato do cliente e falo: gere pra mim uma perícia contábil
> financeira desse cliente baseado no modelo que eu mandei, com os cálculos"

⚠️ **Escopo é perícia bancária revisional, e só.** Perícia criminal foi
cogitada e descartada pelo Cid em 31/08 ("eu que viajei") — o áudio do
Gilberto não menciona criminal em momento nenhum.

---

## Estado

| Fase | O quê | Estado |
|---|---|---|
| 1 | Motor de cálculo determinístico | ✅ 103 asserções + gabarito externo do BACEN |
| 2 | Referência jurídica conferida na fonte | ✅ 12/12 por máquina, 2 pendentes à mão |
| 3 | A Skill (ficha → cálculo → laudo) | ✅ `SKILL.md` + `estrutura-do-laudo.md` |
| 4 | Validação | ⚠️ **parcial** — ver abaixo |
| 5 | Empacotamento | ✅ `node empacotar.mjs` → 60 KB |

★ **O Gilberto não tem modelo de laudo que queira seguir** ("só quer um que
funcione"). Então a régua do documento passou a ser o **art. 473 do CPC**,
conferido na fonte — o que é mais defensável do que o modelo pessoal de
qualquer perito, e não dependeu de esperar por ele.

⚠️ **A Fase 4 está PARCIAL, e isso não pode ser esquecido.** Estão validados:
a **matemática**, contra a Calculadora do Cidadão do BACEN (15 casos); o
**direito**, contra STJ e Planalto (12 verbetes); e os **achados**, contra um
contrato de exemplo com gabarito plantado (11/11). O que **não** está validado
é o resultado ponta a ponta contra uma perícia real, produzida e defendida por
um perito — e nenhum desses três substitui aquilo. Até lá, o perito confere o
laudo antes de assinar, e a `SKILL.md` diz isso por escrito.

⚠️ **Também não está coberto: PDF escaneado de verdade.** O contrato de
exemplo é texto limpo. Layout de banco real, qualidade de digitalização e a
nomenclatura que cada instituição dá às mesmas tarifas só um contrato real
resolve.

## Como se confere

```bash
node motor/testes.mjs           # 103 — matemática pura
node motor/testes-achados.mjs   # 99  — camada pericial
node motor/conferir-lei.mjs     # 12/12 contra STJ e Planalto
node motor/conferir-bacen.mjs   # 15 casos contra a Calculadora do Cidadão
node motor/exemplo.mjs          # gabarito impresso, para conferir com o olho
node motor/gerar-contrato-exemplo.mjs   # contrato fictício + gabarito de achados
node empacotar.mjs              # gera pericia-bancaria.zip pra instalar
node motor/conferir-lei.mjs --baixar   # imprime o texto oficial de cada verbete
```

---

## A tese do produto

★ **A IA não faz a conta — ela roda a conta.** Modelo de linguagem não calcula
360 parcelas de amortização: ele escreve um número plausível. Num laudo
pericial o número **é** o produto, e quem assina é o Gilberto como perito
judicial. Por isso a matemática toda vive em `motor/`, determinística e
testada, e o modelo só monta o texto em cima do que o motor devolveu.

★ **O laudo forte não é "Tabela Price é ilegal".** Essa tese não sustenta
sozinha — a Súmula 539/STJ permite capitalização expressamente pactuada, e o
Tema 27 exige abusividade "cabalmente demonstrada no caso concreto". O que
vale dinheiro é o **checklist de achados, cada um com o número atrás**:
capitalização, taxa efetiva do fluxo, CET, tarifas, seguro, multa, comissão
de permanência, amortização negativa.

★ **O checksum da leitura sai de graça da própria matemática.** Se valor
financiado, taxa e prazo não reproduzem a prestação impressa no contrato, ou
o OCR trocou um dígito ou há encargo embutido não declarado. `conferirEntrada`
**barra a perícia** nos dois casos. Contrato bancário costuma ser PDF
escaneado, e leitura por visão erra dígito — foi medido no app do Max.

---

## Armadilhas já pagas nestas duas fases

### Matemática

☠️ **A tabela de juros simples não pode usar `juros = saldo × i`.** Calcular a
prestação sem capitalizar e depois montar a tabela capitalizando é se
contradizer dentro da peça: o saldo não zera, a última prestação vira bolha e
o método "sem juros compostos" sai **mais caro** que o Price. No desconto
racional simples quem amortiza é `P/(1+i·k)`.

☠️ **TIR por bisseção, nunca Newton-Raphson.** Newton diverge em fluxo
mal-comportado e devolve NaN ou raiz absurda sem avisar. E a bisseção precisa
**encurralar a raiz numa grade primeiro**: `(1+(−0,99))^360` é `Infinity` em
IEEE-754, e a guarda de finitude matava a busca — o financiamento imobiliário,
que é o caso que mais importa, era o único que não calculava.

☠️ **A tolerância do checksum não pode ser fixa em centavos.** Medido contra a
Calculadora do Cidadão do BACEN: em 15 casos, 10 divergiram do nosso cálculo
direto, e a maior diferença foi de **7 centavos** — numa prestação de
R$ 56.687. O erro **cresce com o valor**, porque quem arredonda é o
coeficiente, que multiplica o principal. Com o teto fixo de 2 centavos que
estava lá, um contrato legítimo de valor alto seria barrado como "os números
não fecham": a perícia pararia sozinha apontando um defeito inexistente, e
justamente no contrato que mais importa. Hoje é
`toleranciaDeArredondamento()`, proporcional com piso de 5 centavos.

⚠️ **Não se persegue o algoritmo do BACEN.** Nenhuma hipótese de arredondamento
(round/ceil/trunc em 6 a 9 casas do coeficiente) reproduziu as 18 respostas
dele — a melhor acertou 11. E não adiantaria: cada banco arredonda do seu
jeito, e **a prestação do laudo é a impressa no contrato**, nunca a que a
gente calcula. O `conferir-bacen.mjs` prova que a FÓRMULA é a mesma, e fórmula
errada não erra centavos, erra reais.

☠️ **`formatarBRL(null)` não pode devolver "R$ 0,00".** Num laudo, zero é a
afirmação de que nada é devido, e ninguém confere se aquele zero veio de uma
conta ou de um campo vazio. Devolve `—`.

☠️ **SAC tem prestação decrescente: "diferença por prestação" não existe.**
Saía `−R$ 491,87` ao lado de uma economia total de `R$ 4.449` — a mesma tabela
dizendo que o cenário é mais caro e mais barato. Hoje o campo vem nulo e o
laudo diz por quê.

☠️ **Cenário duplicado.** Quando a taxa anual declarada é o duodécuplo,
`anual/12` **é** a taxa mensal: o cenário "sem capitalizar" saía idêntico ao
de juros simples, centavo a centavo. Duas colunas com o mesmo número num laudo
é a primeira coisa que o assistente técnico do banco aponta.

★ **As quatro foram pegas pelo GABARITO IMPRESSO (`motor/exemplo.mjs`), não
pelos testes** — que estavam todos verdes. Teste prova que o código faz o que
o teste mandou; o gabarito mostra o número.

### Direito

☠️ **A conferência contra a fonte derrubou TRÊS coisas que eu tinha escrito de
cabeça, e nenhuma parecia errada:**

1. **Tema 618** — o acórdão diz "celebrados **até** 30/04/2008 era válida a
   pactuação". Eu implementei "vedada **a partir de** 30/04/2008". Um dia de
   diferença **inverte a conclusão** sobre o contrato do cliente. E havia um
   teste fossilizando o erro, porque nasceu da mesma suposição que o código.
2. **Súmula 472** — o verbo não é "vedada a cumulação". É **"exclui a
   exigibilidade"** dos juros e da multa, e limita o valor da comissão à soma
   dos encargos. Efeito diferente, duas contas em vez de uma.
3. **Tema 958** — a tarifa de avaliação do bem e o ressarcimento de registro
   são **VÁLIDOS em regra**; a abusividade é a exceção. Eu tinha a moldura
   invertida: o laudo acusaria justamente o que a Corte validou, e o banco
   derrubaria o ponto citando o mesmo tema.

☠️ **Não existe tese firmada dizendo "taxa média de mercado".** Conferido nos
Temas 24 a 28: nenhum traz esse critério no enunciado. A comparação com a
média do BACEN é **elemento de prova** da abusividade no caso concreto, não
limiar jurisprudencial. Por isso o limiar é **parâmetro declarado do perito**,
aparece no laudo junto com o resultado, e a faixa intermediária é
**inconclusiva** — nunca "regular".

☠️ **A Resolução CMN 3.517/2007 foi revogada pela 4.881/2020** (vigência
01/02/2021). Citar a 3.517 num contrato de 2023 é invocar norma revogada; e
citar a 4.881 num contrato de 2015 é o erro inverso. A norma sai da **data do
contrato** (`normaCET`), nunca cravada.

### Gabarito externo

★ **A Calculadora do Cidadão do BACEN é o único juiz independente que temos.**
As baterias provam que o código faz o que o teste mandou — e o teste nasceu da
mesma suposição que o código. Contra erro de fato, teste é cego por construção
(foi assim que a data do Tema 618 passou verde invertida). A calculadora é
oficial, pública e não sabe nada do nosso código.

★ E vale **dentro do laudo**: "o cálculo confere com a Calculadora do Cidadão
do Banco Central" é frase que o assistente técnico do banco não derruba.

☠️ **Ela exige cookie de sessão (JSESSIONID).** Sem ele o BACEN responde
**HTTP 200 com o formulário vazio** — "deu certo" sem resposta nenhuma. Uma
leitura ingênua veria 200 e concluiria que a conferência passou.

⚠️ A bateria carrega **casos duros de propósito** (os que mais divergiram numa
varredura de 15). Bateria só com caso fácil passa sempre e não avisa nada.

### Ferramenta de conferência

⚠️ **`scon.stj.jus.br` devolve 403.** O host que responde é
`processo.stj.jus.br`. Súmulas em `/SCON/sumstj/toc.jsp?livre=@num='N'`, temas
repetitivos em `/repetitivos/temas_repetitivos/pesquisa.jsp?...cod_tema_inicial=N`.

⚠️ **STJ e Planalto servem latin-1.** Decodificar como UTF-8 estraga todo
acento e nenhuma âncora casa. O STJ ainda marca o termo buscado com
`<span class=highlightBrs>` **no meio da frase** — tirar tag antes de comparar.

☠️ **Buscar no texto normalizado e recortar no original com o mesmo índice
devolve o dispositivo errado.** A normalização muda o comprimento (NFD separa
acento, o filtro colapsa espaço). No CDC, a busca por "dois por cento do valor
da prestação" achou o trecho e o recorte devolveu um pedaço do § 2º — texto
real, da lei certa, do **dispositivo errado**. Num laudo isso vira citação
errada com cara de citação conferida. Resolvido com mapa de índices
(`normalizarComMapa`).

⚠️ **Fonte fora do ar não reprova a conferência** — é hiccup de rede, não
defeito da referência. Só divergência de âncora reprova.

---

## Estrutura

## Como entregar ao Gilberto

```bash
node empacotar.mjs   # → pericia-bancaria.zip (61 KB, 12 arquivos)
```

O empacotador **recusa empacotar** se o frontmatter violar as regras publicadas
da Anthropic (`name` só minúscula/número/hífen, ≤64; `description` ≤1024;
SKILL.md <500 linhas) ou se algum caminho sair com barra invertida.

☠️ **O ZIP É ESCRITO NA MÃO, e não com `Compress-Archive`.** O cmdlet do
PowerShell grava os caminhos com **barra invertida** (`motorchados.mjs`). O
sandbox onde a Skill roda é Linux: lá isso não é "pasta motor com arquivo
dentro", é um arquivo solto cujo NOME tem uma barra invertida. A Skill sobe,
aparece instalada, e **não acha o motor** — falha só na hora de calcular, com
cara de outro problema. O 1º pacote saiu exatamente assim.

☠️ **Testar o PACOTE, não a pasta.** Rodar `node motor/testes.mjs` aqui prova a
peça; prova o produto extrair o zip em outro lugar e rodar de lá. É a mesma
lição do `.bat` do GSENA Leads, que foi dado como pronto rodando o Node por
dentro. Conferido: 103 + 99 + 11/11 a partir do extraído.

### Onde ele instala

Na conta dele: **Customize → Skills → Add**, e sobe o zip. Skills existem em
todos os planos (Free, Pro, Max, Team, Enterprise).

⚠️ **Exige `code execution` ligado** — sem isso a Skill instala e não roda o
motor, que é o produto inteiro.

⚠️ **Os nomes acima são os da interface em inglês**, tirados da documentação.
O rótulo em português e a posição exata do interruptor de execução de código
**não foram conferidos numa tela** — confirmar na hora, não decorar daqui.

★ **O teste que não precisa de contrato nenhum:** o gerador está dentro do
pacote, então dá pra pedir *"gere o contrato de exemplo e faça a perícia nele"*.
Isso exercita leitura, checksum, motor, achados e laudo de ponta a ponta, sem
ele ter que arrumar documento.

---

## Estrutura

## Como entregar ao Gilberto

```bash
node empacotar.mjs   # → pericia-bancaria.zip (60 KB)
```

☠️ **O `SKILL.md` tem que ficar na RAIZ do zip.** Zipar a pasta que contém a
pasta cria um nível a mais e a Skill não é reconhecida — sem erro que explique
isso. O empacotador já monta certo; conferir com:

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::OpenRead('...\pericia-bancaria.zip').Entries | % { $_.FullName }
```

⚠️ `exemplos/` **não entra no pacote** — é gerado por script e não é parte da
Skill. Está no `.gitignore` pelo mesmo motivo.

⚠️ **Onde ele sobe o zip:** nas configurações da conta dele, na área de
Capacidades/Skills. ⚠️ O caminho exato da tela muda com o tempo e **não foi
conferido nesta máquina** — confirmar na hora, e não passar print de memória.

---

## Estrutura

```
SKILL.md                as instruções do agente — o que ele instala
empacotar.mjs           gera o zip
motor/
  calculo.mjs           matemática pura: Price, SAC, Gauss, TIR, CET, checksum
  achados.mjs           camada pericial: achados, cenários, apuração
  testes.mjs            95 asserções
  testes-achados.mjs    99 asserções
  conferir-lei.mjs      confere a referência contra STJ e Planalto
  conferir-bacen.mjs    confere a fórmula contra a Calculadora do Cidadão
  exemplo.mjs           gabarito impresso
  gerar-contrato-exemplo.mjs   contrato fictício com gabarito de achados
referencias/
  jurisprudencia.mjs    14 verbetes; texto TRANSCRITO da fonte, nunca de cabeça
  estrutura-do-laudo.md as 13 seções, derivadas do art. 473 do CPC
exemplos/               gerado por script; fora do git e fora do pacote
```

★ **O art. 473 do CPC virou o verbete mais importante do arquivo** (`cpc-473`),
porque é ele que manda no formato. Três consequências diretas: o **inciso III**
exige declarar o método e demonstrar que é aceito (daí a validação contra o
BACEN entrar no laudo); o **inciso IV** exige resposta conclusiva a **todos**
os quesitos, que era um requisito que eu não tinha previsto; e o **§ 2º** veda
opinião pessoal que exceda o exame técnico — que é a base normativa dos três
estados do achado e da recusa a decretar abusividade.

⚠️ **Dinheiro é inteiro em centavos. Data é string `AAAA-MM-DD`.** As duas
regras da casa valem aqui com peso extra: um resíduo de float faz o saldo
nunca zerar, e `new Date('2008-04-30')` volta 29/abr no Brasil — o que jogaria
um contrato do próprio dia 30/04 para o lado errado do Tema 618.

⚠️ **Três estados por achado, nunca dois:** `achado`, `regular`,
`inconclusivo`. Colapsar inconclusivo em regular faz o laudo **afirmar
regularidade sobre o que nem foi examinado** — pior que não achar nada.

⚠️ **O motor não contém texto de lei.** Ele carrega uma **chave**
(`fundamento`), e o verbete mora em `referencias/`. Há teste provando que
nenhuma chave é órfã e que todo verbete conferível tem texto transcrito.

---

## O que falta decidir

- **A taxa média do BACEN entra de onde?** Hoje é campo de entrada
  (`mediaBacenMensal`). A série SGS do BACEN é pública e grátis — vale ligar
  na Fase 3, mas exige rede em tempo de execução.
- **Os dois verbetes do CET (`cet-3517`, `cet-4881`) seguem pendentes de
  conferência à mão** — o BACEN serve PDF atrás de SPA. O conferidor relata
  em vez de fingir que estão conferidos.
- **O modelo de laudo do Gilberto** define a forma do documento final. Sem ele,
  qualquer formato que eu escolha ele vai ter que reescrever.

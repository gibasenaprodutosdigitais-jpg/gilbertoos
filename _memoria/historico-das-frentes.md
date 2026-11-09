# Histórico das frentes

> Trechos tirados do `onde-paramos.md` em 30/out/2026, sem mudar uma palavra, para ele
> ficar só com o que está aberto. Consultar quando o assunto voltar.

---

### ✍️ Decisões de edição que eu tomei, e ele pode reverter

**Afastei peças repetidas.** O Simples Híbrido estava no dia 18, logo depois
do Simples Nacional do dia 17, contando a mesma história. Troquei com o
Revenda de Carros: Híbrido foi pro dia 23.

**Padronizei hashtag.** Três carrosséis vinham com acento e maiúscula
(`#PontoDeEquilíbrio`, `#GestãoFinanceira`). Hashtag com acento divide o
alcance com a versão sem. Todos agora são minúscula sem acento, como o
resto do perfil.

---

### 🔴 O carrossel que eu quase publiquei com número errado

O "5 sinais de que sua empresa parou de crescer" foi publicado em 15/10 às
21h52, mas **a última lâmina dizia "2.000+ empresas recuperadas"** e a
legenda falava em "mais de dois mil casos". O número confirmado por ele,
duas vezes, é **+500**. Corrigi nos dois lugares e re-renderizei antes de
subir.

Depois varri os 42 restantes com `grep` atrás do mesmo erro: **estão limpos**,
era só aquele. Mas a lição fica: **conferir número de autoridade antes de
agendar**, porque o carrossel contradizia o media kit dele.

---

### Legenda queimada: como fazer, porque este ffmpeg não ajuda

Ele pediu legenda nos vídeos em 14/out. **Este ffmpeg não tem libass, nem
`subtitles`, nem `drawtext`.** O caminho que funciona: desenhar a legenda com
PIL, montar uma faixa com alfa em `qtrle`, e compor com `overlay`.

O cortador está em `/tmp/.../scratchpad/bin/cortar2.py` e o motor de legenda
em `legenda.py` — **são de sessão, então se precisar de novo, reescrever.**
O que importa guardar são as três lições:

1. **O Whisper não conhece o vocabulário tributário.** Escreveu `SPIRIT PAIN
   MAN` no lugar de **split payment**, `IES` por **IS**, `CBS E BS` por
   **CBS e IBS**, `SIMPLES HÍBIDO`. Legenda errada na tela derruba autoridade
   mais rápido que legenda nenhuma. **Precisa de dicionário de correção.**
2. **A transcrição não prova que o bip funcionou.** O Whisper ouviu o tom de
   1 kHz e preencheu a palavra pelo contexto, imprimindo `f***` como se
   tivesse escutado. **Conferir no espectro:** a voz tem que cair uns 20 dB
   na janela e o tom aparecer em 1 kHz.
3. **Palavrão: ele decidiu bip.** *"da um bip nos palavroes"*, 14/out. Tom de
   1 kHz sobre a palavra e `F***` escrito na legenda. **"Na raça, na porrada"
   e "se lasque" não são palavrão e ficaram.**

### 🔴 Um bug meu da pele, que pegava 25 carrosséis

Os slides `.light` ficaram com fundo escuro pela pele nova, mas a regra
antiga mantinha o rodapé em cinza-escuro. **Texto escrito no HTML e invisível
na imagem.** Não dava para ver olhando rápido: **só apareceu medindo o
contraste pixel a pixel.** Corrigido nos 38 e os 25 afetados re-renderizados.

---

### Carrossel "Quem é Gilberto Sena": card 5 refeito — 13/out/2026

`saidas/CARROSSEIS/carrossel-quem-e-gilberto-2026-10-06/`, 9 cards regerados.

**Card 5** era a lista de formações e virou **"Antes da empresa, a família"**:
marido da Erica Sena, pai da Jessyka Sena e do Victor Sena, construindo o
legado através da família, o primeiro ministério. A troca resolveu uma
repetição de passagem, porque aquela lista era quase a mesma do card 6.

**Cards 6 e 7 perderam todas as cargas horárias.** Nenhuma restou no
carrossel.

⚠ **Os nomes da família se escrevem SEM acento: Erica, Jessyka, Victor.**
Confirmado por ele. Eu tinha posto com acento seguindo o `quem-e-gilberto.md`,
que também foi corrigido, junto com o capítulo "As sete quedas" do livro.

---

**Diagnosticado em 13/out/2026.** Está ligado e tem destino configurado
("Backups de MacBook Pro", externo e criptografado, 50 GB gravados), **mas o
disco não é conectado desde janeiro de 2024.** Falha de hora em hora em
silêncio, com *"Failed to mount destination"*.

**Enquanto esse HD não for plugado, o Mac não tem backup** além do GitHub, e
o GitHub não guarda vídeo nem áudio.

**Quando ele achar o HD:** plugar, avisar, e eu verifico se montou, confiro a
senha e disparo o backup. **O Mac precisa estar na tomada** — nos registros
aparece "Computer is on battery power" como motivo de pular.

---

### A direção de arte, e as regras que ela segue

**Editorial**, Spectral + Barlow Condensed. A escolha priorizou a leitura de
perfis em tela e uma composição mais confortável que a de slides.

**Sem dourado, de propósito:** ele apareceu nas quatro peças anteriores dele.

**Um acento só, em três claridades.** Papel `#F2EFE9` com `#8C2F27` (7,17:1);
azul `#13283F` com `#D9988B` (6,28:1). Matiz 5° e 10°, ou seja a mesma cor.
O vermelho puro sobre o azul dava 3,37:1 e não servia.

**Três páginas azuis, não duas.** Com duas o azul parece acidente; com três
vira sistema. Registrado no `historico.md` da skill `direcao-de-arte`.

Alternativas medidas e aprovadas, caso ele queira trocar: verde-pinho
`#15241F` (14:1) e grafite-azulado `#1A1B2E` (14,8:1).

### Os retratos são recortados, sem fundo

Feito com a **Vision da Apple**, o mesmo motor do Preview do macOS: local,
sem subir foto para serviço nenhum. A ferramenta ficou em
`scripts/recorta-fundo.swift`, com instruções em `scripts/LEIA-recorte.md`.

⛔ **As fotos de palco NÃO se recorta.** Ali o fundo é a prova: é o telão com
o nome do evento e a plateia.

### 🔴 Três armadilhas que me custaram retrabalho aqui

1. **Eu conferia os PNGs do render, nunca o PDF.** São caminhos diferentes no
   Chromium. Usei `mask-image` em degradê para suavizar a borda das fotos, e
   **no leitor dele as fotos sumiram**, porque PDF não tem máscara nativa.
   **Rasterizar o PDF com PDFKit e olhar**, sempre.
2. **Corte de rosto é geometria, não enquadramento.** A coluna tinha 76mm de
   largura e a foto, esticada pela altura, ficava com 198mm. O rosto media uns
   79mm e **não cabia em posição nenhuma**. A saída foi dar a cada bloco a
   **altura exata da proporção do arquivo**. Mesma coisa na página do palco.
3. **Faixa larga não cabe um rosto.** Tentei uma faixa 2,7:1 e ela comia o
   topo da cabeça e o queixo. Virou coluna lateral.

### Os eventos confirmados, e o que falta

**Sete eventos entraram como palestra.** O mais raro é o **Dubai Experience,
1 a 5 de novembro de 2023**: o cartaz oficial traz *"PALESTRANTE CONFIRMADO:
GILBERTO SENA"* e o tema foi *Os 5 G's do Empreendedorismo*, metodologia dele.
É a única credencial internacional fora Portugal. Cartaz em
`entrada-videos/palco-e-eventos/cartaz-dubai-experience-2023.jpeg`.

Os outros: **Empreenda Summit Alphaville 2024** (vídeo do
CONECTV com o GC escrevendo "PALESTRANTE"), **PBXP Paraíba Business
Experience, mai/2023** (cartaz com ele ao lado de Roberto Shinyashiki e
Janguiê Diniz), **GoDigital Festival jan/2023** (palavra dele), **Summit Êxito
2022** (foto de palco com plateia) e **Mentoring Day Experience, Portugal**.

✅ **As cidades estão resolvidas, 15/out.** O site `gruposena.com.br` ainda
mostra Parauapebas e Vitória, e ele mandou **desconsiderar**. A lista que
vale é a do kit: **sede em São Paulo, com escritórios no Rio de Janeiro, em
Goiânia e em Belo Horizonte.** Se alguém apontar a diferença, o site é que
está velho.

**Cargo verificado:** ele é **Diretor de Compliance do Instituto Êxito de
Empreendedorismo**, gestão 2025/2030. Confirmei lendo as 52 fotos da página
oficial da diretoria, onde ele aparece entre Janguiê Diniz (Presidente) e
Celso Niskier (Vice-Presidente). O repositório dizia "conselheiro" e **estava
errado**. Print em `entrada-videos/palco-e-eventos/`.

### ❗ Os depoimentos não existem no computador

Ele pediu os do **Roberto, Tucco, Tiago e Janguiê**. Varri os 20 vídeos que
ele baixou e o PC inteiro. **Achei um**, e os outros três não são depoimento:

- **Tucco**, 15s, apresenta ele como *"um grande expert, o Giba, do Grupo
  Sena"*. **Corta no meio da frase.** Se existir a entrevista inteira, vira o
  melhor do acervo.
- **Shinyashiki**: story de mesa de restaurante. Cita o nome dele numa lista
  de quem estava presente, e o assunto é o pedido de casamento do Stanley
  Bittar. ⛔ **Usar como endosso contraria o aviso do `quem-e-gilberto.md`
  sobre não vender proximidade que não existe.**
- **Tiago Brunet**: é conteúdo do próprio Tiago, não cita o Gilberto.
- **Janguiê**: 11s de bastidor, a transcrição inteira é *"a gente é um beijo
  aqui, ó"*.

**O caminho que funciona é o Drive**, que entrega por link. ⛔ **O Instagram
não:** tentei acesso direto, yt-dlp, a sessão do Chrome dele (travou pedindo
a senha do chaveiro) e o endpoint de incorporação. Devolve casca vazia.

### ✅ Showreel montado — 15/out/2026

`saidas/REELS/showreel-palestrante-2026-10-15/Gilberto-Sena-Showreel.mp4`,
58s, 1080x1920, −14 LUFS. O MP4 não vai pro git (regra do repositório), só o
`LEIA.md`, a `capa.png` e o `_pecas.py`.

**O acervo de palco é de ~3 minutos, não de 5.** O que o arquivo dizia antes
estava errado: as gravações longas de `entrada-videos/longos/` são ele no
carro. De palco existem só os três clipes do Alphaville (120s) e um da
Imersão (61s).

⚠ **Três dos quatro clipes vêm com legenda queimada de outro editor.** Só o
`palco-alphaville-2024-historia.mp4` tem a legenda **fora** da imagem, na
tarja preta: a faixa limpa do palco é `crop=1080:558:0:860`. Os outros têm
legenda em cima da imagem e só servem mudos, como passagem.

**O método da montagem:** uma base única de 49,9s do clipe da história
(18,3s a 68,2s da fonte), com os cartazes entrando por `overlay ...
enable='between(t,a,b)'` **por cima** da base. Assim a fala corre inteira,
sem buraco de áudio, e a imagem do palco volta já em sincronia com a voz —
que é o que quebraria se eu tivesse cortado a base em pedaços. As pontas
(abertura e fecho) entram por concat sem reencode, com áudio mudo a 48 kHz.

⚠ **O Didot do macOS renderiza "e" como "c" no PIL.** Perdi um render nisso.
As serifadas que funcionam: **Hoefler Text**, Baskerville, Charter, Iowan,
Georgia. A condensada boa é **DIN Condensed Bold**.

**Pra melhorar:** precisa de imagem bruta de palco sem legenda. Com 3 ou 4
minutos limpos dá uma peça de 90s com variação de plano.

---

### 🔴 O Time Machine não faz backup desde 29/01/2024

**29/out/2026, 19h20: o HD voltou e o backup completo começou** (~423 GB). **Ainda não terminou:** às 22h44 e à
1h01 de 30/out parou com "device locked", porque a tela apaga em 15 min e o Mac tranca na hora. Deixei a tela acordada
(`caffeinate`) enquanto o backup roda, sem mudar configuração. **Em 30/out à 1h30 estava em 18% da cópia; às 3h20, em 64%, sem nova parada (previsão de terminar perto das 5h).** Antes de firmar, o HD
caiu três vezes, sempre quando começava a gravar (o kernel dizia "media is not present"). Firmou depois que ele
replugou o cabo. **Às 11h30 de 30/out já não estava rodando. Falta ele confirmar pelo ícone do Time Machine se terminou** (o `tmutil latestbackup` pede Acesso Total ao Disco); se não, ver se o HD caiu de
novo. Se cair de novo, a suspeita é o cabo ou o próprio HD (sem uso desde 2024). A senha do HD não é necessária: os
dois volumes abrem sozinhos.

---

## Imersão AME, 14 e 15/nov/2026 (cancelada em 8/nov/2026)

Saiu do `onde-paramos.md` em 8/nov, quando a AME virou assessoria completa e a imersão foi cancelada. Registro como
estava no último dia:

**Imersão AME, 14 e 15/nov/2026, São Paulo** (pedido dele em 21/out; o nome "Imersão AME" é decisão dele de 26/out).
Gilberto e Dr. Stanley, os quatro pilares para clínicas e consultórios médicos, odontológicos e de estética. **Tudo da
imersão fica em `sb/AME/`** (pasta pedida por ele em 26/out).

- **Decidido por ele:**
  - Espaço da **Rede Vivax de Televisão**, **50 vagas**, domingo 15/11 (feriado) confirmado (21/out).
  - **"De R$ 3.999 por R$ 499"** pelos dois dias (26/out; antes era "de R$ 3.000 por R$ 599"; o jurídico liberou o "de").
    **Preço fora dos posts** (27/out): a arte mostra só data, vagas e o link.
  - Oferta do fim do dia 2 (21/out): Choque de Ordem e Caixa R$ 35.000 em 6x no cartão ou R$ 30.000 à vista no pix,
    **12 vagas**; Escala Blindada R$ 60.000 em 12x no cartão ou R$ 50.000 à vista no pix, **8 vagas** (20 no máximo);
    o Club SB fica fora. **Abatimento dos R$ 499 para quem fechar até as 23h de 15/11.**
  - Logo (26/out): embaixo do AME, **"Administração, Marketing e Escala"** em dourado e **"Medicina · Odontologia ·
    Estética"** em prata (saiu o "Assessoria Médica Empresarial"). Ele sabe que AME em SP é o Ambulatório Médico de
    Especialidades do estado e manteve.
  - Inscrição por **link de pagamento**: https://mpago.la/11BizwZ (Mercado Pago, 27/out).
  - Quiz (27/out): até R$ 30 mil e de R$ 30 a 70 mil vão pra página de obrigado; de R$ 70 a 120 mil e acima de
    R$ 120 mil vão pra página de vendas.
- **Pronto:**
  - Cronograma hora a hora no doc https://claude.ai/artifact/5i1kFD51t9amxdeZfpmjmH (privado): dia 1, Gestão e
    Lucratividade com o Gilberto; dia 2, Marketing e Vendas com o Stanley, hot seats e oferta dos programas.
  - Logo, programação, crachás, certificado e artes de divulgação (feed e story; fotos em cor desde 27/out).
  - **Kit do participante** (8 folhas A4: ficha de diagnóstico adaptada pra sala, exercício da margem, decisões dos
    dois dias e os quatro números).
  - **Ficha online AME** (https://claude.ai/artifact/3XuZKa9LcsmVYGx6SYhpdd, privada, com a pergunta do hot seat; banco
    próprio, separado da ficha da SB).
  - **Slides** (26/out, 56, https://claude.ai/artifact/8XLbWYXgZm7w2LLGc6KTbi, privada; também em PowerPoint na pasta),
    feitos só com o método, a ficha, o cronograma e o fichamento da reforma.
  - **Quiz de interesse no ar em https://imersao-ame.vercel.app** (27/out, Vercel, conta apliquepoupe), com
    `/venda.html` (botão do Mercado Pago) e `/obrigado.html`. As respostas vão pro **Google Sheets** (ativo desde 27/out,
    `sb/AME/quiz/google/`; duas planilhas no Drive dele, "Acima de R$ 70 mil" e "Até R$ 70 mil"). Também roda no
    computador (`sb/AME/quiz/`, http://localhost:5180, cópia em `respostas.csv`, fora do GitHub). A versão dentro do
    Claude (https://claude.ai/artifact/8Rmtdk5U8HtJmkmzASEryn) não tem as páginas nem o Google Sheets.
  - **4 reels de teste da imersão publicados em 29/10 às 15h**, os quatro sem falha (Instagram, só pra quem não
    segue, passam pro perfil se forem bem). Ver `sb/AME/divulgacao/reels-de-teste-2026-10-29/LEIA.md`. Dos 6 "Criativos SB", **"Ataque mentoria 2"
    e "Lição política" ficaram de fora** por decisão dele (passam de 3 min; o primeiro diz "20 anos" e cita lei do
    Botox sem base; o segundo é eleição). No vídeo CRTV AME 3 ele fala em **cinco pilares**, mas o método é quatro.
  - **2º lote: 12 reels de teste publicados em 31/10 (~19h45)**, CRTV AME 5 a 16, os doze conferidos (é ele, sem preço,
    "+15 anos"). Na legenda, "teu/tua/contigo" virou "seu/sua/com você". Ver `sb/AME/divulgacao/reels-de-teste-2026-10-31/LEIA.md`.
  - **Banner da live de pré-imersão, 03/11 (terça) às 21h** (01/nov): feed e story em `sb/AME/divulgacao/live-pre-imersao-*.png`,
    com os dois. A live é **no Instagram do Dr. Stanley, @stanleybittar** (decisão e @ dele, 01/nov), com o @ de cada um embaixo da foto; botão
    "Ative o lembrete". Pronto pra postar. As 12 perguntas do Stanley pra live estão em
    `sb/AME/divulgacao/live-pre-imersao-perguntas.md` (e em PDF, uma folha A4).
- **Falta:**
  - ✅ Link de inscrição na bio do Instagram (ele confirmou em 30/out). Falta só o story e o WhatsApp, se ele quiser.
  - **Contratos: 3 modelos prontos em 30/out** em `sb/AME/contratos/` (termo de inscrição da imersão, Choque de Ordem e
    Caixa, Escala Blindada), com cláusula de imagem e vídeo (pedido dele). Falta o advogado conferir e preencher razão
    social, CNPJ e o que está entre colchetes (lista no `LEIA.md` de lá).
  - Regras de publicidade do CFM/CFO: **levantadas em 30/out** em `sb/AME/regras-publicidade-cfm-cfo.md`. Falta o advogado
    conferir (principalmente o CFO) e o Stanley ajustar os slides de Marketing e Vendas. Dentista não pode anunciar preço;
    médico pode.
  - Dele, pros slides: ✅ meta de reserva = **no mínimo 3 meses de custo fixo** (30/out, já no slide `p01-reserva`);
    falta a conta do custo da hora e os casos dele nos blocos; o Dr. Stanley
    revisar os blocos de Marketing e Vendas.
  - ⚠ As linhas do exercício da margem (imposto, cartão, material, repasse, tempo × hora) são proposta minha: ele confere.
  - O arquivo original da logo, pra impressão e palco.
  - Opcional: o número de WhatsApp pra versão do quiz dentro do Claude.
- ⚠ **Não chamar o Stanley de "cirurgião plástico" no material:** a falta de registro na especialidade foi um dos
  motivos do processo no CRM-AC (ver `sb/material/verificacao-stanley-bittar-2026-10-13.md`); usar "médico
  estrategista", como na marca.

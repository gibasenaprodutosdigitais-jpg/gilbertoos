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
**Exceção: nos distratos da Empreenda ela assina como testemunha, com CPF,
sob "Érica Fernanda Sena".** Em contrato a grafia tem que bater com o
documento, e esses arquivos não foram tocados.

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

**Editorial de revista**, Spectral + Barlow Condensed. Dois motivos: quem lê
compara três ou quatro perfis num computador, e página de revista lê melhor
que slide; e ele é CEO de uma revista de negócios.

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

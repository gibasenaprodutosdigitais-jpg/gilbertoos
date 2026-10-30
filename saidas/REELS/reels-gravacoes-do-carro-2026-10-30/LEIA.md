# Cortes das gravações do carro: 26 Shorts no YouTube (30/out/2026)

Vieram das 3 gravações longas no carro (`entrada-videos/longos/`: IMG_3256, IMG_3271, IMG_3304_2), triadas em 14/out
(`saidas/_CONTROLE/_triagem-gravacoes-longas-2026-10-14.md`). Ele mandou montar e agendar em 30/out.
**Só YouTube**, 5 por dia (7h, 10h, 13h, 16h, 19h), de 30/10 às 13h a 4/11 às 13h. Vídeos em `videos/`, fora do git.

## Agendados

| Quando (Brasília) | Título | Duração | ID Zernio |
|---|---|---|---|
| 30/10 13h | Os grandes não quebram. Quem quebra é o pequeno | 53 s | `6ae42850dd0dac70d033314b` |
| 30/10 16h | A pessoa que mais me alegra na academia | 55 s | `6ae42f5286bdabf1c1668deb` |
| 30/10 19h | O seu contador de estimação | 30 s | `6ae4286add0dac70d03331d4` |
| 31/10 07h | A fábrica de sapato que não fabrica sapato | 39 s | `6ae4286cdd0dac70d03331f4` |
| 31/10 10h | Você já está quebrado. Só não entendeu ainda | 35 s | `6ae4286edd0dac70d0333201` |
| 31/10 13h | O médico que me reconheceu na academia | 83 s | `6ae42872dd0dac70d0333221` |
| 31/10 16h | Eu sou da época da internet de escada | 63 s | `6ae42f5659f5e19f1c6a1c2e` |
| 31/10 19h | Pagar imposto não é ruim. É bom | 55 s | `6ae42875dd0dac70d0333243` |
| 01/11 07h | "Você está falando grego comigo" | 42 s | `6ae42f5859f5e19f1c6a1c47` |
| 01/11 10h | Estar na operação não é estar no operacional | 47 s | `6ae4287709f261790d6ccf2d` |
| 01/11 13h | A IA nunca vai substituir a empatia | 54 s | `6ae4288e4671a2279a63a076` |
| 01/11 16h | O dia em que o maior cliente parou de pagar | 46 s | `6ae428904671a2279a63a097` |
| 01/11 19h | Se o seu negócio não paga imposto, feche | 60 s | `6ae428934671a2279a63a0bb` |
| 02/11 07h | O contador não tem obrigação de fazer a sua parte | 40 s | `6ae42f5a59f5e19f1c6a1c60` |
| 02/11 10h | Eu vou te entregar a vara e o anzol | 65 s | `6ae428964671a2279a63a0d9` |
| 02/11 13h | O que é recuperação judicial de verdade | 79 s | `6ae42f5d59f5e19f1c6a1c7b` |
| 02/11 16h | O contador que cobra 300 reais | 75 s | `6ae42f5f59f5e19f1c6a1c9d` |
| 02/11 19h | Eu vivi a era Collor | 71 s | `6ae42899dd0dac70d03332c7` |
| 03/11 07h | 100 clientes, 100 segmentos diferentes | 32 s | `6ae4289bdd0dac70d03332cf` |
| 03/11 10h | O profissional que só quer o honorário | 44 s | `6ae42f6159f5e19f1c6a1cc1` |
| 03/11 13h | Network de verdade não é troca de cartão | 68 s | `6ae42f7959f5e19f1c6a1cfc` |
| 03/11 16h | Sem conhecimento você não entende Provérbios | 49 s | `6ae42f7cdf9cad670bba7ccd` |
| 03/11 19h | O medo está paralisando o empresário | 26 s | `6ae42f7edf9cad670bba7cd9` |
| 04/11 07h | Você fatura 300 mil e paga 600 reais de contador | 38 s | `6ae42f80df9cad670bba7cf9` |
| 04/11 10h | Antes de se chamar empresário, comece como afiliado | 68 s | `6ae42f82df9cad670bba7d1b` |
| 04/11 13h | A culpa não é do governo | 58 s | `6ae42f84df9cad670bba7d29` |

## Como foram feitos

- **Cor:** o iPhone grava em HDR (HLG). A primeira versão saiu opaca e ele reclamou ("as cores está muito opaco").
  O que resolveu: converter o bruto com o **`avconvert` do próprio Mac** (`-p Preset1920x1080`), que faz a passagem
  de HDR pra SDR com a cor certa, e depois um reforço leve (`eq=contrast=1.08:saturation=1.15:gamma=0.97` + nitidez).
  O som vem do bruto original. **Usar esse caminho em todo vídeo HDR do iPhone.**
- **Corte por palavra:** a transcrição palavra por palavra (`entrada-videos/longos/edit/transcripts/`) dá o começo e o
  fim exatos. A receita de cada corte está em `ferramenta/spec.json` e o motor em `ferramenta/cortes.py`.
- **Legenda queimada** em caixa alta, com dicionário de correção (Alphanilhas, Martinho da Vila, era Collor, Pronampe,
  saldar, fôlego, contábeis...). **Bip** de 1 kHz em palavrão (c12 e c20). "Porrada" não leva bip (decisão de 14/out).
- Volume em −14 LUFS. Trechos emendados levam um zoom leve pra esconder o pulo.

## O que mudou em relação à fala

- c03: saiu "todos os profissionais que eu acessar a pouco tempo", que nem o transcritor entende.
- c05: saiu "como embúster, enfim" (palavra que não se entende).
- c01: saiu "aqui de Lagoa Santa", que identificava a rede de clínicas do médico.
- c10: saiu "um projeto" depois de Pronampe (não se entende qual linha).
- c17: saiu "com rabibs e outras mais" e o "falha gestacional"; ficou "falha da gestão".
- c18: saiu "há mais de 25 anos" (o número do repositório é +15 anos).
- Legenda: "de oito" virou "de outro" (c16), "250 mil meses" virou "250 mil ao mês" (c22), "chegar de balela" virou
  "chega de balela" (c25), "sob tributação" virou "sobre tributação" (c19).

## Os 4 que ficaram de fora

- "Pergunte pro seu contador se a empresa está apta pro híbrido" (3256, 873-915): o prazo do Simples venceu em 30/10.
- "Quem paga imposto é o consumidor final" (3304_2, 194-265): número de efeito ("30% por mês") sem fonte.
- "O banco nunca toma prejuízo" (3304_2, 284-341): afirmação técnica sobre dedução de IR sem base no `conhecimento/`.
- "No Simples você está isento do split payment" (3304_2, 372-401): sem base no `conhecimento/`.

# Propostas de serviços do Grupo Sena

Pasta criada em 12/nov/2026, a pedido dele, para os modelos de proposta e contrato de serviços.

| # | Arquivo | O que é |
|---|---|---|
| 01 | `01-contrato-business-advisor-and-consultant.md` e `.docx`; **em papel timbrado:** `-TIMBRADO.docx` (editável) e `-TIMBRADO.pdf` (para enviar) | Business Advisor and Consultant: contabilidade, assessoria tributária, gestão financeira e consultoria de marketing. R$ 5.000,00 por mês, 24 meses, mais 10% sobre a economia financeira e 5% sobre o aumento de faturamento acima de 10% |
| 02 | `02-contrato-assessoria-contabil-tributaria-financeira.md` e `.docx`; **em papel timbrado do Grupo Sena:** `-TIMBRADO.docx` e `-TIMBRADO.pdf` | Assessoria Contábil, Tributária e Financeira: só valor fixo, tabela de 7 faixas (R$ 850, 1.000, 1.250, 1.850, 2.350, 3.000 e 3.500 por mês), 24 meses, mesmas contratadas do 01 |

## O que veio dele (12/nov) e o que é proposta minha

**Dele:** o nome do serviço, as quatro entregas, o valor de R$ 5.000,00 por mês, o prazo de 24 meses, os 10% sobre a economia financeira e os 5% sobre o aumento de faturamento acima de 10%.

**Minha proposta, entre colchetes no contrato, para ele confirmar:**

1. ✅ **Os 5%, confirmado por ele em 12/nov:** só sobre a parte do aumento que passar de 10%. Exemplo: base de R$ 1 milhão, faturamento de R$ 1,25 milhão, a cobrança é sobre R$ 150 mil (5% = R$ 7.500).
2. **O que conta como economia financeira:** redução de tributo contra a linha de base, crédito tributário efetivamente recuperado e redução de juros, multas e tarifas renegociados. Crédito só é cobrado quando aproveitado.
3. **Base do faturamento:** o mesmo trimestre do ano anterior, para a sazonalidade não distorcer.
4. **Apuração trimestral** da parte variável.
5. **Uma reunião mensal de 2 horas** com ele e atendimento por WhatsApp em horário comercial.
6. **Reajuste anual pelo IPCA.**
7. ✅ **Multa por saída antecipada, pedido dele em 12/nov:** correspondente às prestações de serviços e **gradativa**. Do 1º ao 12º mês, fixa em 12 mensalidades (R$ 60.000,00). A partir do 13º mês, cai uma mensalidade por mês (13º mês: 11; 14º: 10; até o 23º: 1), e no 24º mês não há multa. **O prazo de 24 meses não muda**; a redução vale só para a multa. A forma da tabela (12 mensalidades no primeiro ano, caindo uma por mês) é proposta minha a partir do que ele pediu. O aviso prévio de 60 dias continua entre colchetes.
8. **Fora do escopo:** departamento pessoal e folha, processo administrativo ou judicial, abertura e baixa de empresa, e a execução de marketing (anúncios, conteúdo, mídia).
9. **Cláusula da reforma tributária:** se a carga sobre o serviço do Grupo Sena mudar por lei a partir de 2027, o valor acompanha a diferença, para mais ou para menos. Veio do fichamento `conhecimento/elaboracao-de-contratos.md`, que recomenda essa cláusula em contrato de execução continuada.

## Antes da primeira assinatura

- **Passar pelo advogado**, como os contratos da AME.
- **Contratadas (dados dele, 12/nov):** **GS CONSULTORIA EMPRESARIAL LTDA – ME**, CNPJ 21.509.187/0001-23, e **SENA
  CONTABILIDADE**, CNPJ 25.338.012/0001-51, as duas na Av. Arthur Guimarães, 260, sala 301, Santa Cruz, BH, CEP 31.150-690,
  chamadas juntas de "GRUPO SENA". Substituíram a J&V Sena Holding, que só tem CNAE de holding. A Sena Contabilidade faz a
  contabilidade; a GS Consultoria faz tributário, financeiro, marketing e advisor, e fatura a parte variável. Cada uma
  responde pela sua frente. E-mail: financeiro@gruposena.com.br.
- ✅ **Representante das duas empresas: Gilberto Luís de Sena** (palavra dele, 12/nov). Assina pelas duas no contrato e no NDA.
- ✅ **CRC (12/nov):** **CRC-MG 110075/OI é da própria Sena Contabilidade** (organização contábil), palavra dele. Está na
  qualificação, na cláusula 1.1, no quadro das entregas e na assinatura.
- ✅ **Divisão das notas (12/nov):** 35% Sena Contabilidade (R$ 1.750,00) e 65% GS Consultoria (R$ 3.250,00), mesma proporção
  depois dos reajustes; a parte variável sai toda pela GS Consultoria.
- Prazo de 24 meses está dentro do limite de 4 anos para prestação de serviços, conforme o mesmo fichamento.

## Papel timbrado (12/nov/2026)

Pedido dele: a minuta em papel timbrado, com marca d'água, usando **a logo número 1** (aço escovado,
`../logo-3d-business-advisor-2026-11-12/opcao-1-aco-escovado-transparente.png`).

- No topo de cada página: a logo 1 pequena e um fio. No centro: o leão da logo 1 em marca d'água, bem claro.
- No rodapé: "Gilberto Sena · Business Advisor & Consultant | Grupo Sena · Belo Horizonte/MG · (31) 97353-5587 ·
  gruposena.com.br" e o número da página.
- Imagens prontas em `timbrado/` (`logo-cabecalho.png` e `marca-dagua-leao.png`).
- Para refazer depois de mudar o texto do .md:
  - Word: `node scripts/contrato-timbrado.js <md> <saida.docx> timbrado/logo-cabecalho.png timbrado/marca-dagua-leao.png "<rodapé>"`
  - PDF: `python3 scripts/contrato-timbrado-pdf.py <md> <saida.pdf> timbrado/logo-cabecalho.png timbrado/marca-dagua-leao.png "<rodapé>"`

## Sigilo e NDA (12/nov/2026)

Pedido dele: multa por quebra de sigilo, com NDA, para o caso de **outro profissional entrar no sistema para obter a
estratégia implantada pelo Grupo Sena**. Começou em R$ 250.000,00; **em 12/nov ele aprovou trocar por 24 mensalidades fixas
(R$ 120.000,00 na assinatura)**, para não passar do valor do contrato e não ser reduzida pelo juiz, mantendo a
indenização do prejuízo que passar disso. **Logo depois, ele pediu mais R$ 30.000,00: ficou 24 mensalidades + R$ 30.000,00
(R$ 150.000,00 na assinatura)**, no contrato e no Anexo II. Fica R$ 30 mil acima do valor fixo do contrato: o advogado confere.

- **Item 11 do contrato** (Sigilo e confidencialidade): define a informação confidencial (estratégia, método, diagnóstico,
  planejamento tributário, relatórios, planilhas, inclusive em sistemas, pastas, e-mails e grupos); proíbe o CLIENTE de
  deixar outro profissional acessar isso para copiar ou aplicar a estratégia; só entra quem o Grupo Sena autorizar por
  escrito e assinar o NDA; **multa de 24 mensalidades fixas + R$ 30.000,00 por infração** (R$ 150.000,00 na assinatura), mais a indenização do que passar
  disso; e a quebra é justa causa para encerrar o contrato.
- **Anexo II, Termo de Confidencialidade (NDA):** assinado pelo profissional autorizado, com o CLIENTE como responsável
  solidário. Mesma multa. Uma página, com as três assinaturas lado a lado.
- O que **não** é quebra: ordem da lei ou do juiz; informação já pública; e a entrega ao novo contador dos livros e
  arquivos contábeis do próprio CLIENTE no fim do contrato (os números são do cliente; o protegido é a estratégia).

**Decisões minhas, para ele confirmar:**

1. A multa de sigilo vale **para os dois lados** (se o Grupo Sena vazar dado do cliente, também paga). Deixa a cláusula mais
   equilibrada e mais difícil de derrubar. Se ele quiser só contra o cliente, tirar "a parte que der causa" do item 11.5.
2. Se o contrato terminar por justa causa do CLIENTE, ele paga também a multa de saída do item 10.1 (item 10.2).

**Ponto para o advogado:** conferir a redação e o valor da multa de sigilo (24 mensalidades + R$ 30.000,00) e da indenização suplementar.

## Registros profissionais no contrato (12/nov/2026)

Na qualificação do Grupo Sena e nas assinaturas: **CRA nº 06-003960/D** e **perito financeiro CONPEJ nº 01.00.3597**, os dois
passados e confirmados por ele em 12/nov (o CONPEJ foi renovado, na palavra dele).

**Atualização de 12/nov, mais tarde:** ele definiu **a logo dourada no topo** (a opção 3, medalha de cobre, que o guia da marca já
registra como a oficial do Business Advisor), arquivo `timbrado/logo-cabecalho-dourada.png`, e **manteve a marca d'água** do leão
como estava. Nos comandos acima, trocar `logo-cabecalho.png` por `logo-cabecalho-dourada.png`.

## Contrato 02: Assessoria Contábil, Tributária e Financeira (12/nov/2026)

**Dele:** o nome do serviço, só o valor fixo (sem a parte variável do 01), as mesmas contratadas e o mesmo responsável
(GS Consultoria, Sena Contabilidade CRC-MG 110075/OI, Gilberto com CRA e CONPEJ), a tabela de 7 valores e **a logo do
Grupo Sena** no papel timbrado (a assinatura horizontal, `timbrado/logo-cabecalho-grupo-sena.png`, recortada de
`identidade/Grupo Sena - Assinatura Horizontal - Preta.png`). A marca d'água do leão é a mesma do 01.

**Minha proposta, entre colchetes, para ele confirmar:**

1. **O critério das faixas:** faturamento médio mensal, de até R$ 30 mil (R$ 850) a R$ 800 mil (R$ 3.500); acima disso,
   proposta sob medida. Os cortes de cada faixa são sugestão minha.
2. **Mudança de faixa:** conferência a cada 12 meses, ou antes se a média de 3 meses mudar de faixa.
3. **A divisão das notas:** repeti os 35% / 65% do contrato 01. Pode ser que ele prefira faturar mais (ou tudo) pela Sena
   Contabilidade neste.
4. **O que ficou mais enxuto que o 01:** sem consultoria de marketing e sem advisor mensal; atendimento com 1 reunião
   trimestral. Recuperação de crédito, reorganização societária e renegociação de dívidas ficaram **fora do escopo**
   (sem a parte variável, seriam entregues de graça).
5. **Mantido do 01:** 24 meses, multa de saída gradativa (12 mensalidades até o 12º mês, caindo uma por mês) e NDA de
   24 mensalidades + R$ 30.000,00, agora contados sobre a mensalidade da faixa.

Para refazer: os mesmos comandos do 01, com `timbrado/logo-cabecalho-grupo-sena.png` no lugar da logo e o rodapé
"Grupo Sena Soluções Empresariais · Assessoria Contábil, Tributária e Financeira · Belo Horizonte/MG · (31) 97353-5587 · gruposena.com.br".

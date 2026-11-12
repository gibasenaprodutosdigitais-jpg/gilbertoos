# Propostas de serviços do Grupo Sena

Pasta criada em 12/nov/2026, a pedido dele, para os modelos de proposta e contrato de serviços.

| # | Arquivo | O que é |
|---|---|---|
| 01 | `01-contrato-business-advisor-and-consultant.md` e `.docx`; **em papel timbrado:** `-TIMBRADO.docx` (editável) e `-TIMBRADO.pdf` (para enviar) | Business Advisor and Consultant: contabilidade, assessoria tributária, gestão financeira e consultoria de marketing. R$ 5.000,00 por mês, 24 meses, mais 10% sobre a economia financeira e 5% sobre o aumento de faturamento acima de 10% |

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
- Preencher o CNPJ e o endereço do Grupo Sena e o **nome e o CRC do contador responsável técnico** (a contabilidade exige um).
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

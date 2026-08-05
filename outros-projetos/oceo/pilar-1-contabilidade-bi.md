# OCEO — Pilar 1: Contabilidade/BI (rascunho, 05/ago/2026)

> Ponto de partida pedido no briefing do CLAUDE.md desta pasta. Ainda sem
> número nem estrutura fechada — é a base pra próxima sessão dedicada.

## O modelo (evoluído com o Gilberto ao longo de 05/ago/2026)

Três camadas, na ordem em que o Gilberto foi refinando:

1. **Escritório de contabilidade interno, pra gestão.** O OCEO processa de
   verdade — folha, apuração fiscal, relatórios gerenciais — como se fosse
   o setor de contabilidade/controladoria dentro de casa. Não é só um
   painel de status: é a empresa **tendo** a própria capacidade de gestão
   contábil, sem precisar montar essa equipe internamente.
2. **O externo continua existindo, pra obrigação legal.** No Brasil,
   demonstração contábil formal exige assinatura de contador registrado no
   CRC. O escritório terceirizado do cliente **não é substituído** — ele
   segue sendo quem assina e responde legalmente. O empresário continua
   pagando ele normalmente.
3. **A informação interna vira poder de barganha com o externo.** Como o
   empresário agora tem o próprio número (gerado internamente pelo OCEO),
   ele consegue **questionar o contador externo com dado na mão** — "por
   que essa guia não foi paga", "por que a licença tá vencendo e ninguém me
   avisou". Antes disso era caixa-preta: o contador falava termo técnico, o
   empresário assinava sem entender. Agora ele chega sabendo o que
   perguntar.

Isso combina dois princípios já registrados: **"o sistema orienta, não
decide"** (o OCEO nunca decide por ele, só dá o dado pra ele decidir com
consciência) e o que motivou o comparativo CLT x sistema no business plan
geral — **substituir o custo de montar equipe interna**, aplicado aqui
especificamente ao setor contábil/fiscal/DP, não ao analista financeiro
genérico.

## 1. Comparativo de custo — o que muda

O módulo compete com o custo de **montar essa capacidade internamente**
(contratar analista de DP, analista fiscal, controller), não com o
honorário do escritório externo — esse continua sendo pago à parte, porque
resolve uma obrigação legal diferente (assinatura CRC).

### Fato citável — o que o cliente já paga ao externo (não muda com o OCEO)

| Regime tributário | Faixa de mercado (R$/mês) |
| --- | --- |
| MEI | 100 – 250 |
| ME / Simples Nacional | 250 – 800 |
| Lucro Presumido | 600 – 2.500 |
| Lucro Real | 1.500 – 10.000+ |

Fonte: tabela referencial de honorários contábeis 2026 — ASSCON (Resolução
03/2026, jan/2026) e CFC, via CIDESP e Jornal Contábil (09/jun/2026).
Facultativa, serve de baliza de mercado, não é obrigatória. Fica no
documento como contexto pro empresário entender o que já paga — não é mais
o eixo do comparativo de economia.

### Comparativo: custo de montar equipe interna x OCEO

O módulo cobre três funções que, hoje, uma empresa que quisesse internalizar
precisaria contratar separado — **Contábil** (apuração, conciliação,
custos/despesas/entradas/retiradas), **Fiscal** (impostos, guias) e **DP**
(folha, admissão/demissão):

**Analista Contábil (fato citável, fonte forte):** R$ 5.483,98/mês médio,
CAGED via salario.com.br — piso R$ 4.169,55, teto R$ 9.273,16, base 80.176
profissionais contratados/desligados no Brasil em regime CLT nos últimos 12
meses (maio/2025–abr/2026).

**Analista Fiscal (fato citável, fonte forte):** R$ 4.841,53/mês médio,
CAGED via salario.com.br — piso R$ 4.285,69, teto R$ 8.052,00, base 6.180
profissionais (mesma janela).

**Analista de DP (estimativa, fonte mais fraca):** não existe CBO exato
"Analista de Departamento Pessoal" no CAGED/salario.com.br — os CBOs
próximos são Auxiliar de Pessoal (júnior, R$ 2.291,90, CAGED) e Analista de
Recursos Humanos (generalista, R$ 4.384,21, CAGED), nenhum dos dois é o
perfil certo. Usando faixa de portais de vaga (Glassdoor/Indeed, não-CAGED):
R$ 3.000 – 3.600/mês — ponto médio R$ 3.300/mês. **Isso é estimativa, não
fato — marcar como premissa se for pro pitch.**

Aplicando o mesmo fator de encargos do business plan geral (~80%: FGTS,
INSS patronal, 13º, férias+1/3):

| Perfil | Salário base | Custo total c/ encargos |
| --- | --- | --- |
| Analista Contábil (CAGED) | R$ 5.483,98 | R$ 9.871,16 |
| Analista Fiscal (CAGED) | R$ 4.841,53 | R$ 8.714,75 |
| Analista de DP (estimativa) | R$ 3.300,00 | R$ 5.940,00 |
| **Total equipe interna** | | **R$ 24.525,91/mês** |

| | Custo mensal |
| --- | --- |
| Montar equipe interna (Contábil + Fiscal + DP) | R$ 24.525,91 |
| OCEO (mensalidade) | R$ 2.500,00 |
| **Economia mensal** | **R$ 22.025,91 (89,8%)** |
| Payback do setup (R$ 12.500) | ≈ 17 dias |

**Leitura pro pitch:** o módulo não concorre com o honorário do escritório
externo (esse continua sendo pago à parte) — concorre com a decisão de
"vou contratar gente pra cuidar disso por dentro". Duas pernas são CAGED
(fonte forte); a terceira (Analista de DP) é estimativa — se for pra pitch
de investidor de verdade, vale validar essa faixa com uma fonte melhor
antes.

## 2. Funcionalidades do módulo, por setor

Cada setor processa de verdade (gestão interna) **e** gera o painel que
municia o empresário a cobrar o escritório externo. Cada alerta vem com uma
**pergunta pronta pro contador** — não só o dado, mas a frase que o
empresário usa pra cobrar.

### Contábil — apuração e conciliação

- Lançamentos contábeis automáticos a partir da folha (DP) e da apuração
  fiscal — livro diário/razão gerado internamente
- Conciliação bancária (extrato x lançamento)
- Conciliação de contas a pagar/receber x movimentação real
- Controle de custos e despesas por centro de custo
- Controle de entradas (receita/faturamento) por categoria
- Controle de retiradas (pró-labore, distribuição de lucro) — linkado à
  separação PF x PJ já registrada em `ideias-produto.md` (item 1)
- Balancete e DRE gerencial em tempo real
- Margem de contribuição, ponto de equilíbrio, EBITDA — retoma o que já
  estava no escopo original (`ideias-produto.md`, item 4)
- Comparativo automático: o que o OCEO apurou x o que o escritório externo
  reportou — divergência vira pergunta pronta pro contador

### DP — Departamento Pessoal

- Folha de pagamento própria (proventos, descontos, INSS, IRRF, FGTS) —
  gestão interna, gerada pelo OCEO
- Cálculo de 13º, férias e rescisão
- Acompanhamento de admissão/demissão (eSocial, exames, homologação) com
  prazo e status
- Alerta de vencimento de CCT/convenção coletiva por categoria
- Comparativo automático: o que o OCEO calculou x o que o escritório
  externo reportou — divergência vira pergunta pronta pro contador

### Fiscal — linkado à RFB

- Apuração de impostos por regime (Simples / Presumido / Real), gerada
  internamente
- Painel de guias (DAS, DARF, GPS): geradas, pagas, pendentes
- Consulta direta à situação do CNPJ na Receita Federal (malha fina,
  parcelamentos, extrato DCTFWeb) — **depende de API gov.br/e-CAC, precisa
  validação técnica de viabilidade e custo com o time do OCEO**
- Apuração de créditos tributários (ex.: PIS/Cofins não-cumulativo)
- Radar da transição IBS/CBS: o que muda pro cliente e se o escritório
  externo já está adaptado
- Alerta se algo que devia estar pago/entregue não está, com prazo até a
  penalidade

### Departamento de Legalização — municipal, estadual e federal

- Abertura e registro de empresa (Junta Comercial), gerido internamente
- Alterações contratuais e societárias
- Painel de licenças (alvará, vigilância sanitária, inscrição estadual) com
  data de validade e alerta antes do vencimento
- Consulta de certidões negativas nas três esferas num só lugar
- Alerta se uma pendência federal/estadual/municipal está parada sem
  movimentação

**Mesmo ponto de atenção regulatório do módulo de investimentos** (ver
`ideias-produto.md`): integração direta com RFB/Sefaz/Junta Comercial não é
só interface — é dependência técnica real (autenticação gov.br, certificado
digital, API oficial ou scraping). E como esse módulo faz apuração/folha de
verdade internamente (não só monitora), vale confirmar com o time
técnico/jurídico se **algum desses cálculos internos também exige
responsável técnico com registro no CRC** — mesmo não sendo o documento
oficial assinado, precisa saber se há exigência regulatória pro cálculo em
si, não só pra assinatura final.

## Próximo passo

1. Validar com fonte CAGED melhor (ou dado interno do Grupo Sena) o salário
   de Analista de DP — hoje é estimativa de portal de vaga, não CAGED como
   o resto do comparativo.
2. Validar com o time técnico/jurídico se cálculo interno (folha, apuração)
   exige responsável técnico CRC, mesmo sem ser o documento assinado final.
3. Validar viabilidade/custo da integração RFB/Sefaz/Junta Comercial.
4. Com isso encaminhado, transformar em peça visual (comparativo de custo +
   mockup do painel), formato equivalente ao resto do business plan geral.

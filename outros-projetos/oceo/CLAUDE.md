# OCEO — Sistema de Gestão Empresarial (Grupo Sena)

Esta pasta é **outro projeto**, separado do GilbertoOS (a ilha de
conteúdo/posicionamento pessoal do Gilberto no Instagram — ver `CLAUDE.md`
da raiz do repo). Aqui não se fala de carrossel, reels, `/ideias` nem da
voz do Gilberto pro público. Aqui se fala do **produto OCEO**: o sistema de
gestão empresarial (ERP + BI) do Grupo Sena.

> Se você chegou aqui vindo de uma sessão do GilbertoOS: essa mistura foi
> proposital só pra montar este arquivo (05/ago/2026). Daqui pra frente,
> trabalhe o OCEO **nesta pasta**, numa sessão própria.

**Domínio:** `www.oceo.com.br` (já registrado pelo Gilberto, confirmado
06/ago/2026). O Gilberto está em **fase de registro de marca** — ver
`identidade-visual/` pra logos.

---

## O que já existe

- `business-plan-pitch-investimento.md` — resumo do business plan de 27
  páginas (PDF + HTML em `saidas/oceo-business-plan-2026-08-03/` no
  GilbertoOS, cópia também no Desktop). **O PDF de 27 páginas em si ainda
  não foi regerado** com o preço/comparativos atuais — precisa nova
  geração se for usado externamente.
- `ideias-produto.md` — backlog bruto de ideias do Gilberto, com pointer
  pra onde cada ideia foi detalhada nos 5 pilares.
- `OCEO - Business Plan e Pitch de Investimento.pdf` — documento geral,
  27 páginas (desatualizado, ver acima).
- `OCEO - Business Plan (5 Pilares).pptx` — PowerPoint nativo (16 slides,
  gráficos editáveis) com os 5 pilares, comparativo total e projeção de
  mercado, gerado 06/ago/2026 via python-pptx. **Preço em R$.**
- `OCEO - Business Plan Europa (Portugal).pptx` +
  `europa-portugal-pesquisa-salarial.md` — cópia adaptada pro mercado
  europeu (Portugal), preço em EUR, salários pesquisados em Indeed.pt/
  Jobted.pt/Talent.com Portugal, encargos calculados no modelo português
  (14 meses + TSU 23,75%, não o modelo brasileiro de ~80%). **Preço final
  em EUR decidido em 07/ago/2026: setup 2.950 € (único) + mensalidade
  850 €/mês** — acima do piso de conversão direta (594 €) e bem abaixo do
  teto de custo de equipe (19.954 €), 95,7% de economia. Gerado 06/ago/2026,
  preço atualizado 07/ago/2026.
- **Os 5 pilares, cada um com código, escopo, funcionalidades e
  comparativo de custo (CAGED onde possível):**
  - `pilar-1-contabilidade-bi.md` — **GC**, Contabilidade/BI (Contábil,
    Fiscal, DP, RH, Legalização). Complementado por
    `pilar-1-mockup-painel-bi-real.md` (05/set/2026) — 9 painéis de Power BI
    reais, já rodando pra um cliente do Grupo Sena, cobrindo a camada
    Contábil do pilar. Virou PDF de pitch em
    `pitch-bi/OCEO - Prova de Conceito BI.pdf` (05/set/2026, 12 páginas,
    gerado via Playwright com a identidade visual do OCEO) — capa,
    contexto, os 9 painéis com legenda ligando cada um à função do Pilar 1,
    e fechamento com o comparativo de custo. **Contém dado real de cliente
    (nome da rede de franquias, valores individuais de fornecedor) e está
    marcado "USO INTERNO" em toda página** — gerar versão sanitizada
    (nome/valores generalizados) antes de enviar a qualquer investidor ou
    terceiro sem NDA.
  - `pilar-2-gestao-financeira.md` — **GF**, Gestão Financeira (ERP +
    banco, DRE explicado, fundo de reserva de 3 meses de PE)
  - `pilar-3-juridico.md` — **GJ**, Jurídico (advogado consultivo interno)
  - `pilar-4-marketing-vendas.md` — **GM**, Marketing e Vendas (agência +
    comercial interno)
  - `pilar-5-educacao-pre-investimento.md` — **GI**, Educação
    Pré-Investimento (ex-"Criação de Renda Passiva", rota educacional)
- `oceo-cinco-pilares-2026-08-05.html` / `OCEO - Os 5 Pilares.pdf` —
  material consolidado dos 5 pilares (8 páginas, gráfico por pilar + soma
  total na última página), gerado 05/ago/2026 via Playwright (mesmo
  utilitário do carrossel, em `scripts/`).

## Preço do OCEO

Setup R$ 12.500 (único) + **mensalidade R$ 3.500/mês, simples, mas
completo** — mensalidade fixa + repasse de custo variável já identificado
(WhatsApp Business API acima da franquia grátis, Pilar GM).

## Regra-mãe herdada do GilbertoOS (vale aqui também)

**Separar fato de premissa, sempre.** O business plan já existente marca
isso explicitamente (badge "Premissa do modelo"): CAC, churn, custo fixo
operacional e cenários de cliente são **chutes de ordem de grandeza**, não
dado real — precisam validação antes de ir pra investidor de verdade. Preço
do produto (setup R$12.500 + R$3.500/mês) e os dados de mercado
(SEBRAE/TAM, preço de concorrente, salários CAGED) **são** fato citável.
Manter essa disciplina em tudo que for produzido aqui — nunca apresentar
estimativa como se fosse número fechado.

## Estado atual — 05/ago/2026

**Os 5 pilares estão registrados e detalhados** (ver "O que já existe"),
cada um com escopo, ponto de atenção regulatório quando existe, e
comparativo de custo. Pendências reais que sobraram, por pilar:

- **GC (Pilar 1):** validar salário de Analista de DP com fonte melhor
  (hoje é estimativa de portal, não CAGED).
- **GF (Pilar 2):** validar viabilidade/custo da integração Open Finance.
- **GJ (Pilar 3):** definir se há advogado parceiro fixo do OCEO pra
  personalização/execução, ou se fica sempre com o advogado do cliente.
- **GM (Pilar 4):** modelar o custo variável do WhatsApp Business API
  (conversa) na margem do OCEO.
- **GI (Pilar 5):** redigir e validar com jurídico o texto padrão de
  disclaimer (conteúdo educacional, não recomendação individualizada).
- **Geral:** regerar o PDF de 27 páginas do business plan geral com o
  preço/comparativos atualizados (R$ 3.500, simples mas completo), quando
  fizer sentido.

Próxima frente ainda não definida — em aberto pro Gilberto trazer o
Pilar 6 (se houver) ou aprofundar pendências acima.

## Como trabalhar aqui

- Antes de qualquer dado de honorário/mercado: buscar fonte real (sindicato
  contábil, CRC, pesquisa de mercado) — não estimar sem avisar que é
  estimativa, mesma disciplina do resto do documento.
- Ao gerar qualquer material novo (estrutura visual, comparativo, proposta
  de módulo), salvar nesta pasta (`outros-projetos/oceo/`) ou em subpasta
  dela — não em `saidas/` do GilbertoOS, que é reservado pra conteúdo do
  Instagram do Gilberto.
- Se a sessão precisar de contexto pessoal do Gilberto (ex.: habilitação
  AAI/ANCORD que dá lastro ao módulo de investimentos), pode consultar
  `_memoria/quem-e-gilberto.md` na raiz do GilbertoOS — mas só leitura, não
  escrever conteúdo do OCEO lá dentro.

# Os 42 carrosséis na fila

Dois por dia no Instagram, **15h e 20h** (Brasília). De 16/10 a 05/11.
Completa o dia de seis: 5h Provérbios, 9h frase, 12h reels, 15h carrossel,
18h reels, 20h carrossel.

| Dia | 15h | 20h |
|---|---|---|
| 16/10 | 7-mudancas-2027-2026-08-31 | quem-e-gilberto-2026-10-06 |
| 17/10 | simples-nacional-prazo-2026-09-22 | dre-7-passos-2026-09-29 |
| 18/10 | revenda-carros-stj-2026-08-27 | ponto-de-equilibrio-2026-08-02 |
| 19/10 | ipi-imposto-seletivo-2026-08-27 | 12-pilares-business-plan-2026-08-03 |
| 20/10 | pf-autonomo-cbs-2026-08-27 | 5gs-gestao-financeira-2026-07-17 |
| 21/10 | imobiliario-aluguel-2026-08-30 | 5gs-gestao-tributaria-2026-07-17 |
| 22/10 | redutor-ajuste-construcao-2026-08-30 | 5gs-gestao-de-si-2026-07-17 extraido |
| 23/10 | simples-hibrido-2026-08-27 | 5gs-fornecedores-clientes-2026-10-06 |
| 24/10 | reforma-ebooks-2026-09-13 | 10-pergaminhos-maior-vendedor-2026-08-03 |
| 25/10 | reforma-infoprodutores-2026-09-13 | rede-de-mastermind-2026-08-09 |
| 26/10 | reforma-ecommerce-2026-09-13 | forjado-imersao-2026-08-07 |
| 27/10 | reforma-representante-comercial-2026-09-13 | dissolucao-sociedade-2026-08-10 |
| 28/10 | reforma-medicos-2026-09-13 | agronegocio-reforma-2026-08-30 |
| 29/10 | medicos-reforma-2026-08-27 | educacao-reforma-2026-08-30 |
| 30/10 | transportadoras-reforma-2026-08-27 | textil-alerta-2026-08-27 |
| 31/10 | comercio-reforma-2026-08-27 | biomedicina-reforma-2026-08-27 |
| 01/11 | servicos-alerta-2026-08-27 | entregadores-app-reforma-2026-08-27 |
| 02/11 | odontologia-reforma-2026-08-27 | tecnologia-saas-reforma-2026-08-30 |
| 03/11 | ecommerce-alerta-2026-08-27 | saude-geral-reforma-2026-08-27 |
| 04/11 | clinicas-esteticas-reforma-2026-08-27 | transportes-reforma-2026-08-27 |
| 05/11 | industria-reforma-2026-08-30 | 10-ebooks-leitura-2026-09-06 |

⚠ `10-ebooks-leitura` tem **12 lâminas** e o Instagram aceita 10. Está em
último de propósito, esperando ele decidir se corta duas ou vira dois posts.


---

## Onde eu parei

| Dia | 15h | 20h |
|---|---|---|
| 16/10 | ✅ 7-mudancas-2027 | ✅ quem-e-gilberto |
| 17/10 | ✅ simples-nacional-prazo | ✅ dre-7-passos |
| 18/10 | ✅ revenda-carros-stj | ✅ ponto-de-equilibrio |
| 19/10 | ✅ ipi-imposto-seletivo | ✅ 12-pilares-business-plan |
| 20/10 | ✅ pf-autonomo-cbs | ✅ 5gs-gestao-financeira |
| 21/10 em diante | ⏳ | ⏳ |

**Próximo:** 21/10 às 15h, `carrossel-imobiliario-aluguel-2026-08-30`.

⚠ **Troquei o Simples Híbrido do dia 18 com o Revenda de Carros do dia 23.**
O Híbrido caía no dia seguinte ao Simples Nacional do dia 17, e os dois
contam a mesma história (janela de setembro, 30 de novembro, março de 2027,
fim do crédito presumido de 9,25%). Dois dias seguidos repetindo isso
queima o assunto.

🔴 **O limiar de R$40.500 do nanoempreendedor.** O carrossel do autônomo dizia
que "praticamente todo autônomo" vira contribuinte de CBS, e dava **diarista**
como exemplo. Errado, e contradizia o próprio carrossel das 7 mudanças, que
sai quatro dias antes dizendo o número certo. Pela LC 214/2025, quem fatura
até **R$40.500/ano** não é contribuinte de IBS nem CBS. Fichamento em
`conhecimento/reforma-tributaria-nanoempreendedor.md`. **É o terceiro
carrossel/reels em que esse mesmo erro aparece — conferir sempre que a peça
falar de autônomo, PF ou profissional liberal.**

⚠ **Envio de lâmina falha em silêncio.** O `slide-01` do 5Gs voltou `000` no
curl, que é conexão caída, não erro HTTP. **Conferir o código de cada lâmina**
e refazer a que não voltar 200, senão o post vai ao ar com imagem faltando.

⚠ **Peça de agosto pode ter data relativa.** O do IPI dizia "essa semana" e
"semana que vem" em dois cards e na legenda. Em outubro isso vira informação
errada. Troquei por "o que já foi editado", "a primeira" e "a segunda", e
re-renderizei. **Rodar antes de cada peça:**
`grep -niE "essa semana|semana que vem|hoje o governo" carrossel.html legenda.md`

⚠ **O nome dos arquivos muda de pasta pra pasta.** Uns usam
`instagram/slide-01.png`, outros `instagram/card-01.png`. **Listar a pasta
antes de montar o curl**, senão o upload falha com
*"error encountered when reading a file"*.

⚠ **Conferir antes de agendar**, que já peguei dois:
- `7-mudancas-2027` dizia **"tua empresa"** na capa e na legenda. A regra
  dele é **você**, nunca tu. Corrigi e re-renderizei.
- ✅ **O negrito markdown saiu das 11 legendas que tinham.** O Instagram não
  lê `**texto**`, mostra o asterisco na tela.
- `quem-e-gilberto` dizia **"720 horas"** na pós-graduação. Ele mandou tirar
  a carga horária em 15/out. Corrigi na legenda (nos cards já estava certo).

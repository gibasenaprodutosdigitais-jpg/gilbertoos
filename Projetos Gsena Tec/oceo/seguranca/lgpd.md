# O OCEO e a LGPD

> **Leia isto antes de usar o documento.**
> Os artigos citados abaixo estão indicados pela memória de quem escreveu e
> **precisam de conferência do advogado antes de virar material pra cliente,
> contrato ou pitch.** Enquanto isso não for feito, use este arquivo como
> mapa interno de trabalho — não como parecer jurídico.
> Esta é a mesma disciplina do resto do OCEO: **separar fato de premissa,
> sempre.** Pendência do Pilar 3 (GJ).

**Lei 13.709/2018 (LGPD).**

O OCEO trata dado pessoal em volume e em profundidade: folha de pagamento,
dado de funcionário do cliente, movimentação financeira, apuração fiscal.
Não é sistema acessório — é sistema de tratamento pesado.

---

## Onde o OCEO já está de pé

| O que a lei pede (a conferir) | Onde o OCEO cumpre |
|---|---|
| Medidas técnicas de segurança (art. 46) | Senha irreversível, sessão que expira, isolamento entre clientes. Ver `como-o-oceo-protege-os-dados.md` |
| Registro das operações de tratamento (art. 37) | A trilha auditável grava todo fato trocado entre pilares, com data e origem |
| Correção de dado incorreto (art. 18, III) | O dado continua alterável — e a alteração fica registrada |
| Eliminação quando exigida (art. 18, VI) | O dado pode ser apagado. **É exatamente isto que a blockchain impediria** — ver `decisao-blockchain.md` |
| Prevenção e responsabilização (art. 6º) | A trilha prova o que aconteceu e quando, inclusive contra o próprio operador |

## Onde ainda falta

| O que a lei pede (a conferir) | Situação |
|---|---|
| Encarregado / DPO (art. 41) | **Não definido.** Precisa de nome e canal de contato publicado |
| Comunicação de incidente (art. 48) | **Sem plano.** A ANPD fixou prazo curto por resolução própria — o número exato precisa ser confirmado antes de entrar em contrato |
| Política de privacidade e termo de uso | **Não existem.** Obrigatórios antes do primeiro cliente |
| Contrato de operador com o cliente | **Não existe.** O Grupo Sena opera dado de terceiro — o papel de cada parte precisa estar escrito |
| Prazo de guarda e descarte | **Não definido.** Ver a ressalva abaixo, que é onde mora a armadilha |
| Criptografia do banco em repouso | **Não implementada** |

---

## A ressalva que só um contador enxerga

O direito de eliminação **não é absoluto**. A própria lei preserva o dado
quando há obrigação legal de guarda (art. 16) — e é o caso de quase tudo que
o OCEO trata: documento fiscal, folha, livro contábil têm prazo de guarda
próprio na legislação tributária e trabalhista.

Ou seja: cliente pedir "apaga tudo" **não** significa apagar tudo. Significa
apagar o que não está sob guarda obrigatória, e manter o resto pelo prazo
legal.

**Isso precisa estar escrito no contrato** — senão vira discussão no pior
momento possível.

### E isso não salva a blockchain

Poderia parecer que, se o dado tem que ser guardado por anos mesmo, a
imutabilidade deixa de ser problema. Não deixa, por dois motivos:

1. **O prazo de guarda termina.** Passado ele, o dado tem que poder sumir.
   Imutável não some.
2. **Correção é obrigatória o tempo todo.** Dado errado tem que poder ser
   corrigido — e corrigir é escrever por cima, coisa que uma blockchain, por
   definição, não faz.

O que o OCEO faz é o meio-termo correto: o dado é **alterável** (a lei
exige), mas **toda alteração deixa rastro** (a auditoria exige).

---

## O argumento comercial que sai daqui

A maioria dos sistemas contábeis não consegue provar quem alterou o quê. O
OCEO consegue — e consegue inclusive contra o próprio Grupo Sena.

Numa fiscalização ou numa discussão societária, isso deixa de ser recurso
técnico e vira **prova**.

---

## Próximo passo

Levar este arquivo ao advogado do Pilar 3 pra:

1. confirmar ou corrigir cada artigo citado
2. redigir política de privacidade, termo de uso e contrato de operador
3. definir o encarregado e o canal
4. fechar a tabela de prazo de guarda por tipo de documento
5. confirmar o prazo de comunicação de incidente à ANPD

*Escrito em 27/set/2026.*

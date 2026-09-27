# Decisão: blockchain no OCEO

**Data:** 27/set/2026
**Pergunta que originou:** *"Sobre a segurança de dados dos clientes, pode
gerar uma com base em blockchain?"*
**Decisão:** **Não** para guardar o dado do cliente. **Sim** para provar que
o dado não foi adulterado — e essa parte já está construída.

Este documento existe pra não reabrir a discussão daqui a seis meses, e pra
ter resposta pronta quando um cliente ou investidor perguntar "por que vocês
não usam blockchain?".

---

## Por que não guardar o dado numa blockchain

### 1. Blockchain não esconde nada

Ela garante que o registro **não mudou**. Não garante que ele seja
**secreto**. São coisas diferentes, e é a confusão mais comum do mercado.

Numa rede pública, todo mundo vê tudo. Numa rede privada, todos os
participantes veem tudo. O sigilo continua vindo de criptografia e controle
de acesso — que é onde o esforço de engenharia precisa estar.

**Quem vende "blockchain = segurança de dados" está vendendo a palavra, não
a tecnologia.**

### 2. Espalhar o dado é o contrário de protegê-lo

Uma blockchain funciona replicando cada registro em vários computadores —
é disso que vem a resistência dela. Ótimo para dinheiro público. Péssimo
para folha de pagamento, faturamento e apuração de imposto de cliente.

Hoje o dado do cliente está em um lugar, com uma porta. Numa rede, estaria
em vários lugares, com várias portas. Isso é **mais** superfície de ataque,
não menos.

### 3. Imutabilidade briga com a LGPD

A Lei 13.709/2018 dá ao titular o direito de pedir a **eliminação** dos
dados. Se o dado é imutável por construção, não existe como cumprir.

Não é detalhe técnico, é **risco jurídico**: seria adotar uma tecnologia que
impede o cumprimento de uma obrigação legal. O contrário de diferencial.

> Ponto de atenção pro Pilar 3 (GJ): a redação exata e o enquadramento
> precisam de conferência do advogado antes de virar material pra cliente.
> Ver `lgpd.md`.

### 4. Custo e complexidade sem retorno

Rede blockchain exige nós, manutenção, taxa de transação (em rede pública)
e gente que saiba operar. Tudo isso pra entregar uma garantia que a corrente
de hashes já entrega com 100 linhas de código e zero custo de operação.

---

## O que foi feito no lugar

**A parte boa da blockchain, sem as partes que atrapalham:** o encadeamento
de hashes.

Cada registro guarda o resumo criptográfico do anterior. Alterar, apagar ou
inserir registro quebra a corrente, e a conferência aponta o ponto exato.

O que se ganha, igual à blockchain:
- prova de que o histórico não foi adulterado
- detecção que aponta o registro exato
- vale inclusive contra quem administra o sistema

O que se evita:
- replicar dado de cliente em vários computadores
- impedir a correção e a eliminação exigidas por lei
- custo de operar uma rede

Detalhe técnico e provas em `como-o-oceo-protege-os-dados.md`.

---

## Quando blockchain entra de verdade

Existe **um** uso legítimo, e ele fica guardado como opção:

A conferência gera o **resumo do período** — um número de 64 caracteres que
resume todos os registros **sem revelar nenhum deles**.

Publicar esse número numa blockchain pública prova, depois, que aqueles
registros já existiam naquela data. Nenhum dado de cliente sai do OCEO —
vai só o número.

**Função: carimbo de data confiável. Não armazenamento.**

Mesmo isso não é urgente: e-mail datado ao cliente ou registro em cartório
resolvem o mesmo problema hoje, sem custo nenhum. A porta fica aberta pro
dia em que um cliente ou um regulador exigir a prova pública.

---

## Resumo em uma frase, pra usar em reunião

> "A gente usa a criptografia que está por trás da blockchain — o
> encadeamento que prova que nada foi adulterado. O que a gente não faz é
> espalhar o dado do seu cliente por uma rede, porque isso não protegeria
> nada e ainda impediria a gente de apagar o dado quando você exigir, como
> manda a LGPD."

# Quiz da Imersão AME no Google Sheets

Cada resposta do quiz cai numa de duas planilhas no Google Drive do Gilberto:

| Planilha | Quem cai nela |
|---|---|
| **Imersão AME · Acima de R$ 70 mil** | faixas C (de R$ 70 a 120 mil) e D (acima de R$ 120 mil) |
| **Imersão AME · Até R$ 70 mil** | faixas A (até R$ 30 mil) e B (de R$ 30 a 70 mil) |

Colunas: data e hora, nome, WhatsApp, Instagram, nicho, faturamento, maior
dificuldade, o texto com as palavras dele e a origem.

O caminho é: quiz → Google Apps Script (`Codigo.gs`) → planilha certa. A cópia
no computador (`../respostas.csv`) continua valendo quando o quiz roda pelo
servidor local.

## Ativar (uma vez só, uns 10 minutos)

1. Entrar em **script.google.com** com a conta Google onde as planilhas devem ficar.
2. **Novo projeto.** Dar o nome "Imersão AME · Quiz".
3. Apagar o que vier escrito e **colar todo o conteúdo de `Codigo.gs`**. Salvar.
4. No menu de funções, lá em cima, escolher **configurar** e clicar em **Executar**.
   O Google pede permissão: escolher a conta, "Avançado", "Acessar Imersão AME · Quiz"
   e **Permitir**. (O aviso de "app não verificado" é normal: o app é seu.)
5. Embaixo, no **Registro de execução**, aparecem os links das duas planilhas.
   Elas já estão no seu Drive, com o cabeçalho pronto.
6. **Implantar → Nova implantação.** Na engrenagem, escolher **App da Web**.
   - Executar como: **Eu**
   - Quem pode acessar: **Qualquer pessoa**
   Clicar em **Implantar** e **copiar o link do App da Web** (termina em `/exec`).
7. Mandar esse link aqui. Ele entra no quiz em `PLANILHA_URL`, no `site/index.html`.

## Conferir

- Abrir o link do App da Web no navegador: deve aparecer `{"ok":true,"app":"Imersão AME · quiz"}`.
- Responder o quiz uma vez e ver a linha cair na planilha certa.

## Se mudar alguma coisa

- **Mudou a faixa de faturamento no quiz:** mudar também `FAIXAS_ACIMA_70` e
  `FAIXAS_ATE_70` no `Codigo.gs`, colar de novo no Apps Script e fazer
  **Implantar → Gerenciar implantações → editar → Nova versão**. O link continua o mesmo.
  Faixa que o script não conhece é recusada e não cai em nenhuma planilha.
- **Rodar `configurar()` de novo** não cria planilha repetida: ele só mostra os links.

## Cuidados

- As planilhas têm nome e WhatsApp de outras pessoas. Compartilhar só com quem
  vai atender esses contatos.
- Célula que começaria com `=`, `+`, `-` ou `@` entra como texto, pra ninguém
  conseguir colocar fórmula na planilha pelo formulário.

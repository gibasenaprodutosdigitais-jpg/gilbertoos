# Segurança do OCEO

Tudo que diz respeito a **proteger o dado do cliente** dentro do OCEO mora
aqui: as decisões tomadas, o motivo de cada uma, o que já está construído e
o que ainda falta.

> Por que uma pasta só pra isso: segurança é o primeiro assunto que um
> cliente grande levanta e o último que alguém documenta. Quando a pergunta
> vier numa reunião, a resposta tem que estar pronta e escrita — não ser
> improvisada na hora.

---

## Os documentos

| Arquivo | Pra que serve |
|---|---|
| `como-o-oceo-protege-os-dados.md` | A postura técnica completa: senha, sessão, isolamento entre clientes e trilha auditável. É o documento de referência. |
| `decisao-blockchain.md` | A decisão sobre blockchain, registrada com os motivos. Pra não reabrir a discussão daqui a seis meses. |
| `lgpd.md` | Onde o OCEO encosta na Lei 13.709/2018 e o que ainda precisa de validação do jurídico. |
| `resposta-ao-cliente.md` | Como responder "meus dados estão seguros?" numa reunião comercial, sem jargão. |
| `prova-adulteracao-detectada.png` | A tela do portal acusando uma adulteração feita de propósito no banco. É a prova visual. |
| **`OCEO - Seguranca de Dados (guia de reuniao).pdf`** | **Uma página, pra levar impressa.** É o `resposta-ao-cliente` com a identidade do OCEO. Gerado por `guia-reuniao.html` + `render.js` — pra atualizar, edite o HTML e rode `node render.js`. |

O código que implementa tudo isso está em `../oceo-core/`, com os testes que
provam cada afirmação feita aqui.

---

## O resumo em uma página

O OCEO protege o dado do cliente em **quatro camadas**, e cada uma responde
a uma pergunta diferente:

1. **Quem é você?** — senha guardada de forma irreversível (PBKDF2, 600 mil
   iterações, sal próprio por conta) e sessão que expira.
2. **Você pode ver esta empresa?** — cada cliente só enxerga o que é dele.
   Tentar abrir a empresa de outro devolve "não encontrado" — o sistema não
   confirma nem que ela existe.
3. **Alguém mexeu no histórico?** — cada registro guarda o resumo
   criptográfico do anterior. Mexer em um quebra a corrente e a conferência
   aponta o registro exato. **Vale inclusive contra o próprio Grupo Sena.**
4. **A lei está sendo cumprida?** — o dado continua podendo ser corrigido e
   eliminado quando o titular exigir, como manda a LGPD. Ver `lgpd.md`.

---

## O que ainda falta (em ordem de urgência)

Nada disto impede demonstrar o sistema hoje. Tudo isto é obrigatório
**antes do primeiro cliente real com dado de verdade dentro.**

1. **Ligar o envio de e-mail.** A recuperação de senha está construída e
   testada, mas o e-mail hoje é gravado em arquivo em vez de enviado —
   falta contratar e configurar o serviço de envio. É o item mais curto da
   lista e o único que separa a recuperação de estar completa.
2. **Segundo fator para o papel `dono`.** Quem pode tudo precisa de mais
   que uma senha.
3. **Criptografia do banco em repouso.** Se o servidor for levado, o arquivo
   do banco não pode ser legível.
4. **Rotina de backup testada.** Backup que nunca foi restaurado não é
   backup. Precisa de um teste de restauração com data marcada.
5. **Plano de resposta a incidente.** A LGPD dá prazo pra comunicar. Ver
   `lgpd.md`.
6. **Postgres no lugar do SQLite**, quando houver mais de um servidor.

### Já resolvido

- ~~Limite de tentativas de login~~ — **feito em 27/set/2026.** Cinco senhas
  erradas travam a conta por 15 minutos; vinte contas diferentes travam a
  origem. Seis testes provam.
- ~~Recuperação de senha~~ — **o mecanismo está pronto e testado** em
  27/set/2026: link que vence em 30 minutos, vale uma vez só, fica guardado
  resumido no banco e derruba todas as sessões abertas ao ser usado. Falta
  só o envio de e-mail de verdade (item 1 acima).

---

*Registrado em 27/set/2026. Atualizado em 27/set/2026 com a trava de
login e a recuperação de senha. Atualizar sempre que um documento novo
entrar na pasta.*

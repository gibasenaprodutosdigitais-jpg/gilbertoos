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

1. **Limite de tentativas de login.** Hoje dá pra tentar senha infinitas
   vezes. É a falha mais fácil de explorar e a mais fácil de corrigir.
2. **Recuperação de senha por e-mail.** Sem isso, cliente que esquece a
   senha depende de alguém do Grupo Sena mexer no banco — e isso é
   exatamente o que a trilha existe pra flagrar.
3. **Segundo fator para o papel `dono`.** Quem pode tudo precisa de mais que
   uma senha.
4. **Criptografia do banco em repouso.** Se o servidor for levado, o arquivo
   do banco não pode ser legível.
5. **Rotina de backup testada.** Backup que nunca foi restaurado não é
   backup. Precisa de um teste de restauração com data marcada.
6. **Plano de resposta a incidente.** A LGPD dá prazo pra comunicar. Ver
   `lgpd.md`.
7. **Postgres no lugar do SQLite**, quando houver mais de um servidor.

---

*Registrado em 27/set/2026. Atualizar este índice sempre que um documento
novo entrar na pasta.*

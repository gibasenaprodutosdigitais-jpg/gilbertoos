# Capas de Reels

## `capa-preta.jpg`

Preto puro, 1080 × 1920, que é a medida da capa de Reels. O Instagram corta
o centro para o quadradinho do feed, então preto funciona nos dois
enquadramentos.

**Criada em 10/out/2026**, a pedido dele, para os Reels de música clássica
irem ao ar com o feed uniforme em vez de cada um mostrar um frame diferente
do vídeo. **Aplicada em 11 dos 12 publicados naquela noite** — o primeiro, o
do Bach, saiu antes, com o frame do próprio vídeo.

### Como aplicar num post pela Zernio

A capa entra como `instagramThumbnail` dentro do item de mídia, e **não** no
campo `media_urls` da ferramenta simples. Isso quer dizer que o
`posts_create` básico do MCP não dá conta: é preciso usar
`posts_create_post` ou `posts_update_post` via `call_tool`, assim:

```
media_items: [{
  "type": "video",
  "url": "<url do video>",
  "instagramThumbnail": "<url da capa>"
}]
platforms: [{"platform": "instagram", "accountId": "<id>"}]
```

Dá para aplicar depois de agendado: `posts_update_post` aceita post com
status `scheduled` e não perde a hora nem a legenda.

### ⚠ Isso vai mudar

**Ele avisou em 10/out/2026 que a capa vai mudar num próximo momento.** Então
**não tratar preto como padrão**: em publicação nova, perguntar ou esperar ele
dizer qual capa usar.

O que pesa na decisão: capa preta deixa o grid uniforme e esconde do que o
vídeo trata. Num perfil em que a imagem é o atrativo, como orquestra e
pianista, isso custa clique. Vale quando a intenção é justamente o grid.

Uma terceira via, se ele quiser os dois: capa preta **com o nome da obra em
branco**. Mantém a uniformidade e ainda diz o que é.

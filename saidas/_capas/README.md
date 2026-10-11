# Capas de Reels

## `capa-preta.jpg`

Preto puro, 1080 × 1920, que é a medida da capa de Reels. O Instagram corta
o centro para o quadradinho do feed, então preto funciona nos dois
enquadramentos.

**Criada em 10/out/2026**, a pedido dele, para os 11 Reels de música clássica
irem ao ar com o feed uniforme em vez de cada um mostrar um frame diferente
do vídeo.

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

### O que considerar antes de usar de novo

Capa preta deixa o grid uniforme e esconde do que o vídeo trata. Num perfil
em que a imagem é o atrativo, isso custa clique. Vale quando a intenção é
justamente o grid, ou quando o conteúdo se vende pela legenda.

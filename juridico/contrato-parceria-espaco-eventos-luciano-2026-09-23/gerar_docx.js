/*
 * Gera a versao EDITAVEL (.docx) do resumo de uma pagina.
 *
 *   node gerar_docx.js
 *
 * Por que existe: o Gilberto edita no Word e devolve. Entregar PDF obriga ele
 * a converter, e a conversao embaralha as tabelas — foi o que aconteceu em
 * 28/09. Este arquivo sai ja editavel.
 *
 * O conteudo espelha o resumo.html. Mudou um, mude o outro.
 */
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, VerticalAlign,
  convertMillimetersToTwip,
} = require('/Users/gilbertosena/Desktop/GilbertoOS/scripts/node_modules/docx');
const fs = require('fs');

// ------------------------------------------------------------------ paleta
const TINTA = '16161A', ACENTO = 'D6412B', FRACO = '6E6A63', LINHA = 'C9C5BC';
const PAPEL = 'F2F0EB', CAIXA = 'FBFAF8';

// A4 com margem de 12mm: sobra 186mm de largura util
const LARGURA = convertMillimetersToTwip(186);
const MEIO = Math.floor(LARGURA / 2) - 40;

const semTabela = {
  top:    { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  bottom: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  left:   { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  right:  { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  insideHorizontal: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  insideVertical:   { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
};
const semBorda = {
  top:    { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  bottom: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  left:   { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  right:  { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
};
const linhaBaixo = {
  ...semBorda,
  bottom: { style: BorderStyle.SINGLE, size: 2, color: LINHA },
};

/** Texto com trechos em negrito: t('normal', ['negrito', 1], ' resto') */
function runs(...partes) {
  return partes.map((p) => {
    if (Array.isArray(p)) {
      const [texto, , cor] = p;
      return new TextRun({ text: texto, bold: true, size: 16, color: cor || TINTA });
    }
    return new TextRun({ text: p, size: 16, color: TINTA });
  });
}

const p = (children, extra = {}) =>
  new Paragraph({ children, spacing: { before: 0, after: 20, line: 200 }, ...extra });

const texto = (...partes) => p(runs(...partes));

/** Cabecalho de secao: caixa alta, fina, com regua embaixo */
const secao = (t) => new Paragraph({
  children: [new TextRun({
    text: t.toUpperCase(), bold: true, size: 13, color: TINTA,
    characterSpacing: 30,
  })],
  spacing: { before: 130, after: 50 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: TINTA, space: 1 } },
});

/** Celula generica */
const celula = (filhos, largura, opts = {}) => new TableCell({
  children: filhos,
  width: { size: largura, type: WidthType.DXA },
  borders: opts.borders || semBorda,
  shading: opts.fundo
    ? { type: ShadingType.CLEAR, color: 'auto', fill: opts.fundo }
    : undefined,
  margins: { top: 60, bottom: 60, left: 90, right: 90 },
  verticalAlign: VerticalAlign.TOP,
});

/** Tabela de duas colunas: rotulo estreito + valor */
function tabelaRotulos(linhas, larguraRotulo = 2100) {
  const larguraValor = LARGURA - larguraRotulo;
  return new Table({
    columnWidths: [larguraRotulo, larguraValor],
    width: { size: LARGURA, type: WidthType.DXA },
    borders: semTabela,
    rows: linhas.map(([rot, ...conteudo]) => new TableRow({
      children: [
        celula([p([new TextRun({ text: rot, bold: true, size: 16, color: TINTA })])],
               larguraRotulo, { borders: linhaBaixo }),
        celula([p(runs(...conteudo))], larguraValor, { borders: linhaBaixo }),
      ],
    })),
  });
}

/** Duas colunas lado a lado */
const parLadoALado = (esq, dir) => new Table({
  columnWidths: [MEIO, MEIO],
  width: { size: LARGURA, type: WidthType.DXA },
  borders: semTabela,
  rows: [new TableRow({ children: [celula(esq, MEIO), celula(dir, MEIO)] })],
});

const bolinha = (t) => p([
  new TextRun({ text: '◆  ', size: 13, color: ACENTO }),
  ...runs(t),
]);

// --------------------------------------------------------------- conteudo
const caixaParte = (quem, oque, itens, paga) => [
  p([new TextRun({ text: quem.toUpperCase(), bold: true, size: 13, color: ACENTO,
                   characterSpacing: 24 })], { spacing: { after: 30 } }),
  p([new TextRun({ text: oque, bold: true, size: 20, color: TINTA })],
    { spacing: { after: 60 } }),
  ...itens.map(bolinha),
  p([new TextRun({ text: paga, size: 14, color: FRACO })],
    { spacing: { before: 60 },
      border: { top: { style: BorderStyle.SINGLE, size: 2, color: LINHA, space: 3 } } }),
];

const caixaDestaque = (numero, corpo) => [
  new Table({
    // a coluna do numero precisa caber "50/50" sem quebrar linha
    columnWidths: [1450, MEIO - 1650],
    width: { size: MEIO - 200, type: WidthType.DXA },
    borders: semTabela,
    rows: [new TableRow({ children: [
      celula([p([new TextRun({ text: numero, bold: true, size: 28, color: ACENTO,
                               font: 'Courier New' })])], 1450),
      celula(corpo.map((c) => p(runs(...c))), MEIO - 1650),
    ] })],
  }),
];

const doc = new Document({
  styles: { default: { document: { run: { font: 'Arial', size: 16, color: TINTA } } } },
  sections: [{
    properties: {
      page: {
        size: { width: convertMillimetersToTwip(210), height: convertMillimetersToTwip(297) },
        margin: {
          top: convertMillimetersToTwip(11), bottom: convertMillimetersToTwip(10),
          left: convertMillimetersToTwip(12), right: convertMillimetersToTwip(12),
        },
      },
    },
    children: [
      // ----------------------------------------------------------- topo
      p([new TextRun({ text: 'VERSÃO DE TRABALHO · POSTERIOR À ASSINATURA DE 28/09/2026',
                       bold: true, size: 13, color: ACENTO, characterSpacing: 26 })],
        { spacing: { after: 40 } }),
      p([new TextRun({ text: 'Centro de Eventos "Kairós"', bold: true, size: 32, color: TINTA })],
        { spacing: { after: 50 } }),
      p([
        new TextRun({ text: 'Atenção: este não é o documento assinado em 28/09/2026. ',
                      bold: true, size: 15, color: TINTA }),
        new TextRun({ text: 'Aquele está guardado à parte e não deve ser alterado. Este '
                          + 'acompanha o contrato definitivo, que é o documento que vale. '
                          + 'Inventário dos equipamentos em anexo separado.',
                      size: 14, color: FRACO }),
      ], { spacing: { after: 40 },
           border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: TINTA, space: 4 } } }),

      // --------------------------------------------------------- partes
      secao('As partes'),
      parLadoALado(
        caixaParte('Motor em Ação aporta', 'O espaço físico',
          ['Imóvel com auditório e dependências, pronto para uso',
           'Instalações prediais, energia, climatização e acessos',
           'Disponibilidade garantida durante toda a parceria'],
          'Continua pagando por fora: IPTU, aluguel, obras, manutenção predial, '
          + 'manutenção dos equipamentos, energia, água, internet, portaria, ECAD, '
          + 'alvará, AVCB e o seguro de responsabilidade civil. Davi Leonardo de Paula '
          + 'Arraz assina pela empresa; Luciano Duarte Peres (advogado, OAB/SC 2010) é o '
          + 'interlocutor e o devedor solidário.'),
        caixaParte('Espaço Kairós aporta', 'A estrutura e a operação',
          ['Equipamentos e mobiliário: 57 itens, 325 peças (Anexo I)',
           'Marca e nome "Centro de Eventos Kairós"',
           'CNPJ já ativo e perfis em redes sociais',
           'Carteira de clientes e reputação de mercado'],
          'Continua pagando por fora: reposição de equipamento por desgaste, seguro dos '
          + 'equipamentos e o imposto sobre a receita.'),
      ),

      // -------------------------------------------------------- dinheiro
      parLadoALado(
        [secao('Como o dinheiro é dividido'), ...caixaDestaque('50/50', [
          ['Nas ', ['datas comercializadas', 1], ', tudo que o espaço arrecada entra numa '
           + 'conta própria da parceria. Dela saem ', ['somente os custos da operação', 1],
           ' — a lista é fechada — e ', ['o que sobra é dividido em duas partes iguais', 1],
           '. Prejuízo no mês, os dois cobrem meio a meio. Ninguém tem pró-labore.'],
        ])],
        [secao('As duas datas mensais de Gilberto'), ...caixaDestaque('2', [
          ['Gilberto tem ', ['duas datas por mês', 1], ' para seus eventos — imersões, '
           + 'treinamentos, palestras, gravações —, ',
           ['sem custo de locação do espaço nem de uso dos equipamentos', 1],
           '. A receita dessas datas é ', ['integralmente dele', 1], ' e não entra no rateio. '
           + 'Ele paga só os custos variáveis do dia. Indicadas com 30 dias de antecedência, '
           + 'têm preferência na agenda. Não são cumulativas.'],
        ])],
      ),

      tabelaRotulos([
        ['Únicos custos abatidos', ['Só o custo direto do evento: ', 1],
         'operador técnico, limpeza, segurança e equipe de evento.'],
        ['Não pode ser abatido', ['Lista fechada: ', 1],
         'pró-labore, taxa de administração, aluguel ou IPTU, energia, água, internet, '
         + 'portaria, ECAD, manutenção predial e dos equipamentos, royalty de marca, '
         + 'depreciação e despesa estranha à operação. Sem nota fiscal idônea não entra.'],
        ['Fica com cada um', ['Motor em Ação: ', 1], 'imóvel, manutenção predial e manutenção '
         + 'dos equipamentos. ', ['Kairós: ', 1], 'só a reposição por desgaste. Conserto é '
         + 'deles, substituição é sua.'],
        ['Apuração e repasse', 'Fechamento ', ['mensal', 1], ', com demonstrativo de cada '
         + 'data, receita, custo e memória de cálculo. Repasse logo após.'],
      ], 2600),

      // -------------------------------------------------------- controle
      secao('Controle, preços e decisões'),
      tabelaRotulos([
        ['Conta e transparência', ['Contas separadas. ', 1], 'A Kairós fatura, recebe, abate '
         + 'o custo operacional do evento e repassa ', ['50% do saldo líquido', 1],
         ', com demonstrativo e notas. Valor recebido pela Motor em Ação volta para a Kairós '
         + 'em 48 horas.'],
        ['Preços, agenda e decisões', 'Tabela só muda de comum acordo; agenda única, por '
         + 'ordem de registro. Preços, equipe fixa, investimento, dívida, mudança de nome e '
         + 'contrato longo exigem acordo escrito.'],
      ], 2600),

      // -------------------------------------------------------- comodato
      parLadoALado(
        [secao('O comodato dos equipamentos'),
         ...[
           ['Prazo', '24 meses, do termo de entrega, renovando junto com a parceria. Nenhum '
            + 'bem vai para o espaço antes do termo assinado, com fotos.'],
           ['Retirada por vontade própria', 'Kairós pode retirar os bens avisando por escrito '
            + 'com 90 dias. É aviso, não pedido de autorização.'],
           ['Retirada imediata', 'Sem aviso nenhum em caso de fim do contrato, inadimplência, '
            + 'risco aos bens ou manutenção.'],
           ['Propriedade', 'Seguem da Kairós (ou de Gilberto, conforme o inventário) e não se '
            + 'incorporam ao imóvel, mesmo instalados em caráter permanente. Motor em Ação é '
            + 'depositária, sem direito de retenção.'],
           ['Manutenção', 'Motor em Ação paga a manutenção dos equipamentos, mas a Kairós '
            + 'escolhe o técnico e executa.'],
           ['Garantia pessoal', 'Luciano Duarte Peres — advogado, OAB/SC 2010, solteiro — '
            + 'responde com o patrimônio pessoal, como devedor solidário, sem benefício de '
            + 'ordem. Vale mesmo que ele saia da empresa. Sendo solteiro, não há outorga de '
            + 'cônjuge a colher.'],
           ['Marca, CNPJ e redes', 'Seguem sendo da Kairós, licenciados à Motor em Ação só '
            + 'enquanto durar a parceria.'],
         ].map(([rot, val]) => p([
           new TextRun({ text: rot + ': ', bold: true, size: 15, color: TINTA }),
           new TextRun({ text: val, size: 15, color: TINTA }),
         ]))],
        [secao('Prazo e saída'),
         ...[
           ['Vigência', '24 meses, renovando sozinha. Para não renovar, aviso escrito com 90 '
            + 'dias. Parceria e comodato começam e terminam juntos.'],
           ['Eventos já vendidos', 'São honrados até a data de realização, com o rateio '
            + 'mantido.'],
           ['No encerramento', 'Equipamentos voltam para a Kairós em até 30 dias. A licença da '
            + 'marca cessa e a Motor em Ação remove toda referência ao "Centro de Eventos '
            + 'Kairós". Acerto de contas em 30 dias.'],
           ['Depois da saída', 'Sigilo por 2 anos. Motor em Ação pode seguir com o imóvel, com '
            + 'marca própria, sem usar a marca, a carteira ou os equipamentos da Kairós.'],
         ].map(([rot, val]) => p([
           new TextRun({ text: rot + ': ', bold: true, size: 15, color: TINTA }),
           new TextRun({ text: val, size: 15, color: TINTA }),
         ]))],
      ),

      // --------------------------------------------------------- abertos
      secao('Pontos ainda em aberto'),
      ...[
        ['Em que qualidade o Luciano assinou? ', 'Ele e o Davi assinaram pela Motor em Ação. '
         + 'Se ele assinou só como representante, a garantia pessoal não se constituiu — por '
         + 'mais que o texto a descreva. Garantidor assina em nome próprio. Olhe o papel.'],
        ['O contrato tem cláusulas que o papel assinado não tinha. ', 'O garantidor do outro '
         + 'lado é advogado e vai comparar. Os dois pontos que ele deve contestar são a '
         + 'retirada dos equipamentos ("solicitar" × "avisar") e a contagem do inventário.'],
        ['O imposto ficou todo com você. ', 'O tributo sobre a receita não é abatido antes da '
         + 'divisão, e o faturamento sai no seu CNPJ. Cerca de R$ 600 por evento do seu bolso.'],
        ['Vale tentar o Davi também como devedor solidário. ', 'Quem aparece como sócio é ele. '
         + 'Dois garantidores valem mais que um.'],
        ['Endereço do imóvel e inventário definitivo ', 'com série, titularidade e valor de '
         + 'reposição, assinado na apuração dos 30 dias.'],
        ['Valores ', 'da multa por violação e da cobertura do seguro de responsabilidade '
         + 'civil, além do foro e da data de início.'],
      ].map(([forte, resto], i) => p([
        new TextRun({ text: `${i + 1}. `, bold: true, size: 15, color: ACENTO }),
        new TextRun({ text: forte, bold: true, size: 15, color: TINTA }),
        new TextRun({ text: resto, size: 15, color: TINTA }),
      ], { indent: { left: 180, hanging: 180 } })),

      // --------------------------------------------------------- rodape
      p([new TextRun({
        text: 'Versão de trabalho · 28/09/2026 · o documento assinado está em arquivo próprio'
            + '  ·  Sujeito a revisão jurídica antes da assinatura',
        size: 12, color: FRACO,
      })], { spacing: { before: 100 },
             border: { top: { style: BorderStyle.SINGLE, size: 2, color: LINHA, space: 3 } } }),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const saida = __dirname + '/Resumo da Parceria - editavel.docx';
  fs.writeFileSync(saida, buf);
  console.log('gerado: Resumo da Parceria - editavel.docx');
});

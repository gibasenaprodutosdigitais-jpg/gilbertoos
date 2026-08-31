// ============================================================================
// REFERÊNCIA JURÍDICA DO LAUDO — verbetes conferidos contra a fonte primária
// ============================================================================
// ☠️ NÃO EDITAR O CAMPO `texto` DE CABEÇA. Ele é TRANSCRITO do que a fonte
//    devolve (`node motor/conferir-lei.mjs --baixar`) e conferido por máquina
//    (`node motor/conferir-lei.mjs`). Enunciado de súmula e tese de repetitivo
//    não sobrevivem a paráfrase: uma palavra trocada muda quem ganha a causa.
//
//    A primeira rodada de conferência derrubou TRÊS suposições escritas de
//    cabeça, e nenhuma delas parecia errada:
//      · Súmula 472 — o verbo não é "vedada a cumulação". É "EXCLUI A
//        EXIGIBILIDADE" dos juros e da multa. Efeito diferente.
//      · Tema 618 — "válida ATÉ 30/04/2008", não "vedada a partir de".
//        Um dia, e a conclusão sobre o contrato inverte.
//      · Tema 958 — a tarifa de avaliação do bem é VÁLIDA em regra; a
//        abusividade é a EXCEÇÃO (serviço não prestado). Eu tinha a moldura
//        invertida, o que faria o laudo acusar o que a Corte validou.
//
// ⚠️ `ancoras` são os trechos que a conferência exige encontrar no texto
//    oficial — o contrato entre este arquivo e a fonte. Incluir sempre os
//    NÚMEROS e as DATAS, que é onde o erro se esconde.
//
// ⚠️ O motor (`motor/achados.mjs`) referencia estes verbetes por CHAVE e não
//    contém texto de lei nenhum. Quem escreve o laudo lê daqui.
// ============================================================================

const sumula = (n) =>
  `https://processo.stj.jus.br/SCON/sumstj/toc.jsp?livre=%40num%3D%27${n}%27`;

const tema = (n) =>
  "https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp" +
  `?novaConsulta=true&tipo_pesquisa=T&cod_tema_inicial=${n}&cod_tema_final=${n}`;

export const VERBETES = [
  {
    chave: "sumula-539",
    rotulo: "Súmula 539/STJ",
    assunto: "Capitalização de juros: permitida se expressamente pactuada",
    conferidor: "stj-sumula",
    fonte: sumula(539),
    texto:
      "É permitida a capitalização de juros com periodicidade inferior à anual " +
      "em contratos celebrados com instituições integrantes do Sistema " +
      "Financeiro Nacional a partir de 31/3/2000 (MP n. 1.963-17/2000, " +
      "reeditada como MP n. 2.170-36/2001), desde que expressamente pactuada.",
    ancoras: [
      "capitalização de juros com periodicidade inferior à anual",
      "31/3/2000",
      "desde que expressamente pactuada",
    ],
    comoUsarNoLaudo:
      "A capitalização mensal NÃO é ilegal por si só. O ponto pericial é " +
      "verificar se houve pactuação expressa — e é isso que o laudo apura, " +
      "não a legalidade do sistema Price em abstrato.",
  },
  {
    chave: "sumula-541",
    rotulo: "Súmula 541/STJ",
    assunto: "Taxa anual superior ao duodécuplo da mensal já é pactuação suficiente",
    conferidor: "stj-sumula",
    fonte: sumula(541),
    texto:
      "A previsão no contrato bancário de taxa de juros anual superior ao " +
      "duodécuplo da mensal é suficiente para permitir a cobrança da taxa " +
      "efetiva anual contratada.",
    ancoras: ["duodécuplo da mensal", "taxa efetiva anual contratada"],
    comoUsarNoLaudo:
      "É a régua objetiva do achado de capitalização: se a taxa anual do " +
      "instrumento supera o duodécuplo da mensal, a pactuação está atendida. " +
      "Se é IGUAL ao duodécuplo, não há a pactuação por essa via.",
  },
  {
    chave: "sumula-382",
    rotulo: "Súmula 382/STJ",
    assunto: "Juros acima de 12% ao ano não indicam abusividade por si sós",
    conferidor: "stj-sumula",
    fonte: sumula(382),
    texto:
      "A estipulação de juros remuneratórios superiores a 12% ao ano, por si " +
      "só, não indica abusividade.",
    ancoras: ["juros remuneratórios superiores a 12% ao ano", "não indica abusividade"],
    comoUsarNoLaudo:
      "Impede a conclusão preguiçosa de que taxa alta = taxa abusiva. O laudo " +
      "apura percentuais e os compara; não decreta abusividade por patamar.",
  },
  {
    chave: "sumula-472",
    rotulo: "Súmula 472/STJ",
    assunto: "Comissão de permanência exclui a exigibilidade dos demais encargos",
    conferidor: "stj-sumula",
    fonte: sumula(472),
    texto:
      "A cobrança de comissão de permanência - cujo valor não pode ultrapassar " +
      "a soma dos encargos remuneratórios e moratórios previstos no contrato - " +
      "exclui a exigibilidade dos juros remuneratórios, moratórios e da multa " +
      "contratual.",
    // ☠️ a âncora anterior ("vedada a sua cumulação") NÃO EXISTE no enunciado
    ancoras: [
      "não pode ultrapassar a soma dos encargos remuneratórios e moratórios",
      "exclui a exigibilidade dos juros remuneratórios, moratórios e da multa contratual",
    ],
    comoUsarNoLaudo:
      "O efeito não é 'vedar a cumulação' em abstrato: é EXCLUIR a " +
      "exigibilidade dos demais encargos, e limitar o valor da própria " +
      "comissão à soma dos encargos previstos. São dois pontos de apuração " +
      "distintos, e o laudo trata dos dois.",
  },
  {
    chave: "tema-25",
    rotulo: "Tema 25/STJ",
    assunto: "Patamar de juros não indica abusividade (par repetitivo da Súmula 382)",
    conferidor: "stj-tema",
    fonte: tema(25),
    texto:
      "A estipulação de juros remuneratórios superiores a 12% ao ano, por si " +
      "só, não indica abusividade.",
    ancoras: ["superiores a 12% ao ano", "não indica abusividade"],
    comoUsarNoLaudo: "Mesmo conteúdo da Súmula 382, em sede de repetitivo.",
  },
  {
    chave: "tema-27",
    rotulo: "Tema 27/STJ",
    assunto: "Revisão de juros só em situação excepcional, com abusividade demonstrada",
    conferidor: "stj-tema",
    fonte: tema(27),
    texto:
      "É admitida a revisão das taxas de juros remuneratórios em situações " +
      "excepcionais, desde que caracterizada a relação de consumo e que a " +
      "abusividade (capaz de colocar o consumidor em desvantagem exagerada " +
      "(art. 51, §1 º, do CDC) fique cabalmente demonstrada, ante às " +
      "peculiaridades do julgamento em concreto.",
    ancoras: [
      "revisão das taxas de juros remuneratórios em situações excepcionais",
      "cabalmente demonstrada",
    ],
    // ☠️ NÃO EXISTE tese firmada dizendo "taxa média de mercado". Foi
    //    conferido nos temas 24 a 28: nenhum traz esse critério no enunciado.
    //    A comparação com a média do BACEN é ELEMENTO DE PROVA da abusividade
    //    no caso concreto — não é limiar jurisprudencial, e o laudo não pode
    //    apresentá-la como se fosse.
    comoUsarNoLaudo:
      "Sustenta a comparação com a média do BACEN como MEIO DE PROVA da " +
      "abusividade no caso concreto. ☠️ NÃO afirmar que a jurisprudência fixou " +
      "a média de mercado como critério ou percentual: não existe tese firmada " +
      "nesse sentido (conferido nos Temas 24 a 28). O laudo apura a razão entre " +
      "a taxa e a média e a submete ao juízo — não decreta abusividade.",
  },
  {
    chave: "tema-28",
    rotulo: "Tema 28/STJ",
    assunto: "Abusividade nos encargos da normalidade descaracteriza a mora",
    conferidor: "stj-tema",
    fonte: tema(28),
    texto:
      "O reconhecimento da abusividade nos encargos exigidos no período da " +
      "normalidade contratual (juros remuneratórios e capitalização) " +
      "descaracteriza a mora.",
    ancoras: ["período da normalidade contratual", "descaracteriza a mora"],
    comoUsarNoLaudo:
      "Par obrigatório do item 3 do Tema 972: encargo ACESSÓRIO abusivo não " +
      "descaracteriza a mora, mas abusividade nos juros remuneratórios ou na " +
      "capitalização SIM. A distinção muda a conclusão e não pode ser omitida.",
  },
  {
    chave: "tema-618",
    rotulo: "Tema 618/STJ",
    assunto: "TAC e TEC: válidas em contratos celebrados até 30/04/2008",
    conferidor: "stj-tema",
    fonte: tema(618),
    texto:
      "Nos contratos bancários celebrados até 30/04/2008 (fim da vigência da " +
      "Resolução CMN 2.303/96) era válida a pactuação das Tarifas de Abertura " +
      "de Crédito (TAC) e de Emissão de Carnê (TEC), ou outra denominação para " +
      "o mesmo fato gerador, ressalvado o exame de abusividade em cada caso " +
      "concreto.",
    // ☠️ a data é a âncora mais importante do arquivo: o motor a tinha invertida
    ancoras: ["celebrados até 30/04/2008", "era válida a pactuação", "ressalvado o exame de abusividade"],
    comoUsarNoLaudo:
      "'Até 30/04/2008' INCLUI o dia 30/04. Contrato dessa data ou anterior: " +
      "pactuação válida, ressalvado o exame de abusividade concreto. A partir " +
      "de 01/05/2008: é achado.",
  },
  {
    chave: "tema-958",
    rotulo: "Tema 958/STJ",
    assunto: "Serviços de terceiros, correspondente bancário, avaliação do bem e registro",
    conferidor: "stj-tema",
    fonte: tema(958),
    texto:
      "2.1. Abusividade da cláusula que prevê a cobrança de ressarcimento de " +
      "serviços prestados por terceiros, sem a especificação do serviço a ser " +
      "efetivamente prestado; 2.2. Abusividade da cláusula que prevê o " +
      "ressarcimento pelo consumidor da comissão do correspondente bancário, " +
      "em contratos celebrados a partir de 25/02/2011, data de entrada em vigor " +
      "da Res.-CMN 3.954/2011, sendo válida a cláusula no período anterior a " +
      "essa resolução, ressalvado o controle da onerosidade excessiva; 2.3. " +
      "Validade da tarifa de avaliação do bem dado em garantia, bem como da " +
      "cláusula que prevê o ressarcimento de despesa com o registro do " +
      "contrato, ressalvadas a: 2.3.1. abusividade da cobrança por serviço não " +
      "efetivamente prestado; e a 2.3.2. possibilidade de controle da " +
      "onerosidade excessiva, em cada caso concreto.",
    ancoras: [
      "sem a especificação do serviço a ser efetivamente prestado",
      "a partir de 25/02/2011",
      "Validade da tarifa de avaliação do bem dado em garantia",
      "serviço não efetivamente prestado",
    ],
    // ☠️ A REGRA É A VALIDADE; a abusividade é a exceção. Eu tinha invertido,
    //    e o laudo acusaria justamente o que a Corte declarou válido.
    comoUsarNoLaudo:
      "Três regras distintas, e confundi-las é fatal: (a) serviços de TERCEIRO " +
      "sem especificação → abusivo; (b) comissão de CORRESPONDENTE bancário → " +
      "abusiva só a partir de 25/02/2011, válida antes; (c) tarifa de AVALIAÇÃO " +
      "do bem e ressarcimento de REGISTRO → VÁLIDAS em regra, abusivas apenas " +
      "se o serviço não foi efetivamente prestado ou por onerosidade excessiva. " +
      "O laudo NÃO acusa (c) de ofício: aponta como pendente de prova documental.",
  },
  {
    chave: "tema-972",
    rotulo: "Tema 972/STJ",
    assunto: "Pré-gravame, seguro imposto e efeito sobre a mora",
    conferidor: "stj-tema",
    fonte: tema(972),
    texto:
      "1 - Abusividade da cláusula que prevê o ressarcimento pelo consumidor da " +
      "despesa com o registro do pré-gravame, em contratos celebrados a partir " +
      "de 25/02/2011, data de entrada em vigor da Res.-CMN 3.954/2011, sendo " +
      "válida a cláusula pactuada no período anterior a essa resolução, " +
      "ressalvado o controle da onerosidade excessiva. 2 - Nos contratos " +
      "bancários em geral, o consumidor não pode ser compelido a contratar " +
      "seguro com a instituição financeira ou com seguradora por ela indicada. " +
      "3 - A abusividade de encargos acessórios do contrato não descaracteriza " +
      "a mora.",
    ancoras: [
      "registro do pré-gravame",
      "a partir de 25/02/2011",
      "não pode ser compelido a contratar seguro",
      "encargos acessórios do contrato não descaracteriza a mora",
    ],
    comoUsarNoLaudo:
      "O item 2 é o do seguro prestamista: a irregularidade é a IMPOSIÇÃO da " +
      "seguradora, não a existência do seguro. Perícia contábil não prova " +
      "imposição — por isso o achado é INCONCLUSIVO e aponta o que precisa ser " +
      "verificado. ⚠️ O item 3 é desfavorável ao mutuário e vai no laudo do " +
      "mesmo jeito: encargo acessório abusivo NÃO descaracteriza a mora " +
      "(mas ver o Tema 28 para os encargos da normalidade).",
  },
  {
    chave: "cdc-52",
    rotulo: "CDC, art. 52, § 1º (Lei 8.078/90)",
    assunto: "Multa de mora limitada a 2% do valor da prestação",
    conferidor: "planalto",
    fonte: "https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm",
    texto:
      "§ 1° As multas de mora decorrentes do inadimplemento de obrigações no " +
      "seu termo não poderão ser superiores a dois por cento do valor da " +
      "prestação. (Redação dada pela Lei nº 9.298, de 1º.8.1996)",
    ancoras: [
      "não poderão ser superiores a dois por cento do valor da prestação",
      "Lei nº 9.298",
    ],
    comoUsarNoLaudo:
      "Teto de 2% na redação da Lei 9.298/96, em vigor desde 01/08/1996. " +
      "⚠️ Conferir a data do contrato: os anteriores seguiam o teto de 10%. " +
      "★ O § 2º do mesmo artigo (liquidação antecipada com redução " +
      "proporcional dos juros e demais acréscimos) é o dispositivo a invocar " +
      "quando a perícia examinar quitação antecipada — é conta, e a perícia faz.",
  },

  {
    chave: "cpc-473",
    rotulo: "CPC, art. 473 (Lei 13.105/2015)",
    assunto: "Requisitos obrigatórios do laudo pericial",
    conferidor: "planalto",
    fonte: "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm",
    texto:
      "Art. 473. O laudo pericial deverá conter: I - a exposição do objeto da " +
      "perícia; II - a análise técnica ou científica realizada pelo perito; " +
      "III - a indicação do método utilizado, esclarecendo-o e demonstrando ser " +
      "predominantemente aceito pelos especialistas da área do conhecimento da " +
      "qual se originou; IV - resposta conclusiva a todos os quesitos " +
      "apresentados pelo juiz, pelas partes e pelo órgão do Ministério Público. " +
      "§ 1º No laudo, o perito deve apresentar sua fundamentação em linguagem " +
      "simples e com coerência lógica, indicando como alcançou suas conclusões. " +
      "§ 2º É vedado ao perito ultrapassar os limites de sua designação, bem " +
      "como emitir opiniões pessoais que excedam o exame técnico ou científico " +
      "do objeto da perícia.",
    ancoras: [
      "a exposição do objeto da perícia",
      "a indicação do método utilizado",
      "resposta conclusiva a todos os quesitos",
      "em linguagem simples e com coerência lógica",
      "emitir opiniões pessoais que excedam o exame técnico",
    ],
    // ★ Este é o verbete que MANDA NO FORMATO do laudo — é a régua que
    //   substitui o "modelo" que o Gilberto não tem.
    comoUsarNoLaudo:
      "É a estrutura obrigatória, e os quatro incisos viram as quatro seções " +
      "do documento. Três consequências diretas no desenho: " +
      "(a) o inciso III exige DECLARAR o método e mostrar que é aceito — daí o " +
      "quadro de método e a validação contra a Calculadora do Cidadão do BACEN; " +
      "(b) o inciso IV exige resposta conclusiva a TODOS os quesitos, então " +
      "quesito sem resposta é laudo incompleto, e 'não foi possível apurar' É " +
      "uma resposta conclusiva — omitir não é; " +
      "(c) ☠️ o § 2º VEDA opinião pessoal que exceda o exame técnico. É a base " +
      "normativa dos três estados do achado e da recusa a decretar abusividade: " +
      "o perito apura e demonstra; quem decide é o juízo.",
  },

  // ————————————————————————————————————————————————————————————————————————
  // SEM CONFERÊNCIA POR MÁQUINA
  // O BACEN serve o normativo em PDF atrás de uma SPA — não dá pra comparar
  // texto por HTTP. Ficam declarados como PENDENTES, e o conferidor os relata
  // em vez de fingir que estão conferidos.
  // ————————————————————————————————————————————————————————————————————————
  {
    chave: "cet-3517",
    rotulo: "Resolução CMN 3.517/2007",
    assunto: "CET — norma aplicável a contratos anteriores a 01/02/2021",
    conferidor: "manual",
    fonte: "https://normativos.bcb.gov.br/Lists/Normativos/Attachments/48005/Res_3517_v4_P.pdf",
    texto: null,
    ancoras: [],
    conferenciaManual:
      "PENDENTE — ☠️ REVOGADA pela Res. CMN 4.881/2020. Só se aplica a contrato " +
      "celebrado ANTES de 01/02/2021. Conferir a revogação no PDF antes de citar.",
  },
  {
    chave: "cet-4881",
    rotulo: "Resolução CMN 4.881/2020",
    assunto: "CET — norma vigente para contratos a partir de 01/02/2021",
    conferidor: "manual",
    fonte: "https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20CMN&numero=4881",
    texto: null,
    ancoras: [],
    conferenciaManual:
      "PENDENTE — conferir no PDF do BACEN a vigência (01/02/2021) e que " +
      "revogou a 3.517/2007, a 3.909/2010 e a 4.197/2013.",
  },
];

/** Verbete por chave. Lança se não existe — chave torta é erro de código. */
export function verbete(chave) {
  const v = VERBETES.find((x) => x.chave === chave);
  if (!v) throw new Error(`verbete inexistente: ${chave}`);
  return v;
}

/** Chaves cujo texto ainda não foi transcrito da fonte. */
export function naoTranscritos() {
  return VERBETES.filter((v) => !v.texto).map((v) => v.chave);
}

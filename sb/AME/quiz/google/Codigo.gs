/**
 * Imersão AME · recebe as respostas do quiz e grava no Google Sheets.
 *
 * Duas planilhas:
 *   - "Imersão AME · Acima de R$ 70 mil"  (faixas C e D do quiz)
 *   - "Imersão AME · Até R$ 70 mil"       (faixas A e B do quiz)
 *
 * Como usar (o passo a passo completo está no GUIA.md):
 *   1. Colar este código num projeto novo em script.google.com
 *   2. Rodar a função configurar() uma vez: ela cria as duas planilhas no
 *      seu Google Drive e mostra os links no registro de execução
 *   3. Implantar como "App da Web" (executar como: eu; acesso: qualquer pessoa)
 *   4. Copiar o link da implantação e colar no quiz, em PLANILHA_URL
 */

const ABA = 'Respostas';
const COLUNAS = [
  'Data e hora', 'Nome', 'WhatsApp', 'Instagram', 'Nicho',
  'Faturamento por mês', 'Maior dificuldade', 'Com as palavras dele', 'Origem'
];

// Faixas do quiz (27/out/2026). As duas de cima vão pra planilha "Acima de R$ 70 mil".
const FAIXAS_ACIMA_70 = ['De R$ 70 mil a R$ 120 mil', 'Acima de R$ 120 mil'];
const FAIXAS_ATE_70 = ['Até R$ 30 mil', 'De R$ 30 mil a R$ 70 mil'];

/** Rodar UMA vez, pelo editor. Cria as duas planilhas e guarda os endereços. */
function configurar() {
  const props = PropertiesService.getScriptProperties();
  const criadas = [];
  [['ACIMA_70', 'Imersão AME · Acima de R$ 70 mil'],
   ['ATE_70', 'Imersão AME · Até R$ 70 mil']].forEach(function (par) {
    let id = props.getProperty(par[0]);
    if (!id) {
      const planilha = SpreadsheetApp.create(par[1]);
      const aba = planilha.getSheets()[0];
      aba.setName(ABA);
      aba.getRange(1, 1, 1, COLUNAS.length).setValues([COLUNAS])
        .setFontWeight('bold').setBackground('#0C1A2E').setFontColor('#F2EFE8');
      aba.setFrozenRows(1);
      aba.setColumnWidths(1, COLUNAS.length, 180);
      id = planilha.getId();
      props.setProperty(par[0], id);
    }
    criadas.push(par[1] + ': ' + SpreadsheetApp.openById(id).getUrl());
  });
  Logger.log(criadas.join('\n'));
}

/** Recebe cada envio do quiz. */
function doPost(e) {
  const trava = LockService.getScriptLock();
  trava.waitLock(20000);
  try {
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const nome = limpa(d.nome);
    const faixa = limpa(d.faturamento);
    if (!nome || !faixa) return resposta({ ok: false, erro: 'faltou nome ou faturamento' });

    let chave;
    if (FAIXAS_ACIMA_70.indexOf(faixa) >= 0) chave = 'ACIMA_70';
    else if (FAIXAS_ATE_70.indexOf(faixa) >= 0) chave = 'ATE_70';
    else return resposta({ ok: false, erro: 'faixa desconhecida: ' + faixa });

    const id = PropertiesService.getScriptProperties().getProperty(chave);
    if (!id) return resposta({ ok: false, erro: 'rode configurar() primeiro' });

    const agora = Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm');
    SpreadsheetApp.openById(id).getSheetByName(ABA).appendRow([
      agora, nome, limpa(d.whatsapp), limpa(d.instagram) ? '@' + limpa(d.instagram) : '',
      limpa(d.nicho), faixa, limpa(d.dificuldade), limpa(d.dificuldade_texto), limpa(d.versao)
    ]);
    return resposta({ ok: true, planilha: chave });
  } catch (erro) {
    return resposta({ ok: false, erro: String(erro) });
  } finally {
    trava.releaseLock();
  }
}

/** Abrir o link do app no navegador mostra se ele está no ar. */
function doGet() {
  return resposta({ ok: true, app: 'Imersão AME · quiz' });
}

// Texto curto e sem fórmula: célula que começa com = + - @ vira texto puro.
function limpa(v) {
  let s = String(v == null ? '' : v).trim().slice(0, 2000);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

function resposta(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

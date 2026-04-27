'use strict';
const express = require('express');
const path    = require('path');
const https   = require('https');
const http    = require('http');
const XLSX    = require('xlsx');

const app  = express();
const PORT = process.env.PORT || 3000;

// ─── IDs das planilhas por mês (formato: "ANO-MES": "SHEET_ID") ──────────────
// O servidor lê automaticamente todas as planilhas configuradas aqui.
// Para adicionar um novo mês, basta adicionar uma linha com o ID da planilha.
const PLANILHAS = {
  '2026-01': '1wfHx4_JkhgqCBdMzFNFuiZdoAxCSpwOsAzHzapiUpIQ', // Janeiro 2026
  '2026-02': process.env.SHEET_FEV_2026 || '',                 // Fevereiro 2026
  '2026-03': process.env.SHEET_MAR_2026 || '',                 // Março 2026
};

const MESES_NOME = {
  '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
  '05': 'Maio',    '06': 'Junho',     '07': 'Julho', '08': 'Agosto',
  '09': 'Setembro','10': 'Outubro',   '11': 'Novembro','12': 'Dezembro'
};

// ─── Cache por planilha ───────────────────────────────────────────────────────
const cache     = {};   // { "2026-01": { data, ts } }
const CACHE_TTL = 30 * 60 * 1000; // 30 minutos

// ─── Helpers ─────────────────────────────────────────────────────────────────
function safeStr(v)  { return v == null ? '' : String(v).trim(); }
function safeInt(v)  { const n = parseInt(safeStr(v)); return isNaN(n) ? 0 : n; }
function safeFloat(v){ const n = parseFloat(safeStr(v).replace(',','.')); return isNaN(n) ? 0 : n; }
function safeDate(v) {
  if (!v) return '';
  if (v instanceof Date) return v.toLocaleDateString('pt-BR');
  return safeStr(v);
}

function downloadBuffer(url, maxRedirects = 5) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
      if ([301,302,303,307,308].includes(res.statusCode) && res.headers.location && maxRedirects > 0)
        return resolve(downloadBuffer(res.headers.location, maxRedirects - 1));
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode} em ${url}`));
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve(Buffer.concat(chunks)));
      res.on('error', reject);
    }).on('error', reject);
  });
}

// ─── Parser da aba Chamados ───────────────────────────────────────────────────
function parseChamados(ws) {
  const rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: null });
  if (rows.length < 2) return [];

  const headers = rows[0].map(h => safeStr(h));
  const idx = {};
  headers.forEach((h, i) => { idx[h] = i; });

  const chamados = [];
  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    if (!r || r[idx['Nº']] == null) continue;

    chamados.push({
      numero:        safeInt(r[idx['Nº']]),
      elt:           safeInt(r[idx['ELT']]),
      codPonto:      safeInt(r[idx['Cód Ponto']]),
      ponto:         safeStr(r[idx['Ponto']]),
      endereco:      safeStr(r[idx['Endereço']]),
      bairro:        safeStr(r[idx['Bairro']]),
      cidade:        safeStr(r[idx['Cidade']]),
      tipoEquip:     safeStr(r[idx['Tipo de Equipamento']]),
      nivel:         safeStr(r[idx['Nível']]),
      responsavel:   safeStr(r[idx['Responsável']]),
      tipoAtividade: safeStr(r[idx['Tipo de Atividade']]),
      origem:        safeStr(r[idx['Origem']]),
      dataCriacao:   safeDate(r[idx['Data de Criação']]),
      dataEncerramen:safeDate(r[idx['Data de Encerramento']]),
      tecnico:       safeStr(r[idx['Técnico']]),
      status:        safeStr(r[idx['Status']]),
      duracaoMin:    safeInt(r[idx['Duração Exec. em minutos']]),
      problemas:     safeStr(r[idx['Problemas Relatados']]),
      solucoes:      safeStr(r[idx['Soluções']]),
      estado:        safeStr(r[idx['Estado']]),
      praca:         safeStr(r[idx['Praça']]),
    });
  }
  return chamados;
}

// ─── Calcular métricas a partir dos chamados ──────────────────────────────────
function calcMetricas(chamados) {
  const total = chamados.length;
  const concluidos = chamados.filter(c =>
    c.status === 'Concluído' || c.status === 'Concluído pelo Sistema'
  ).length;

  const comDuracao = chamados.filter(c => c.duracaoMin > 0);
  const tempoMedio = comDuracao.length > 0
    ? Math.round(comDuracao.reduce((s, c) => s + c.duracaoMin, 0) / comDuracao.length)
    : 0;

  // Por nível
  const porNivel = {};
  chamados.forEach(c => {
    if (!c.nivel) return;
    porNivel[c.nivel] = (porNivel[c.nivel] || 0) + 1;
  });

  // Por técnico
  const porTecnico = {};
  chamados.forEach(c => {
    if (!c.tecnico) return;
    if (!porTecnico[c.tecnico]) porTecnico[c.tecnico] = { total: 0, concluidos: 0, duracaoTotal: 0 };
    porTecnico[c.tecnico].total++;
    if (c.status === 'Concluído' || c.status === 'Concluído pelo Sistema')
      porTecnico[c.tecnico].concluidos++;
    if (c.duracaoMin > 0) porTecnico[c.tecnico].duracaoTotal += c.duracaoMin;
  });

  // Por cidade
  const porCidade = {};
  chamados.forEach(c => {
    if (!c.cidade) return;
    porCidade[c.cidade] = (porCidade[c.cidade] || 0) + 1;
  });

  // Por tipo de atividade
  const porAtividade = {};
  chamados.forEach(c => {
    if (!c.tipoAtividade) return;
    porAtividade[c.tipoAtividade] = (porAtividade[c.tipoAtividade] || 0) + 1;
  });

  return { total, concluidos, tempoMedio, porNivel, porTecnico, porCidade, porAtividade };
}

// ─── Carregar dados de uma planilha ──────────────────────────────────────────
async function loadPlanilha(periodo, sheetId, force = false) {
  const now = Date.now();
  if (!force && cache[periodo] && (now - cache[periodo].ts) < CACHE_TTL)
    return cache[periodo].data;

  const url = `https://docs.google.com/spreadsheets/d/${sheetId}/export?format=xlsx`;
  console.log(`[data] Baixando planilha ${periodo}...`);

  const buf = await downloadBuffer(url);
  const wb  = XLSX.read(buf, { type: 'buffer', cellDates: true });

  let chamados = [];
  if (wb.SheetNames.includes('Chamados')) {
    chamados = parseChamados(wb.Sheets['Chamados']);
  }

  const metricas = calcMetricas(chamados);
  const data = { periodo, chamados, metricas, loadedAt: new Date().toISOString() };

  cache[periodo] = { data, ts: now };
  console.log(`[data] ${periodo} OK — ${chamados.length} chamados`);
  return data;
}

// ─── Carregar todos os períodos disponíveis ───────────────────────────────────
async function loadTodos(force = false) {
  const periodos = Object.entries(PLANILHAS).filter(([, id]) => id);
  const results  = {};

  await Promise.allSettled(
    periodos.map(async ([periodo, sheetId]) => {
      try {
        results[periodo] = await loadPlanilha(periodo, sheetId, force);
      } catch (err) {
        console.error(`[data] Erro ao carregar ${periodo}:`, err.message);
      }
    })
  );

  return results;
}

// ─── Pré-carregar na inicialização ────────────────────────────────────────────
loadTodos().catch(console.error);

// ─── Rotas ────────────────────────────────────────────────────────────────────
app.use(express.static(__dirname));

// Lista os períodos disponíveis
app.get('/api/periodos', (req, res) => {
  const lista = Object.entries(PLANILHAS)
    .filter(([, id]) => id)
    .map(([periodo]) => {
      const [ano, mes] = periodo.split('-');
      return {
        id: periodo,
        label: `${MESES_NOME[mes] || mes} ${ano}`,
        cached: !!cache[periodo],
      };
    });
  res.json(lista);
});

// Dados de um período específico
app.get('/api/data/:periodo', async (req, res) => {
  const { periodo } = req.params;
  const sheetId = PLANILHAS[periodo];
  if (!sheetId) return res.status(404).json({ error: 'Período não encontrado' });

  try {
    const data = await loadPlanilha(periodo, sheetId);
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Dados consolidados de todos os períodos (para gráficos de evolução)
app.get('/api/evolucao', async (req, res) => {
  try {
    const todos = await loadTodos();
    const evolucao = Object.entries(todos).map(([periodo, d]) => {
      const [ano, mes] = periodo.split('-');
      return {
        periodo,
        label: `${MESES_NOME[mes] || mes}/${ano}`,
        total: d.metricas.total,
        concluidos: d.metricas.concluidos,
        tempoMedio: d.metricas.tempoMedio,
      };
    });
    res.json(evolucao);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Forçar atualização do cache
app.get('/api/refresh', async (req, res) => {
  try {
    await loadTodos(true);
    res.json({ ok: true, ts: new Date().toISOString() });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('*', (req, res) =>
  res.sendFile(path.join(__dirname, 'index.html'))
);

app.listen(PORT, () => console.log(`🚀 Dashboard Eletromidia rodando na porta ${PORT}`));

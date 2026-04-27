# Dashboard Eletromidia — Relatórios Técnicos

Dashboard web para visualização de chamados técnicos mensais, lendo diretamente das planilhas Google Sheets.

## Estrutura

```
dashboard-eletromidia/
├── server.js          ← Backend Node.js + Express
├── public/
│   └── index.html     ← Frontend (HTML/CSS/JS puro)
├── package.json
├── Procfile           ← Para Railway
└── README.md
```

## Como adicionar um novo mês

Abra o `server.js` e localize o objeto `PLANILHAS`:

```js
const PLANILHAS = {
  '2026-01': 'ID_DA_PLANILHA_JANEIRO',
  '2026-02': 'ID_DA_PLANILHA_FEVEREIRO',
  // Adicione aqui:
  '2026-04': 'ID_DA_PLANILHA_ABRIL',
};
```

O ID da planilha é o código na URL do Google Sheets:
`https://docs.google.com/spreadsheets/d/**ID_AQUI**/edit`

> As planilhas precisam estar com acesso público ("Qualquer pessoa com o link").

## Deploy no Railway

1. Faça push do código para o GitHub
2. No Railway: **New Project → Deploy from GitHub repo**
3. Selecione o repositório `dashboard-eletromidia`
4. O Railway detecta o `Procfile` e faz o deploy automaticamente
5. Nenhuma variável de ambiente obrigatória

## Variáveis de ambiente opcionais

| Variável | Descrição |
|---|---|
| `PORT` | Porta do servidor (Railway injeta automaticamente) |
| `SHEET_FEV_2026` | ID da planilha de Fevereiro/2026 |
| `SHEET_MAR_2026` | ID da planilha de Março/2026 |

## Tecnologias

- **Node.js** + **Express** (backend)
- **XLSX** (leitura de planilhas)
- **Chart.js** (gráficos)
- **HTML/CSS/JS puro** (frontend)

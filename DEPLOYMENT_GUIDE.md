# Guia de Deploy - Dashboard Eletromidia

## Estrutura do Projeto

Este é um projeto React 19 + Vite com integração automática com Google Sheets.

### Arquivos Principais
- `client/src/` - Código-fonte React
- `server/index.ts` - Servidor Express
- `dist/` - Build produção (gerado automaticamente)

## Deploy no Railway

### Pré-requisitos
- Conta no Railway
- Repositório GitHub atualizado

### Passos

1. **Fazer push para GitHub**
   ```bash
   git add .
   git commit -m "Dashboard Eletromidia v2 - Integração Google Sheets"
   git push origin main
   ```

2. **Conectar ao Railway**
   - Acesse https://railway.app
   - Clique em "New Project"
   - Selecione "Deploy from GitHub"
   - Escolha o repositório `dashboard-eletromidia`

3. **Configurar Variáveis de Ambiente**
   - `NODE_ENV=production`
   - `PORT=3000` (padrão)

4. **Deploy Automático**
   - Railway detectará automaticamente `package.json`
   - Executará `pnpm install` e `pnpm build`
   - Iniciará com `pnpm start`

## Estrutura de Build

```
dist/
├── index.js          # Servidor Node.js
└── public/           # Arquivos estáticos
    ├── index.html    # SPA principal
    └── assets/       # CSS e JS compilados
```

## Google Sheets Integration

O dashboard busca automaticamente dados da planilha:
- **Sheet ID**: `1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58`
- **Atualização**: A cada 5 minutos
- **Abas Suportadas**: Qualquer aba com "Chamados" no nome

### Adicionar Novas Abas

1. Crie uma nova aba na planilha Google Sheets
2. Nomeie como "Chamados [Mês]" (ex: "Chamados Março")
3. Adicione as colunas: Ponto, Setor, Cidade, Tipo de Equipamento, Ambiente, Tipo de Falha
4. O dashboard detectará automaticamente na próxima atualização

## Troubleshooting

### Erro: "Nenhuma aba de chamados encontrada"
- Verifique se a planilha é pública (compartilhada com "Qualquer pessoa com o link")
- Confirme que o Sheet ID está correto
- Verifique se as abas contêm "Chamados" no nome

### Erro: "Cannot apply unknown utility class"
- Limpe cache: `rm -rf node_modules/.vite`
- Reinstale: `pnpm install`
- Reconstrua: `pnpm build`

### Gráficos não aparecem
- Verifique console do navegador (F12)
- Confirme que os dados estão sendo carregados
- Verifique se há dados suficientes na planilha

## Performance

- **Bundle Size**: ~1MB (gzip: ~300KB)
- **Tempo de Carregamento**: ~2-3 segundos
- **Atualização de Dados**: ~5 minutos
- **Suporte**: Todos os navegadores modernos

## Segurança

- Sem credenciais sensíveis no código
- Usa apenas CSV export público do Google Sheets
- CORS habilitado para acesso ao Google Sheets
- Sem autenticação necessária (dados públicos)

## Manutenção

### Atualizar Dependências
```bash
pnpm update
pnpm build
```

### Verificar Erros TypeScript
```bash
pnpm check
```

### Formatar Código
```bash
pnpm format
```

## Suporte

Para dúvidas ou problemas, consulte:
- Documentação React: https://react.dev
- Documentação Vite: https://vitejs.dev
- Documentação Railway: https://docs.railway.app

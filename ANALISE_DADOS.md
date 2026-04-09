# Análise da Planilha Google Sheets - Dashboard Eletromidia

## Estrutura de Dados Identificada

### Abas Encontradas
- **Chamados Janeiro** - Dados de chamados do mês de janeiro
- **Chamados Fevereiro** - Dados de chamados do mês de fevereiro
- Estrutura dinâmica: Novas abas serão adicionadas mensalmente

### Colunas Identificadas
1. **Ponto** - Identificador do ponto de venda
2. **Setor Bueno** - Localização/Setor
3. **Cidade** - Cidade onde está localizado
4. **Tipo de Equipamento** - Classificação do equipamento
5. **Ambiente** - Tipo de ambiente (Edifícios Comerciais, Shopping, etc)
6. **Tipo de Falha** - Classificação da falha

### Dados de Exemplo
- Clientes: Focus Business Center, N&B Business, Lozandes Business Tower, New World Concept Office
- Cidades: Goiânia, Vila Brasília Complemento, Park Lozandes
- Ambientes: Edifícios Comerciais, Shopping Coberturas
- Equipamentos: Diversos tipos

## Estratégia de Integração

### API Google Sheets
- URL Base: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}`
- Método: Busca automática de todas as abas via Google Sheets API
- Atualização: Em tempo real quando o usuário acessa o dashboard

### Processamento de Dados
1. Buscar lista de todas as abas disponíveis
2. Carregar dados de cada aba em paralelo
3. Normalizar estrutura de dados
4. Agregar métricas por período, localização, tipo de falha

### Métricas a Calcular
- Total de chamados por mês
- Chamados por localização/ponto
- Chamados por tipo de falha
- Chamados por ambiente
- Taxa de resolução
- Tendências mensais

## Tecnologia

### Frontend
- React 19 + TypeScript
- Recharts para visualizações
- Tailwind CSS 4 + shadcn/ui
- Integração com Google Sheets via CSV export

### Busca Automática de Abas
- Implementar função que detecta novas abas automaticamente
- Usar Google Sheets API com autenticação por chave pública
- Cache local com invalidação periódica

## Próximas Etapas
1. Criar design extraordinário do dashboard
2. Implementar integração com Google Sheets
3. Desenvolver visualizações de dados
4. Implementar busca automática de novas abas
5. Testar com dados reais

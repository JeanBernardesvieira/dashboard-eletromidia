# Dashboard Eletromidia - Análise de Chamados

Um dashboard profissional e moderno para visualização e análise de dados de chamados da Eletromidia, com integração automática com Google Sheets.

## 🎯 Características

- **Integração Google Sheets**: Busca automática de dados de todas as abas mensais
- **Visualizações em Tempo Real**: Gráficos interativos com Recharts
- **Design Minimalista Corporativo**: Interface elegante e profissional
- **Atualização Automática**: Dados atualizados a cada 5 minutos
- **Responsivo**: Funciona em desktop, tablet e mobile
- **Performance**: Build otimizado com Vite

## 📊 Visualizações

### Visão Geral
- Total de chamados
- Pontos ativos
- Tipos de falha identificados
- Média de chamados por mês
- Gráfico de tendência mensal
- Distribuição de tipos de falha
- Top 8 pontos com mais chamados

### Tendências
- Evolução mensal de chamados
- Análise de crescimento/redução

### Localizações
- Chamados por cidade
- Distribuição por ambiente

### Tipos de Falha
- Análise detalhada de falhas
- Categorização de problemas

## 🚀 Quick Start

### Desenvolvimento Local

```bash
# Instalar dependências
pnpm install

# Iniciar servidor de desenvolvimento
pnpm dev

# Acessar em http://localhost:3000
```

### Build para Produção

```bash
# Compilar projeto
pnpm build

# Testar build localmente
pnpm preview

# Iniciar servidor de produção
pnpm start
```

## 📋 Estrutura de Dados

A planilha Google Sheets deve conter as seguintes colunas:

| Coluna | Descrição |
|--------|-----------|
| Ponto | Identificador do ponto de venda |
| Setor | Localização/Setor |
| Cidade | Cidade onde está localizado |
| Tipo de Equipamento | Classificação do equipamento |
| Ambiente | Tipo de ambiente |
| Tipo de Falha | Classificação da falha |

## 🔧 Configuração

### Google Sheets

1. Abra a planilha em https://docs.google.com/spreadsheets/d/1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58
2. Compartilhe com "Qualquer pessoa com o link"
3. Crie novas abas com nome "Chamados [Mês]"
4. Adicione dados seguindo a estrutura acima

### Variáveis de Ambiente

Não há variáveis de ambiente obrigatórias. O dashboard usa apenas dados públicos do Google Sheets.

## 🎨 Design

- **Tipografia**: Poppins (display) + Inter (body)
- **Paleta**: Azul profundo + Verde esmeralda + Vermelho coral
- **Tema**: Light (claro)
- **Componentes**: shadcn/ui + Recharts

## 📦 Dependências Principais

- **React 19**: Framework UI
- **Vite**: Build tool
- **Recharts**: Visualizações de dados
- **Tailwind CSS 4**: Styling
- **shadcn/ui**: Componentes UI
- **Lucide React**: Ícones
- **Express**: Servidor

## 🚢 Deploy

### Railway

1. Conecte seu repositório GitHub ao Railway
2. Configure variáveis de ambiente se necessário
3. Deploy automático em cada push para `main`

Ver [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) para instruções detalhadas.

## 🔄 Atualização de Dados

O dashboard busca dados automaticamente:
- **Intervalo**: A cada 5 minutos
- **Fonte**: Google Sheets CSV export
- **Abas**: Detecta automaticamente abas com "Chamados" no nome
- **Sem Cache**: Sempre busca dados mais recentes

## 🐛 Troubleshooting

### Dados não carregam
- Verifique se a planilha é pública
- Confirme o Sheet ID está correto
- Verifique console do navegador (F12)

### Gráficos vazios
- Certifique-se de que há dados na planilha
- Verifique se as colunas estão nomeadas corretamente
- Aguarde 5 minutos para atualização

### Erro de compilação
```bash
# Limpar cache e reinstalar
rm -rf node_modules .pnpm-store
pnpm install
pnpm build
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
2. Consulte logs do servidor
3. Verifique console do navegador (F12)

## 📄 Licença

Propriedade da Eletromidia

## 🔗 Links Úteis

- [Planilha Google Sheets](https://docs.google.com/spreadsheets/d/1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58)
- [Dashboard em Produção](https://dashboard-eletromidia.railway.app)
- [Repositório GitHub](https://github.com/JeanBernardesvieira/dashboard-eletromidia)

---

**Versão**: 2.0.0  
**Última Atualização**: Abril 2026  
**Status**: ✅ Em Produção

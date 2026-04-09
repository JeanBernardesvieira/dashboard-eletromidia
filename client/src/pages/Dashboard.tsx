import { useState } from 'react';
import { Sidebar } from '@/components/Sidebar';
import { MetricCard } from '@/components/MetricCard';
import { useGoogleSheets, calculateStats } from '@/hooks/useGoogleSheets';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, TrendingUp, MapPin, Zap } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

/**
 * Dashboard principal com visualizacoes de dados do Google Sheets
 * Design: Minimalismo Corporativo Sofisticado
 */
export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const { sheets, loading, error } = useGoogleSheets();

  const stats = sheets.length > 0 ? calculateStats(sheets) : null;

  // Cores para gráficos
  const chartColors = ['#0072b1', '#0088cc', '#00a3e0', '#00b8d4', '#00c9a7'];

  // Preparar dados para gráficos
  const porPontoData = stats
    ? Object.entries(stats.porPonto)
        .sort(([, a], [, b]) => (b as number) - (a as number))
        .slice(0, 8)
        .map(([name, value]) => ({ name, value }))
    : [];

  const porTipoFalhaData = stats
    ? Object.entries(stats.porTipoFalha)
        .sort(([, a], [, b]) => (b as number) - (a as number))
        .slice(0, 6)
        .map(([name, value]) => ({ name, value }))
    : [];

  const porCidadeData = stats
    ? Object.entries(stats.porCidade)
        .sort(([, a], [, b]) => (b as number) - (a as number))
        .map(([name, value]) => ({ name, value }))
    : [];

  const porAmbienteData = stats
    ? Object.entries(stats.porAmbiente)
        .sort(([, a], [, b]) => (b as number) - (a as number))
        .map(([name, value]) => ({ name, value }))
    : [];

  // Dados de tendencia mensal
  const trendData = sheets.map((sheet) => ({
    mes: sheet.name.replace('Chamados ', ''),
    chamados: sheet.data.length,
  }));

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <Card className="p-8 max-w-md">
          <div className="flex items-center gap-3 mb-4">
            <AlertCircle className="w-6 h-6 text-destructive" />
            <h2 className="text-lg font-bold">Erro ao carregar dados</h2>
          </div>
          <p className="text-sm text-muted-foreground">{error}</p>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar */}
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {/* Header */}
        <div
          className="bg-cover bg-center relative h-48 border-b border-border"
          style={{
            backgroundImage:
              'url(https://d2xsxph8kpxj0f.cloudfront.net/310519663107643057/hJHwAjrQfsCVvFZ7YyEkkQ/hero-dashboard-gtLP8oYwgnMktdCNXjcJ5y.webp)',
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-primary/80 to-accent/60 flex items-end">
            <div className="p-8">
              <h1 className="text-4xl font-bold text-white mb-2">Dashboard de Chamados</h1>
              <p className="text-white/90">Analise de dados mensais da Eletromidia</p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-8">
              {/* KPI Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {loading ? (
                  <>
                    {[1, 2, 3, 4].map((i) => (
                      <Skeleton key={i} className="h-32" />
                    ))}
                  </>
                ) : stats ? (
                  <>
                    <MetricCard
                      title="Total de Chamados"
                      value={stats.totalChamados}
                      subtitle={`${stats.totalMeses} meses analisados`}
                      icon={<Zap />}
                      color="primary"
                    />
                    <MetricCard
                      title="Pontos Ativos"
                      value={Object.keys(stats.porPonto).length}
                      subtitle="Localizacoes com chamados"
                      icon={<MapPin />}
                      color="accent"
                    />
                    <MetricCard
                      title="Tipos de Falha"
                      value={Object.keys(stats.porTipoFalha).length}
                      subtitle="Categorias identificadas"
                      icon={<AlertCircle />}
                      color="destructive"
                    />
                    <MetricCard
                      title="Media por Mes"
                      value={Math.round(stats.totalChamados / stats.totalMeses)}
                      subtitle="Chamados/mes"
                      icon={<TrendingUp />}
                      color="muted"
                    />
                  </>
                ) : null}
              </div>

              {/* Charts Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Tendencia Mensal */}
                <Card className="p-6">
                  <h3 className="text-lg font-bold mb-4">Tendencia Mensal</h3>
                  {loading ? (
                    <Skeleton className="h-64" />
                  ) : (
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={trendData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                        <XAxis dataKey="mes" />
                        <YAxis />
                        <Tooltip />
                        <Line
                          type="monotone"
                          dataKey="chamados"
                          stroke="#0072b1"
                          strokeWidth={2}
                          dot={{ fill: '#0072b1', r: 4 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  )}
                </Card>

                {/* Chamados por Tipo de Falha */}
                <Card className="p-6">
                  <h3 className="text-lg font-bold mb-4">Tipos de Falha</h3>
                  {loading ? (
                    <Skeleton className="h-64" />
                  ) : (
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={porTipoFalhaData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, value }) => `${name}: ${value}`}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {porTipoFalhaData.map((_, index) => (
                            <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  )}
                </Card>
              </div>

              {/* Chamados por Ponto */}
              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4">Chamados por Ponto (Top 8)</h3>
                {loading ? (
                  <Skeleton className="h-64" />
                ) : (
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={porPontoData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} interval={0} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#0072b1" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                )}
              </Card>
            </div>
          )}

          {/* Trends Tab */}
          {activeTab === 'trends' && (
            <div className="space-y-6">
              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4">Evolucao Mensal</h3>
                {loading ? (
                  <Skeleton className="h-64" />
                ) : (
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={trendData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis dataKey="mes" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="chamados"
                        stroke="#0072b1"
                        strokeWidth={3}
                        dot={{ fill: '#0072b1', r: 6 }}
                        activeDot={{ r: 8 }}
                        name="Chamados"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                )}
              </Card>
            </div>
          )}

          {/* Locations Tab */}
          {activeTab === 'locations' && (
            <div className="space-y-6">
              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4">Chamados por Cidade</h3>
                {loading ? (
                  <Skeleton className="h-64" />
                ) : (
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={porCidadeData} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis type="number" />
                      <YAxis dataKey="name" type="category" width={150} />
                      <Tooltip />
                      <Bar dataKey="value" fill="#00a3e0" radius={[0, 8, 8, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                )}
              </Card>

              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4">Chamados por Ambiente</h3>
                {loading ? (
                  <Skeleton className="h-64" />
                ) : (
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={porAmbienteData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, value }) => `${name}: ${value}`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {porAmbienteData.map((_, index) => (
                          <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                )}
              </Card>
            </div>
          )}

          {/* Failures Tab */}
          {activeTab === 'failures' && (
            <div className="space-y-6">
              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4">Analise de Tipos de Falha</h3>
                {loading ? (
                  <Skeleton className="h-64" />
                ) : (
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={porTipoFalhaData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#00b8d4" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                )}
              </Card>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

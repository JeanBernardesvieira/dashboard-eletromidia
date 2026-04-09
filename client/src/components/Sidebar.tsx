import { BarChart3, TrendingUp, MapPin, AlertCircle, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  const tabs = [
    {
      id: 'overview',
      label: 'Visao Geral',
      icon: BarChart3,
    },
    {
      id: 'trends',
      label: 'Tendencias',
      icon: TrendingUp,
    },
    {
      id: 'locations',
      label: 'Localizacoes',
      icon: MapPin,
    },
    {
      id: 'failures',
      label: 'Tipos de Falha',
      icon: AlertCircle,
    },
  ];

  return (
    <aside className="w-64 bg-sidebar border-r border-sidebar-border min-h-screen flex flex-col p-6">
      {/* Logo/Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-sidebar-foreground">Eletromidia</h1>
        <p className="text-xs text-sidebar-accent-foreground mt-1">Dashboard de Chamados</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-2">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <Button
              key={tab.id}
              variant={isActive ? 'default' : 'ghost'}
              className="w-full justify-start gap-3"
              onClick={() => onTabChange(tab.id)}
            >
              <Icon className="w-5 h-5" />
              <span>{tab.label}</span>
            </Button>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-sidebar-border pt-4">
        <Button variant="ghost" className="w-full justify-start gap-3 text-sidebar-accent-foreground">
          <Settings className="w-5 h-5" />
          <span className="text-sm">Configuracoes</span>
        </Button>
        <p className="text-xs text-sidebar-accent-foreground mt-4 px-2">
          Dados atualizados a cada 5 minutos
        </p>
      </div>
    </aside>
  );
}

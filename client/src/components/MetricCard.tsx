import { ReactNode } from 'react';
import { Card } from '@/components/ui/card';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: ReactNode;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  color?: 'primary' | 'accent' | 'destructive' | 'muted';
}

/**
 * Card de metrica com design minimalista corporativo
 * Exibe KPI principal com icone, subtitulo e tendencia opcional
 */
export function MetricCard({
  title,
  value,
  subtitle,
  icon,
  trend,
  color = 'primary',
}: MetricCardProps) {
  const colorClasses: Record<string, string> = {
    primary: 'border-l-primary',
    accent: 'border-l-accent',
    destructive: 'border-l-destructive',
    muted: 'border-l-muted',
  };

  const trendColor = trend?.isPositive ? 'text-accent' : 'text-destructive';
  const trendSymbol = trend?.isPositive ? '↑' : '↓';

  return (
    <Card className={`border-l-4 ${colorClasses[color]} p-6 hover:shadow-md transition-shadow duration-300`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-muted-foreground mb-2">{title}</p>
          <h3 className="text-3xl font-bold text-foreground mb-1">{value}</h3>
          {subtitle && <p className="text-xs text-muted-foreground">{subtitle}</p>}
        </div>
        {icon && <div className="ml-4 text-2xl opacity-60">{icon}</div>}
      </div>

      {trend && (
        <div className={`mt-4 text-sm font-medium ${trendColor}`}>
          {trendSymbol} {Math.abs(trend.value)}% vs periodo anterior
        </div>
      )}
    </Card>
  );
}

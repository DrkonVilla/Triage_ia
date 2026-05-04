import { Activity, Clock, CheckCircle, AlertTriangle } from 'lucide-react';

interface KPICardsProps {
  kpis: {
    total_triajes: number;
    promedio_tiempo: number;
    tasa_concurrencia_ia: number;
    criticos_atendidos: number;
  };
}

export const KPICards: React.FC<KPICardsProps> = ({ kpis }) => {
  const cards = [
    {
      title: 'Total Triajes',
      value: kpis.total_triajes,
      icon: Activity,
      color: 'bg-blue-500',
      change: '+12% vs mes anterior'
    },
    {
      title: 'Tiempo Promedio',
      value: `${kpis.promedio_tiempo} min`,
      icon: Clock,
      color: 'bg-green-500',
      change: '-2 min vs meta'
    },
    {
      title: 'Concurrencia IA',
      value: `${kpis.tasa_concurrencia_ia}%`,
      icon: CheckCircle,
      color: 'bg-purple-500',
      change: 'Nivel de confianza'
    },
    {
      title: 'Críticos Atendidos',
      value: kpis.criticos_atendidos,
      icon: AlertTriangle,
      color: 'bg-red-500',
      change: 'Prioridad máxima'
    }
  ];
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, idx) => (
        <div key={idx} className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 mb-1">{card.title}</p>
              <p className="text-2xl font-bold">{card.value}</p>
              <p className="text-xs text-gray-400 mt-2">{card.change}</p>
            </div>
            <div className={`${card.color} p-3 rounded-full`}>
              <card.icon className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

interface TiempoAreaChartProps {
  data: {
    semana: string;
    promedio: number;
    meta: number;
  }[];
}

export const TiempoAreaChart: React.FC<TiempoAreaChartProps> = ({ data }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold mb-4">
        Evolución Semanal del Tiempo de Triaje
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="semana" />
          <YAxis label={{ value: 'Minutos', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Area
            type="monotone"
            dataKey="promedio"
            stroke="#4f46e5"
            fill="#eef2ff"
            name="Tiempo promedio"
          />
          <ReferenceLine
            y={data[0]?.meta || 5}
            label="Meta (5 min)"
            stroke="#ef4444"
            strokeDasharray="5 5"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
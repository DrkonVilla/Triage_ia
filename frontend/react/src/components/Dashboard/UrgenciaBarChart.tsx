import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface UrgenciaBarChartProps {
  data: {
    mes: string;
    RED: number;
    ORANGE: number;
    YELLOW: number;
    GREEN: number;
    BLUE: number;
  }[];
}

const COLORS = {
  RED: '#ef4444',
  ORANGE: '#f97316',
  YELLOW: '#eab308',
  GREEN: '#22c55e',
  BLUE: '#3b82f6'
};

export const UrgenciaBarChart: React.FC<UrgenciaBarChartProps> = ({ data }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold mb-4">Volumen Mensual por Nivel de Urgencia</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="mes" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="RED" fill={COLORS.RED} name="Crítico" />
          <Bar dataKey="ORANGE" fill={COLORS.ORANGE} name="Urgente" />
          <Bar dataKey="YELLOW" fill={COLORS.YELLOW} name="Poco Urgente" />
          <Bar dataKey="GREEN" fill={COLORS.GREEN} name="No Urgente" />
          <Bar dataKey="BLUE" fill={COLORS.BLUE} name="Administrativo" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
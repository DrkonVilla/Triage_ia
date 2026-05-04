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

interface ConfianzaBarChartProps {
  data: {
    nivel: string;
    ia: number;
    humano: number;
  }[];
}

export const ConfianzaBarChart: React.FC<ConfianzaBarChartProps> = ({ data }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold mb-4">
        Comparativa: IA vs Enfermera (Último mes)
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="nivel" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="ia" fill="#6366f1" name="Sugerido por IA" />
          <Bar dataKey="humano" fill="#10b981" name="Confirmado por Enfermera" />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-sm text-gray-500 mt-4 text-center">
        📊 La diferencia indica discrepancias en la evaluación del sistema
      </p>
    </div>
  );
};
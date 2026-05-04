import { useState, useEffect } from 'react';
import { KPICards } from '../components/Dashboard/KPICards';
import { DateRangeFilter } from '../components/Dashboard/DateRangeFilter';
import { UrgenciaBarChart } from '../components/Dashboard/UrgenciaBarChart';
import { ConfianzaBarChart } from '../components/Dashboard/ConfianzaBarChart';
import { TiempoAreaChart } from '../components/Dashboard/TiempoAreaChart';
import { dashboardService } from '../services/api';
import { subDays, format } from 'date-fns';
import { es } from 'date-fns/locale';

export const DashboardGestion: React.FC = () => {
  const [startDate, setStartDate] = useState(subDays(new Date(), 30));
  const [endDate, setEndDate] = useState(new Date());
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadDashboardData();
  }, [startDate, endDate]);
  
  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const data = await dashboardService.getDashboardData(
        format(startDate, 'yyyy-MM-dd'),
        format(endDate, 'yyyy-MM-dd')
      );
      setDashboardData(data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }
  
  if (!dashboardData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Error cargando datos del dashboard</p>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard de Gestión</h1>
        <DateRangeFilter
          startDate={startDate}
          endDate={endDate}
          onRangeChange={(start, end) => {
            setStartDate(start);
            setEndDate(end);
          }}
        />
      </div>
      
      <KPICards kpis={dashboardData.kpis} />
      
      {/* Guía de Interpretación */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-lg font-semibold text-blue-800 mb-2 flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Cómo Interpretar los Gráficos
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-blue-700">
          <div>
            <h4 className="font-semibold mb-1">Volumen por Nivel de Urgencia</h4>
            <p>Muestra la cantidad de pacientes atendidos por mes, clasificados por color de triaje:</p>
            <ul className="list-disc list-inside mt-1 text-xs">
              <li><span className="text-red-600 font-semibold">RED</span>: Críticos (atención inmediata)</li>
              <li><span className="text-orange-600 font-semibold">ORANGE</span>: Muy urgentes</li>
              <li><span className="text-yellow-600 font-semibold">YELLOW</span>: Urgentes</li>
              <li><span className="text-green-600 font-semibold">GREEN</span>: Menos urgentes</li>
              <li><span className="text-blue-600 font-semibold">BLUE</span>: No urgentes</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-1">IA vs. Criterio Humano</h4>
            <p>Compara las sugerencias de la IA con la decisión final de enfermería:</p>
            <ul className="list-disc list-inside mt-1 text-xs">
              <li>Barras similares = Buena concordancia</li>
              <li>Diferencias grandes = Revisar criterios</li>
              <li>Meta: &gt;90% de concordancia</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-1">Tiempo Promedio Semanal</h4>
            <p>Tiempo desde llegada hasta atención médica:</p>
            <ul className="list-disc list-inside mt-1 text-xs">
              <li>Línea azul: Tiempo real promedio</li>
              <li>Línea roja: Meta de 5 minutos</li>
              <li>Picos = Posibles cuellos de botella</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <UrgenciaBarChart data={dashboardData.volumen_mensual} />
        <ConfianzaBarChart data={dashboardData.comparativa_confianza} />
      </div>
      
      <TiempoAreaChart data={dashboardData.tiempo_promedio_semanal} />
    </div>
  );
};
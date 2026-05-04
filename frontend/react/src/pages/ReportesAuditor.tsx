import { useState, useEffect } from 'react';
import { dashboardService } from '../services/api';
import { FileText, Calendar, BarChart3, AlertTriangle, CheckCircle, Clock, Activity } from 'lucide-react';

interface AnalisisAuditoria {
  periodo: {
    mes: number;
    anio: number;
    nombre_mes: string;
  };
  resumen: {
    total_casos: number;
    tasa_concordancia_ia: number;
    discrepancias: number;
    coincidencias: number;
  };
  distribucion_urgencia: {
    nivel: string;
    cantidad: number;
    porcentaje: number;
  }[];
  tiempos_atencion: {
    nivel: string;
    tiempo_promedio_min: number;
  }[];
  tendencia_diaria: {
    dia: number;
    total: number;
    concordancias: number;
    discrepancias: number;
  }[];
  top_sintomas: {
    sintoma: string;
    frecuencia: number;
  }[];
}

export const ReportesAuditor: React.FC = () => {
  const [analisis, setAnalisis] = useState<AnalisisAuditoria | null>(null);
  const [loading, setLoading] = useState(true);
  const [mes, setMes] = useState(new Date().getMonth() + 1);
  const [anio, setAnio] = useState(new Date().getFullYear());

  useEffect(() => {
    loadAnalisis();
  }, [mes, anio]);

  const loadAnalisis = async () => {
    setLoading(true);
    try {
      const data = await dashboardService.getAnalisisAuditoria(mes, anio);
      setAnalisis(data);
    } catch (error) {
      console.error('Error loading auditor analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  const getNivelColor = (nivel: string) => {
    const colors: Record<string, string> = {
      RED: 'bg-red-100 text-red-800 border-red-200',
      ORANGE: 'bg-orange-100 text-orange-800 border-orange-200',
      YELLOW: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      GREEN: 'bg-green-100 text-green-800 border-green-200',
      BLUE: 'bg-blue-100 text-blue-800 border-blue-200',
    };
    return colors[nivel] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getNivelLabel = (nivel: string) => {
    const labels: Record<string, string> = {
      RED: 'Crítico (RED)',
      ORANGE: 'Muy urgente (ORANGE)',
      YELLOW: 'Urgente (YELLOW)',
      GREEN: 'Menos urgente (GREEN)',
      BLUE: 'No urgente (BLUE)',
    };
    return labels[nivel] || nivel;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Análisis para Auditoría</h1>
          <p className="text-sm text-gray-500 mt-1">
            Datos anonimizados - Sin información personal identificable
          </p>
        </div>
        <div className="flex space-x-4">
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Mes</label>
            <select
              value={mes}
              onChange={(e) => setMes(parseInt(e.target.value))}
              className="px-3 py-2 border rounded-lg text-sm"
            >
              {Array.from({ length: 12 }, (_, i) => (
                <option key={i + 1} value={i + 1}>
                  {new Date(2024, i, 1).toLocaleString('es-ES', { month: 'long' })}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Año</label>
            <select
              value={anio}
              onChange={(e) => setAnio(parseInt(e.target.value))}
              className="px-3 py-2 border rounded-lg text-sm"
            >
              {[2023, 2024, 2025, 2026].map(y => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Warning Banner */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start space-x-3">
        <Activity className="w-5 h-5 text-blue-600 mt-0.5" />
        <div>
          <h3 className="text-sm font-semibold text-blue-800">Reporte Anonimizado</h3>
          <p className="text-xs text-blue-700 mt-1">
            Este reporte no contiene información personal identificable (PII) de pacientes. 
            Solo muestra estadísticas agregadas y tendencias para fines de auditoría de calidad.
          </p>
        </div>
      </div>

      {analisis && (
        <>
          {/* KPIs */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg shadow-md p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Casos</p>
                  <p className="text-2xl font-bold text-gray-800">{analisis.resumen.total_casos.toLocaleString()}</p>
                </div>
                <FileText className="w-8 h-8 text-blue-500" />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-md p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Concordancia IA</p>
                  <p className="text-2xl font-bold text-green-600">{analisis.resumen.tasa_concordancia_ia}%</p>
                </div>
                <CheckCircle className="w-8 h-8 text-green-500" />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-md p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Discrepancias</p>
                  <p className="text-2xl font-bold text-yellow-600">{analisis.resumen.discrepancias.toLocaleString()}</p>
                </div>
                <AlertTriangle className="w-8 h-8 text-yellow-500" />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-md p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Coincidencias</p>
                  <p className="text-2xl font-bold text-blue-600">{analisis.resumen.coincidencias.toLocaleString()}</p>
                </div>
                <BarChart3 className="w-8 h-8 text-blue-500" />
              </div>
            </div>
          </div>

          {/* Distribución por Nivel */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Distribución por Nivel de Urgencia</h2>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {analisis.distribucion_urgencia.map((item) => (
                <div key={item.nivel} className={`p-4 rounded-lg border ${getNivelColor(item.nivel)}`}>
                  <p className="text-xs font-medium">{getNivelLabel(item.nivel)}</p>
                  <p className="text-2xl font-bold mt-1">{item.cantidad}</p>
                  <p className="text-sm">{item.porcentaje}%</p>
                </div>
              ))}
            </div>
          </div>

          {/* Tiempos de Atención */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Clock className="w-5 h-5 mr-2" />
              Tiempos Promedio de Atención
            </h2>
            <div className="space-y-3">
              {analisis.tiempos_atencion.map((item) => (
                <div key={item.nivel} className="flex items-center">
                  <span className={`w-32 px-2 py-1 rounded text-xs font-medium ${getNivelColor(item.nivel)}`}>
                    {item.nivel}
                  </span>
                  <div className="flex-1 mx-4">
                    <div className="bg-gray-200 rounded-full h-4 overflow-hidden">
                      <div
                        className="bg-blue-600 h-full rounded-full"
                        style={{ width: `${Math.min(100, (item.tiempo_promedio_min / 30) * 100)}%` }}
                      ></div>
                    </div>
                  </div>
                  <span className="text-sm font-semibold w-24 text-right">
                    {item.tiempo_promedio_min} min
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Top Síntomas */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Top Síntomas (Frecuencia)</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              {analisis.top_sintomas.map((item, index) => (
                <div key={index} className="bg-gray-50 p-3 rounded-lg">
                  <p className="text-xs text-gray-500">#{index + 1}</p>
                  <p className="text-sm font-medium text-gray-800 truncate">{item.sintoma}</p>
                  <p className="text-lg font-semibold text-blue-600">{item.frecuencia}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Tendencia Diaria */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Tendencia Diaria - Concordancia vs Discrepancias</h2>
            <div className="overflow-x-auto">
              <div className="inline-flex space-x-2 min-w-full">
                {analisis.tendencia_diaria.slice(0, 31).map((dia) => (
                  <div key={dia.dia} className="flex flex-col items-center w-8">
                    <div className="relative w-6 flex flex-col-reverse">
                      <div 
                        className="bg-green-500 w-full"
                        style={{ height: `${dia.concordancias > 0 ? Math.max(4, dia.concordancias * 2) : 0}px` }}
                        title={`Concordancias: ${dia.concordancias}`}
                      ></div>
                      <div 
                        className="bg-yellow-500 w-full"
                        style={{ height: `${dia.discrepancias > 0 ? Math.max(4, dia.discrepancias * 2) : 0}px` }}
                        title={`Discrepancias: ${dia.discrepancias}`}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-500 mt-1">{dia.dia}</span>
                    <span className="text-[10px] text-gray-400">{dia.total}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="flex items-center space-x-4 mt-4 text-sm">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 mr-1"></div>
                <span>Concordancias</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-yellow-500 mr-1"></div>
                <span>Discrepancias</span>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

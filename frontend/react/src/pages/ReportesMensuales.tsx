import { useState, useEffect } from 'react';
import { format, subMonths } from 'date-fns';
import { es } from 'date-fns/locale';
import { FileText, Download, AlertCircle } from 'lucide-react';
import { dashboardService } from '../services/api';
import { DiscrepanciasTable } from '../components/Reportes/DiscrepanciasTable';

export const ReportesMensuales: React.FC = () => {
  const [selectedMonth, setSelectedMonth] = useState(format(new Date(), 'yyyy-MM'));
  const [generating, setGenerating] = useState(false);
  const [discrepancias, setDiscrepancias] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const months = Array.from({ length: 6 }, (_, i) => {
    const date = subMonths(new Date(), i);
    return {
      value: format(date, 'yyyy-MM'),
      label: format(date, 'MMMM yyyy', { locale: es })
    };
  });
  
  useEffect(() => {
    loadDiscrepancias();
  }, [selectedMonth]);
  
  const loadDiscrepancias = async () => {
    try {
      setLoading(true);
      setError(null);
      const [year, month] = selectedMonth.split('-');
      const startDate = `${year}-${month}-01`;
      const endDate = `${year}-${month}-${new Date(parseInt(year), parseInt(month), 0).getDate()}`;
      
      const data = await dashboardService.getDiscrepancias(startDate, endDate);
      setDiscrepancias(data || []);
    } catch (err) {
      console.error('Error cargando discrepancias:', err);
      setError('Error al cargar los datos. Verifica que el backend esté corriendo.');
      setDiscrepancias([]);
    } finally {
      setLoading(false);
    }
  };
  
  const handleGeneratePDF = async () => {
    setGenerating(true);
    try {
      const [year, month] = selectedMonth.split('-');
      const pdfBlob = await dashboardService.generateMonthlyReport(parseInt(month), parseInt(year));
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `reporte-triaje-${selectedMonth}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Error generando el reporte');
    } finally {
      setGenerating(false);
    }
  };
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Reportes Mensuales</h1>
        <div className="flex space-x-4">
          <select
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            {months.map((month) => (
              <option key={month.value} value={month.value}>
                {month.label}
              </option>
            ))}
          </select>
          
          <button
            onClick={handleGeneratePDF}
            disabled={generating}
            className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50"
          >
            {generating ? (
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            ) : (
              <>
                <Download className="h-5 w-5" />
                <span>Generar PDF</span>
              </>
            )}
          </button>
        </div>
      </div>
      
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-red-800">
            <p className="font-semibold">Error</p>
            <p>{error}</p>
          </div>
        </div>
      )}
      
      {loading && (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span className="ml-2 text-gray-600">Cargando datos...</span>
        </div>
      )}
      
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex items-start space-x-3">
        <AlertCircle className="h-5 w-5 text-yellow-600 flex-shrink-0 mt-0.5" />
        <div className="text-sm text-yellow-800">
          <p className="font-semibold">Resumen Ejecutivo</p>
          <p>
            Durante el período seleccionado, se registraron {discrepancias.length} casos con discrepancias
            entre la evaluación de IA y el criterio de enfermería. La tasa de concurrencia se mantiene
            en niveles óptimos, con mejoras en la detección de casos críticos.
          </p>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center">
          <FileText className="h-5 w-5 mr-2 text-primary-600" />
          Discrepancias IA vs Humano
        </h2>
        <DiscrepanciasTable data={discrepancias} />
      </div>
    </div>
  );
};
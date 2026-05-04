import { useState } from 'react';
import { Download, Loader2 } from 'lucide-react';
import { dashboardService } from '../../services/api';

interface ReportGeneratorProps {
  month: string;
  onGenerate?: () => void;
}

export const ReportGenerator: React.FC<ReportGeneratorProps> = ({ month, onGenerate }) => {
  const [generating, setGenerating] = useState(false);
  
  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const pdfBlob = await dashboardService.generateMonthlyReport(month);
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `reporte-triaje-${month}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      onGenerate?.();
    } catch (error) {
      console.error('Error generando PDF:', error);
      alert('Error al generar el reporte');
    } finally {
      setGenerating(false);
    }
  };
  
  return (
    <button
      onClick={handleGenerate}
      disabled={generating}
      className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
    >
      {generating ? (
        <Loader2 className="h-4 w-4 animate-spin" />
      ) : (
        <Download className="h-4 w-4" />
      )}
      <span>{generating ? 'Generando...' : 'Exportar PDF'}</span>
    </button>
  );
};
import { useState } from 'react';
import { AuditLog } from '../../types';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface AuditLogTableProps {
  data: AuditLog[];
  page?: number;
  totalPages?: number;
  onPageChange?: (page: number) => void;
  pageSize?: number;
}

export const AuditLogTable: React.FC<AuditLogTableProps> = ({ 
  data, 
  page = 1, 
  totalPages = 1, 
  onPageChange,
  pageSize = 10
}) => {
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set());

  const toggleRow = (id: number) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedRows(newExpanded);
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString('es-CL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getActionColor = (accion: string) => {
    const colors: Record<string, string> = {
      INSERT: 'bg-green-100 text-green-800',
      UPDATE: 'bg-blue-100 text-blue-800',
      DELETE: 'bg-red-100 text-red-800',
      STATUS_CHANGE: 'bg-yellow-100 text-yellow-800',
    };
    return colors[accion] || 'bg-gray-100 text-gray-800';
  };

  const formatJsonData = (data: any) => {
    if (!data) return null;
    if (typeof data === 'string') return data;
    try {
      return JSON.stringify(data, null, 2);
    } catch {
      return String(data);
    }
  };

  return (
    <div className="space-y-4">
      <div className="overflow-x-auto border rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-2 py-3 w-8"></th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Fecha/Hora
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Usuario
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acción
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Módulo
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                ID Registro
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                  No hay registros de auditoría
                </td>
              </tr>
            ) : (
              data.map((log) => (
                <>
                  <tr 
                    key={log.id} 
                    className="hover:bg-gray-50 cursor-pointer"
                    onClick={() => toggleRow(log.id)}
                  >
                    <td className="px-2 py-4">
                      {expandedRows.has(log.id) ? (
                        <ChevronUp className="w-4 h-4 text-gray-500" />
                      ) : (
                        <ChevronDown className="w-4 h-4 text-gray-500" />
                      )}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(log.timestamp)}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                      {log.usuario_nombre || 'Sistema'}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getActionColor(log.accion)}`}>
                        {log.accion}
                      </span>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                      {log.modulo}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                      {log.registro_id}
                    </td>
                  </tr>
                  {expandedRows.has(log.id) && (
                    <tr className="bg-gray-50">
                      <td colSpan={6} className="px-6 py-4">
                        <div className="space-y-3">
                          {log.datos_anteriores && (
                            <div>
                              <span className="text-xs font-semibold text-gray-500 uppercase">Datos Anteriores:</span>
                              <pre className="mt-1 p-2 bg-white rounded border text-xs overflow-x-auto">
                                {formatJsonData(log.datos_anteriores)}
                              </pre>
                            </div>
                          )}
                          {log.datos_nuevos && (
                            <div>
                              <span className="text-xs font-semibold text-gray-500 uppercase">Datos Nuevos:</span>
                              <pre className="mt-1 p-2 bg-white rounded border text-xs overflow-x-auto">
                                {formatJsonData(log.datos_nuevos)}
                              </pre>
                            </div>
                          )}
                          {log.ip_address && (
                            <div className="text-sm">
                              <span className="text-xs font-semibold text-gray-500 uppercase">IP:</span>{' '}
                              <span className="text-gray-700">{log.ip_address}</span>
                            </div>
                          )}
                          {log.user_agent && (
                            <div className="text-sm">
                              <span className="text-xs font-semibold text-gray-500 uppercase">User Agent:</span>{' '}
                              <span className="text-gray-700 text-xs">{log.user_agent}</span>
                            </div>
                          )}
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && onPageChange && (
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-500">
            Mostrando página {page} de {totalPages}
          </div>
          <div className="flex space-x-1">
            <button
              onClick={() => onPageChange(Math.max(1, page - 1))}
              disabled={page === 1}
              className="px-3 py-1 border rounded text-sm disabled:opacity-50 hover:bg-gray-50"
            >
              ← Anterior
            </button>
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              const pageNum = i + 1;
              return (
                <button
                  key={pageNum}
                  onClick={() => onPageChange(pageNum)}
                  className={`px-3 py-1 border rounded text-sm ${
                    page === pageNum 
                      ? 'bg-blue-600 text-white' 
                      : 'hover:bg-gray-50'
                  }`}
                >
                  {pageNum}
                </button>
              );
            })}
            <button
              onClick={() => onPageChange(Math.min(totalPages, page + 1))}
              disabled={page === totalPages}
              className="px-3 py-1 border rounded text-sm disabled:opacity-50 hover:bg-gray-50"
            >
              Siguiente →
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
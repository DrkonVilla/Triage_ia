import { useState, useEffect } from 'react';
import { AuditLogTable } from '../components/Auditoria/AuditLogTable';
import { auditoriaService } from '../services/api';
import { AuditLog, AuditStats } from '../types';
import { Search, Filter, Calendar, User, BarChart3 } from 'lucide-react';

export const Auditoria: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [modulo, setModulo] = useState('');
  const [usuarioId, setUsuarioId] = useState('');
  const [desde, setDesde] = useState('');
  const [hasta, setHasta] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [stats, setStats] = useState<AuditStats | null>(null);
  const [showStats, setShowStats] = useState(false);
  const pageSize = 10;
  
  useEffect(() => {
    loadLogs();
    loadStats();
  }, [modulo, usuarioId, desde, hasta, page]);
  
  const loadLogs = async () => {
    setLoading(true);
    try {
      const data = await auditoriaService.getLogs({ 
        modulo: modulo || undefined, 
        usuario_id: usuarioId ? parseInt(usuarioId) : undefined,
        desde: desde || undefined,
        hasta: hasta || undefined,
        limit: pageSize,
        offset: (page - 1) * pageSize
      });
      setLogs(data);
      // Estimar total de páginas (asumiendo que hay más si devuelve pageSize)
      setTotalPages(Math.max(1, Math.ceil(data.length / pageSize) + (data.length === pageSize ? 1 : 0)));
    } catch (error) {
      console.error('Error loading logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const data = await auditoriaService.getStats();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };
  
  const applyFilters = () => {
    setPage(1);
    loadLogs();
  };

  const formatDateForInput = (dateStr: string) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toISOString().split('T')[0];
  };
  
  if (loading && logs.length === 0) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Auditoría del Sistema</h1>
        <button
          onClick={() => setShowStats(!showStats)}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <BarChart3 className="w-4 h-4" />
          <span>{showStats ? 'Ocultar Stats' : 'Ver Stats'}</span>
        </button>
      </div>

      {/* Stats Panel */}
      {showStats && stats && (
        <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
          <h2 className="text-lg font-semibold text-gray-800">📊 Estadísticas de Auditoría</h2>
          
          {/* KPIs */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{stats.total_registros.toLocaleString()}</div>
              <div className="text-sm text-blue-800">Total de registros</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{stats.registros_ultima_semana.toLocaleString()}</div>
              <div className="text-sm text-green-800">Registros última semana</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{stats.acciones_por_modulo?.length || 0}</div>
              <div className="text-sm text-purple-800">Módulos activos</div>
            </div>
          </div>

          {/* Acciones por módulo */}
          {stats.acciones_por_modulo && stats.acciones_por_modulo.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Acciones por módulo:</h3>
              <div className="space-y-2">
                {stats.acciones_por_modulo.map((item) => (
                  <div key={item.modulo} className="flex items-center">
                    <div className="w-32 text-sm text-gray-600">{item.modulo}</div>
                    <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                      <div 
                        className="bg-blue-600 h-full rounded-full"
                        style={{ width: `${item.porcentaje}%` }}
                      ></div>
                    </div>
                    <div className="w-24 text-right text-sm text-gray-600">
                      {item.total} ({item.porcentaje}%)
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Top usuarios */}
          {stats.top_usuarios && stats.top_usuarios.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Top usuarios más activos:</h3>
              <div className="space-y-1">
                {stats.top_usuarios.slice(0, 5).map((usuario, index) => (
                  <div key={index} className="flex items-center justify-between py-1">
                    <div className="flex items-center space-x-2">
                      <span className="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center text-xs font-semibold">
                        {index + 1}
                      </span>
                      <span className="text-sm">{usuario.usuario}</span>
                      <span className="text-xs text-gray-500">({usuario.rol})</span>
                    </div>
                    <span className="text-sm font-semibold text-blue-600">{usuario.total} acciones</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
      
      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Módulo */}
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">
              <Filter className="w-3 h-3 inline mr-1" />
              Módulo
            </label>
            <select
              value={modulo}
              onChange={(e) => setModulo(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg text-sm"
            >
              <option value="">Todos los módulos</option>
              <option value="triaje">Triaje</option>
              <option value="estado_logistico">Estado Logístico</option>
              <option value="paciente">Paciente</option>
              <option value="notas_medicas">Notas Médicas</option>
            </select>
          </div>

          {/* Usuario */}
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">
              <User className="w-3 h-3 inline mr-1" />
              ID Usuario
            </label>
            <input
              type="number"
              value={usuarioId}
              onChange={(e) => setUsuarioId(e.target.value)}
              placeholder="Filtrar por usuario..."
              className="w-full px-3 py-2 border rounded-lg text-sm"
            />
          </div>

          {/* Fecha Desde */}
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">
              <Calendar className="w-3 h-3 inline mr-1" />
              Desde
            </label>
            <input
              type="date"
              value={desde}
              onChange={(e) => setDesde(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg text-sm"
            />
          </div>

          {/* Fecha Hasta */}
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">
              <Calendar className="w-3 h-3 inline mr-1" />
              Hasta
            </label>
            <input
              type="date"
              value={hasta}
              onChange={(e) => setHasta(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg text-sm"
            />
          </div>
        </div>

        <div className="mt-4 flex justify-end">
          <button
            onClick={applyFilters}
            className="flex items-center space-x-2 px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700"
          >
            <Search className="w-4 h-4" />
            <span>Aplicar Filtros</span>
          </button>
        </div>
      </div>
      
      {/* Table */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-4 text-sm text-gray-500">
          Mostrando {logs.length} registros (página {page})
        </div>
        <AuditLogTable 
          data={logs} 
          page={page}
          totalPages={totalPages}
          onPageChange={setPage}
        />
      </div>
    </div>
  );
};
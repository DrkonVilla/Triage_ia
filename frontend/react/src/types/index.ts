export interface Usuario {
  id: number;
  username: string;
  email: string;
  nombres: string;
  apellidos: string;
  rol: string;
}

export interface TriajeStats {
  id: number;
  fecha_hora: string;
  nivel_urgencia_asignado_ia: string;
  nivel_urgencia_final: string;
  estado_logistico: string;
  tiempo_atencion_segundos: number;
  paciente_nombre: string;
}

export interface DashboardData {
  volumen_mensual: {
    mes: string;
    RED: number;
    ORANGE: number;
    YELLOW: number;
    GREEN: number;
    BLUE: number;
  }[];
  comparativa_confianza: {
    nivel: string;
    ia: number;
    humano: number;
  }[];
  tiempo_promedio_semanal: {
    semana: string;
    promedio: number;
    meta: number;
  }[];
  kpis: {
    total_triajes: number;
    promedio_tiempo: number;
    tasa_concurrencia_ia: number;
    criticos_atendidos: number;
  };
}

export interface Discrepancia {
  id: number;
  fecha: string;
  paciente: string;
  nivel_ia: string;
  nivel_humano: string;
  diferencia: string;
  motivo?: string;
}

export interface AuditLog {
  id: number;
  usuario_nombre: string;
  accion: string;
  modulo: string;
  registro_id: number;
  datos_anteriores: any;
  datos_nuevos: any;
  ip_address?: string;
  user_agent?: string;
  timestamp: string;
}

export interface AuditStats {
  total_registros: number;
  registros_ultima_semana: number;
  acciones_por_modulo: { modulo: string; total: number; porcentaje: number }[];
  top_usuarios: { usuario: string; rol: string; total: number }[];
}
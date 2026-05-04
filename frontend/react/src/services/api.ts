import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: number;
    username: string;
    email: string;
    nombres: string;
    apellidos: string;
    rol: string;
  };
}

export const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', credentials);
    const data = response.data as any;

    // Backend usa alias_generator=to_camel => accessToken/tokenType/expiresIn
    const accessToken = data?.access_token ?? data?.accessToken;
    const tokenType = data?.token_type ?? data?.tokenType ?? 'bearer';
    const expiresIn = data?.expires_in ?? data?.expiresIn;

    return {
      access_token: accessToken,
      token_type: tokenType,
      expires_in: expiresIn,
      user: data?.user,
    } as AuthResponse;
  },
  
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
};

export const dashboardService = {
  getDashboardData: async (startDate: string, endDate: string): Promise<DashboardData> => {
    const response = await api.get('/reportes/dashboard', {
      params: { start_date: startDate, end_date: endDate }
    });
    return response.data;
  },
  
  getDiscrepancias: async (startDate: string, endDate: string): Promise<Discrepancia[]> => {
    const response = await api.get('/reportes/discrepancias', {
      params: { start_date: startDate, end_date: endDate }
    });
    return response.data;
  },
  
  generateMonthlyReport: async (mes: number, anio: number): Promise<Blob> => {
    const response = await api.get('/reportes/monthly-pdf', {
      params: { mes, anio },
      responseType: 'blob'
    });
    return response.data;
  },

  getAnalisisAuditoria: async (mes: number, anio: number) => {
    const response = await api.get('/reportes/analisis-auditoria', {
      params: { mes, anio }
    });
    return response.data;
  }
};

export const auditoriaService = {
  getLogs: async (params: {
    modulo?: string;
    usuario_id?: number;
    desde?: string;
    hasta?: string;
    limit?: number;
    offset?: number;
  }): Promise<AuditLog[]> => {
    const response = await api.get('/auditoria/logs', { params });
    return response.data;
  },
  
  getStats: async () => {
    const response = await api.get('/auditoria/stats');
    return response.data;
  }
};

export default api;
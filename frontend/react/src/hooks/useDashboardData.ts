import { useState, useEffect } from 'react';
import { dashboardService } from '../services/api';
import { DashboardData } from '../types';

export const useDashboardData = (startDate: string, endDate: string) => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await dashboardService.getDashboardData(startDate, endDate);
        setData(result);
      } catch (err) {
        setError('Error cargando datos del dashboard');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, [startDate, endDate]);
  
  return { data, loading, error };
};
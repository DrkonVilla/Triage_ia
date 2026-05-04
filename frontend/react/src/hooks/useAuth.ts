import { useEffect, useState } from 'react';
import { isAuthenticated, getUserRole, getUserName } from '../services/auth';

export const useAuth = () => {
  const [authenticated, setAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState<string | null>(null);
  const [userName, setUserName] = useState<string | null>(null);
  
  useEffect(() => {
    setAuthenticated(isAuthenticated());
    setUserRole(getUserRole());
    setUserName(getUserName());
  }, []);
  
  return { authenticated, userRole, userName };
};
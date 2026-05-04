import { Navigate } from 'react-router-dom';
import { isAuthenticated, getUserRole } from '../../services/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: string[];
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  allowedRoles 
}) => {
  const authenticated = isAuthenticated();
  const userRole = getUserRole();
  
  if (!authenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (allowedRoles && userRole && !allowedRoles.includes(userRole)) {
    return <Navigate to="/unauthorized" replace />;
  }
  
  return <>{children}</>;
};
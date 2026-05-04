import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  Shield, 
  LogOut,
  Activity 
} from 'lucide-react';

interface NavItem {
  path: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  roles?: string[];
}

const allNavItems: NavItem[] = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, roles: ['admin', 'gerente', 'medico', 'enfermera'] },
  { path: '/reportes', label: 'Reportes Mensuales', icon: FileText, roles: ['admin', 'gerente'] },
  { path: '/auditoria', label: 'Auditoría', icon: Shield },
  { path: '/reportes-auditor', label: 'Análisis Auditoría', icon: FileText, roles: ['auditor'] },
];

export const Sidebar: React.FC = () => {
  // Get user from localStorage
  const userStr = localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : null;
  const userRole = user?.rol || '';

  // Filter nav items based on role
  const navItems = allNavItems.filter(item => {
    if (!item.roles) return true; // Items without roles restriction are visible to all
    return item.roles.includes(userRole);
  });

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };
  
  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen flex flex-col">
      <div className="p-6 border-b border-gray-800">
        <div className="flex items-center space-x-2">
          <Activity className="h-8 w-8 text-primary-500" />
          <span className="text-xl font-bold">Triaje IA</span>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          {user ? `${user.nombres || user.username} (${user.rol})` : 'Gestión Administrativa'}
        </p>
      </div>
      
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800'
              }`
            }
          >
            <item.icon className="h-5 w-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      
      <div className="p-4 border-t border-gray-800">
        <button
          onClick={handleLogout}
          className="flex items-center space-x-3 px-4 py-3 w-full rounded-lg text-gray-300 hover:bg-gray-800 transition-colors"
        >
          <LogOut className="h-5 w-5" />
          <span>Cerrar Sesión</span>
        </button>
      </div>
    </aside>
  );
};
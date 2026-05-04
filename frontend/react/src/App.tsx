import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Sidebar } from './components/Layout/Sidebar';
import { ProtectedRoute } from './components/Layout/ProtectedRoute';
import { Login } from './pages/Login';
import { DashboardGestion } from './pages/DashboardGestion';
import { ReportesMensuales } from './pages/ReportesMensuales';
import { ReportesAuditor } from './pages/ReportesAuditor';
import { Auditoria } from './pages/Auditoria';
import { getUserRole } from './services/auth';

const AppLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const userRole = getUserRole();
  
  // Solo gerentes y auditores pueden acceder a esta app
  if (userRole !== 'gerente' && userRole !== 'auditor') {
    return <Navigate to="/unauthorized" replace />;
  }
  
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute allowedRoles={['gerente', 'auditor']}>
              <AppLayout>
                <DashboardGestion />
              </AppLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/reportes"
          element={
            <ProtectedRoute allowedRoles={['gerente']}>
              <AppLayout>
                <ReportesMensuales />
              </AppLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/auditoria"
          element={
            <ProtectedRoute allowedRoles={['gerente', 'auditor']}>
              <AppLayout>
                <Auditoria />
              </AppLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/reportes-auditor"
          element={
            <ProtectedRoute allowedRoles={['auditor']}>
              <AppLayout>
                <ReportesAuditor />
              </AppLayout>
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to={getUserRole() === 'auditor' ? '/auditoria' : '/dashboard'} replace />} />
        <Route
          path="/unauthorized"
          element={
            <div className="flex items-center justify-center h-screen">
              <div className="text-center">
                <h1 className="text-2xl font-bold text-red-600 mb-2">Acceso no autorizado</h1>
                <p className="text-gray-600">No tiene permisos para acceder a esta sección</p>
              </div>
            </div>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ roles }) {
  const { user, loading, hasRole } = useAuth();
  if (loading) return <div className="screen-loader">Loading secure workspace...</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (roles?.length && !hasRole(roles)) return <Navigate to="/" replace />;
  return <Outlet />;
}

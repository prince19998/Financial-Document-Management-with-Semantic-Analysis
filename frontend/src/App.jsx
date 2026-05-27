import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import ProtectedRoute from './routes/ProtectedRoute';
import Analytics from './pages/Analytics';
import Dashboard from './pages/Dashboard';
import DocumentDetails from './pages/DocumentDetails';
import Documents from './pages/Documents';
import Login from './pages/Login';
import Register from './pages/Register';
import Roles from './pages/Roles';
import SemanticSearch from './pages/SemanticSearch';
import UploadDocument from './pages/UploadDocument';
import Users from './pages/Users';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/documents/:id" element={<DocumentDetails />} />
            <Route path="/semantic-search" element={<SemanticSearch />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route element={<ProtectedRoute roles={['Admin', 'Financial Analyst']} />}>
              <Route path="/upload" element={<UploadDocument />} />
            </Route>
            <Route element={<ProtectedRoute roles={['Admin']} />}>
              <Route path="/users" element={<Users />} />
              <Route path="/roles" element={<Roles />} />
            </Route>
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

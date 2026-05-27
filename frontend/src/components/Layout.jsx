import { Link, NavLink, Outlet } from 'react-router-dom';
import { BarChart3, FileSearch, Files, LayoutDashboard, LogOut, Moon, Shield, Upload, Users } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';

const links = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/upload', label: 'Upload', icon: Upload, roles: ['Admin', 'Financial Analyst'] },
  { to: '/documents', label: 'Documents', icon: Files },
  { to: '/semantic-search', label: 'Semantic Search', icon: FileSearch },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/users', label: 'Users', icon: Users, roles: ['Admin'] },
  { to: '/roles', label: 'Roles', icon: Shield, roles: ['Admin'] },
];

export default function Layout() {
  const { user, logout, hasRole } = useAuth();
  const [dark, setDark] = useState(false);

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  }, [dark]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link className="brand" to="/">FinDoc AI</Link>
        <nav className="nav flex-column gap-1">
          {links.filter((link) => !link.roles || hasRole(link.roles)).map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <Icon size={18} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="workspace">
        <header className="topbar">
          <div>
            <strong>{user?.full_name}</strong>
            <span>{user?.roles?.join(', ')}</span>
          </div>
          <div className="d-flex align-items-center gap-2">
            <button className="icon-btn" title="Toggle theme" onClick={() => setDark((value) => !value)}><Moon size={18} /></button>
            <button className="btn btn-outline-danger btn-sm d-inline-flex align-items-center gap-2" onClick={logout}><LogOut size={16} /> Logout</button>
          </div>
        </header>
        <section className="content">
          <Outlet />
        </section>
      </main>
    </div>
  );
}

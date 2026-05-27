import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: 'admin@example.com', password: 'Admin@123' });
  const [error, setError] = useState('');

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      await login(form.email, form.password);
      navigate('/');
    } catch {
      setError('Invalid credentials');
    }
  };

  return (
    <main className="auth-screen">
      <form className="auth-panel" onSubmit={submit}>
        <h1>FinDoc AI</h1>
        <p>Secure financial document intelligence workspace.</p>
        {error && <div className="alert alert-danger py-2">{error}</div>}
        <input className="form-control" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <input className="form-control" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <button className="btn btn-primary w-100">Login</button>
        <Link to="/register">Create an account</Link>
      </form>
    </main>
  );
}

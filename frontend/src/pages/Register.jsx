import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: '', email: '', password: '' });

  const submit = async (event) => {
    event.preventDefault();
    await register(form);
    navigate('/');
  };

  return (
    <main className="auth-screen">
      <form className="auth-panel" onSubmit={submit}>
        <h1>Create Account</h1>
        <input className="form-control" placeholder="Full name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
        <input className="form-control" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <input className="form-control" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <button className="btn btn-primary w-100">Register</button>
        <Link to="/login">Back to login</Link>
      </form>
    </main>
  );
}

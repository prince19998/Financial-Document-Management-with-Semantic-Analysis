import { useEffect, useState } from 'react';
import api from '../services/api';

const permissionOptions = ['admin:*', 'documents:upload', 'documents:edit', 'documents:view', 'documents:delete', 'documents:review', 'rag:search', 'users:manage'];

export default function Roles() {
  const [roles, setRoles] = useState([]);
  const [form, setForm] = useState({ name: '', description: '', permissions: [] });

  const load = async () => setRoles((await api.get('/roles')).data);
  useEffect(() => { load(); }, []);

  const togglePermission = (permission) => {
    setForm((current) => ({
      ...current,
      permissions: current.permissions.includes(permission)
        ? current.permissions.filter((item) => item !== permission)
        : [...current.permissions, permission],
    }));
  };

  const create = async (event) => {
    event.preventDefault();
    await api.post('/roles/create', form);
    setForm({ name: '', description: '', permissions: [] });
    await load();
  };

  return (
    <>
      <div className="page-heading"><h2>Role Management</h2><p>Create permission bundles for finance, audit, client, and admin teams.</p></div>
      <form className="data-panel" onSubmit={create}>
        <div className="row g-3">
          <div className="col-md-6"><input className="form-control" placeholder="Role name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
          <div className="col-md-6"><input className="form-control" placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
        </div>
        <div className="permission-grid">
          {permissionOptions.map((permission) => (
            <label key={permission} className="form-check">
              <input className="form-check-input" type="checkbox" checked={form.permissions.includes(permission)} onChange={() => togglePermission(permission)} />
              <span>{permission}</span>
            </label>
          ))}
        </div>
        <button className="btn btn-primary">Create Role</button>
      </form>
      <div className="data-panel mt-3">
        <table className="table"><tbody>{roles.map((role) => <tr key={role.id}><td>{role.name}</td><td>{role.permissions.join(', ')}</td></tr>)}</tbody></table>
      </div>
    </>
  );
}

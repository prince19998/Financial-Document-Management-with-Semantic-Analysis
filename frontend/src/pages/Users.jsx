import { useEffect, useState } from 'react';
import api from '../services/api';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [assignment, setAssignment] = useState({ user_id: '', role_name: 'Client' });

  const load = async () => {
    const [usersRes, rolesRes] = await Promise.all([api.get('/users'), api.get('/roles')]);
    setUsers(usersRes.data);
    setRoles(rolesRes.data);
  };

  useEffect(() => { load(); }, []);

  const assign = async (event) => {
    event.preventDefault();
    await api.post('/users/assign-role', { ...assignment, user_id: Number(assignment.user_id) });
    await load();
  };

  return (
    <>
      <div className="page-heading"><h2>User Management</h2><p>Assign access according to organizational responsibility.</p></div>
      <form className="data-panel compact-form" onSubmit={assign}>
        <select className="form-select" value={assignment.user_id} onChange={(e) => setAssignment({ ...assignment, user_id: e.target.value })} required>
          <option value="">Select user</option>
          {users.map((user) => <option value={user.id} key={user.id}>{user.full_name} ({user.email})</option>)}
        </select>
        <select className="form-select" value={assignment.role_name} onChange={(e) => setAssignment({ ...assignment, role_name: e.target.value })}>
          {roles.map((role) => <option key={role.id}>{role.name}</option>)}
        </select>
        <button className="btn btn-primary">Assign Role</button>
      </form>
      <div className="data-panel mt-3">
        <table className="table"><tbody>{users.map((user) => <tr key={user.id}><td>{user.full_name}</td><td>{user.email}</td><td>{user.roles.join(', ')}</td></tr>)}</tbody></table>
      </div>
    </>
  );
}

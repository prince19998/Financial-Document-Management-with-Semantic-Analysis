import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [q, setQ] = useState('');

  const load = async () => {
    const { data } = await api.get(q ? `/documents/search?q=${encodeURIComponent(q)}` : '/documents');
    setDocuments(data);
  };

  useEffect(() => { load(); }, []);

  return (
    <>
      <div className="page-heading"><h2>Document Management</h2><p>Browse and inspect uploaded financial records.</p></div>
      <div className="data-panel">
        <div className="d-flex gap-2 mb-3">
          <input className="form-control" placeholder="Filter by title, company, or type" value={q} onChange={(e) => setQ(e.target.value)} />
          <button className="btn btn-outline-primary" onClick={load}>Search</button>
        </div>
        <div className="table-responsive">
          <table className="table align-middle">
            <thead><tr><th>Title</th><th>Company</th><th>Type</th><th>Uploaded</th><th></th></tr></thead>
            <tbody>
              {documents.map((doc) => (
                <tr key={doc.id}>
                  <td>{doc.title}</td><td>{doc.company_name}</td><td>{doc.document_type}</td>
                  <td>{new Date(doc.created_at).toLocaleDateString()}</td>
                  <td><Link className="btn btn-sm btn-outline-secondary" to={`/documents/${doc.id}`}>Details</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

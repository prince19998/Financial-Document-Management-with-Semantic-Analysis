import { useEffect, useState } from 'react';
import api from '../services/api';
import StatCard from '../components/StatCard';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  useEffect(() => {
    api.get('/analytics/summary').then(({ data }) => setSummary(data));
  }, []);

  return (
    <>
      <div className="page-heading">
        <h2>Dashboard</h2>
        <p>Operational overview for document intake, retrieval, and audit activity.</p>
      </div>
      <div className="stat-grid">
        <StatCard label="Total Documents" value={summary?.total_documents ?? 0} tone="primary" />
        <StatCard label="Uploaded Files" value={summary?.uploaded_files ?? 0} tone="green" />
        <StatCard label="Active Users" value={summary?.active_users ?? 0} tone="amber" />
        <StatCard label="Searches" value={summary?.searches ?? 0} tone="rose" />
      </div>
      <div className="data-panel mt-4">
        <h3>Recent Search Activity</h3>
        <div className="table-responsive">
          <table className="table align-middle">
            <tbody>
              {(summary?.recent_searches ?? []).map((item, index) => (
                <tr key={`${item.query}-${index}`}>
                  <td>{item.query}</td>
                  <td>{item.results_count} results</td>
                  <td>{new Date(item.created_at).toLocaleString()}</td>
                </tr>
              ))}
              {!summary?.recent_searches?.length && <tr><td>No searches yet.</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

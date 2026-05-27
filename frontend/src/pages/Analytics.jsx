import { ArcElement, BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Tooltip } from 'chart.js';
import { useEffect, useState } from 'react';
import { Bar, Doughnut } from 'react-chartjs-2';
import api from '../services/api';

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function Analytics() {
  const [summary, setSummary] = useState(null);
  useEffect(() => { api.get('/analytics/summary').then(({ data }) => setSummary(data)); }, []);
  const labels = summary?.document_types?.map((item) => item.name) ?? [];
  const counts = summary?.document_types?.map((item) => item.count) ?? [];

  return (
    <>
      <div className="page-heading"><h2>Analytics</h2><p>Document mix and search activity signals.</p></div>
      <div className="analytics-grid">
        <div className="data-panel"><h3>Document Types</h3><Doughnut data={{ labels, datasets: [{ data: counts, backgroundColor: ['#2563eb', '#16a34a', '#f59e0b', '#dc2626', '#7c3aed'] }] }} /></div>
        <div className="data-panel"><h3>Volume</h3><Bar data={{ labels, datasets: [{ label: 'Documents', data: counts, backgroundColor: '#2563eb' }] }} /></div>
      </div>
    </>
  );
}

import { useState } from 'react';
import api from '../services/api';
import Toast from '../components/Toast';

export default function UploadDocument() {
  const [file, setFile] = useState(null);
  const [form, setForm] = useState({ title: '', company_name: '', document_type: 'Invoice' });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (event) => {
    event.preventDefault();
    setLoading(true);
    const payload = new FormData();
    Object.entries(form).forEach(([key, value]) => payload.append(key, value));
    payload.append('file', file);
    try {
      await api.post('/documents/upload', payload);
      setMessage('Document uploaded, extracted, chunked, embedded, and indexed.');
      setForm({ title: '', company_name: '', document_type: 'Invoice' });
      setFile(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Toast message={message} />
      <div className="page-heading"><h2>Upload Document</h2><p>PDF, DOCX, TXT, and CSV files are validated before indexing.</p></div>
      <form className="data-panel upload-form" onSubmit={submit}>
        <div className="row g-3">
          <div className="col-md-4"><input required className="form-control" placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
          <div className="col-md-4"><input required className="form-control" placeholder="Company name" value={form.company_name} onChange={(e) => setForm({ ...form, company_name: e.target.value })} /></div>
          <div className="col-md-4">
            <select className="form-select" value={form.document_type} onChange={(e) => setForm({ ...form, document_type: e.target.value })}>
              {['Invoice', 'Financial Report', 'Contract', 'Agreement', 'Statement'].map((type) => <option key={type}>{type}</option>)}
            </select>
          </div>
        </div>
        <label className="drop-zone mt-3">
          <input required type="file" accept=".pdf,.docx,.txt,.csv" onChange={(e) => setFile(e.target.files[0])} />
          <strong>{file ? file.name : 'Drop or select a financial document'}</strong>
          <span>Text extraction and semantic indexing start after upload.</span>
        </label>
        <button disabled={loading || !file} className="btn btn-primary">{loading ? 'Indexing...' : 'Upload and Index'}</button>
      </form>
    </>
  );
}

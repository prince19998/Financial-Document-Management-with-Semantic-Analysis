import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';

export default function DocumentDetails() {
  const { id } = useParams();
  const [document, setDocument] = useState(null);
  useEffect(() => { api.get(`/documents/${id}`).then(({ data }) => setDocument(data)); }, [id]);
  if (!document) return <div className="screen-loader">Loading document...</div>;
  return (
    <>
      <div className="page-heading"><h2>{document.title}</h2><p>{document.company_name} · {document.document_type}</p></div>
      <div className="data-panel">
        <dl className="row">
          <dt className="col-sm-3">Filename</dt><dd className="col-sm-9">{document.filename}</dd>
          <dt className="col-sm-3">Uploaded</dt><dd className="col-sm-9">{new Date(document.created_at).toLocaleString()}</dd>
        </dl>
        <pre className="preview-box">{document.content_preview}</pre>
      </div>
    </>
  );
}

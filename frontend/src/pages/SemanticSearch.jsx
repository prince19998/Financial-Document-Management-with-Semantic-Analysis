import { useState } from 'react';
import api from '../services/api';

export default function SemanticSearch() {
  const [query, setQuery] = useState('financial risk related to high debt ratio');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const search = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const { data } = await api.post('/rag/search', { query, top_k: 5 });
      setResponse(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="page-heading"><h2>Semantic Search</h2><p>Retrieve financial evidence by meaning, then rerank the strongest passages.</p></div>
      <form className="search-bar" onSubmit={search}>
        <input className="form-control" value={query} onChange={(e) => setQuery(e.target.value)} />
        <button className="btn btn-primary">{loading ? 'Searching...' : 'Search'}</button>
      </form>
      {response && (
        <div className="results-stack">
          <div className="insight-box">{response.insights}</div>
          {response.results.map((result, index) => (
            <article className="result-card" key={`${result.document_id}-${index}`}>
              <div><strong>{result.title}</strong><span>{result.company_name} · {result.document_type}</span></div>
              <p>{result.chunk}</p>
              <small>Relevance score: {result.score.toFixed(3)}</small>
            </article>
          ))}
        </div>
      )}
    </>
  );
}

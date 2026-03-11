import { useEffect, useState } from 'react';
import api from '../api';

export default function Articles() {
  const [articles, setArticles] = useState([]);
  const [source, setSource] = useState('');
  const [topic, setTopic] = useState('');
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [sources, setSources] = useState([]);
  const [topics, setTopics] = useState([]);

  const fetchArticles = () => {
    const params = { page, limit: 30 };
    if (source) params.source = source;
    if (topic) params.topic = topic;
    if (search) params.search = search;
    api.get('/articles', { params }).then((r) => setArticles(r.data));
  };

  useEffect(() => {
    api.get('/sites').then((r) => setSources(r.data));
    api.get('/topics').then((r) => setTopics(r.data));
  }, []);

  useEffect(() => { fetchArticles(); }, [page, source, topic]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchArticles();
  };

  return (
    <div className="page">
      <div className="page-header">
        <h2>Articles</h2>
      </div>

      <div className="card filters-bar">
        <form onSubmit={handleSearch} className="filter-row">
          <select value={source} onChange={(e) => { setSource(e.target.value); setPage(1); }}>
            <option value="">All Sources</option>
            {sources.map((s) => <option key={s.id} value={s.name}>{s.name}</option>)}
          </select>
          <select value={topic} onChange={(e) => { setTopic(e.target.value); setPage(1); }}>
            <option value="">All Topics</option>
            {topics.map((t) => <option key={t.id} value={t.name}>{t.name}</option>)}
            <option value="General">General</option>
          </select>
          <input
            type="text"
            placeholder="Search headlines…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button type="submit" className="btn btn-primary">Search</button>
        </form>
      </div>

      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Source</th>
                <th>Topic</th>
                <th>Date</th>
                <th>Sent</th>
              </tr>
            </thead>
            <tbody>
              {articles.map((a) => (
                <tr key={a.id}>
                  <td>
                    <a href={a.url} target="_blank" rel="noreferrer">{a.title}</a>
                  </td>
                  <td>{a.source}</td>
                  <td><span className="badge">{a.topic}</span></td>
                  <td>{a.date_scraped ? new Date(a.date_scraped).toLocaleDateString() : '—'}</td>
                  <td>{a.sent_status ? '✅' : '⏳'}</td>
                </tr>
              ))}
              {articles.length === 0 && (
                <tr><td colSpan={5} className="empty">No articles found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="pagination">
          <button disabled={page <= 1} onClick={() => setPage(page - 1)}>← Prev</button>
          <span>Page {page}</span>
          <button disabled={articles.length < 30} onClick={() => setPage(page + 1)}>Next →</button>
        </div>
      </div>
    </div>
  );
}

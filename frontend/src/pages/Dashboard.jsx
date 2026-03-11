import { useEffect, useState } from 'react';
import api from '../api';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [articles, setArticles] = useState([]);
  const [triggering, setTriggering] = useState(false);

  useEffect(() => {
    api.get('/dashboard/stats').then((r) => setStats(r.data));
    api.get('/articles?limit=10').then((r) => setArticles(r.data));
  }, []);

  const triggerDigest = async () => {
    setTriggering(true);
    try {
      await api.post('/dashboard/trigger-digest');
      alert('Digest workflow triggered! Check logs in a few minutes.');
    } catch {
      alert('Failed to trigger digest.');
    }
    setTriggering(false);
  };

  return (
    <div className="page">
      <div className="page-header">
        <h2>Dashboard</h2>
        <button className="btn btn-primary" onClick={triggerDigest} disabled={triggering}>
          {triggering ? 'Running…' : '▶ Run Digest Now'}
        </button>
      </div>

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{stats.articles_today}</div>
            <div className="stat-label">Articles Today</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.total_articles}</div>
            <div className="stat-label">Total Articles</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.active_sources}</div>
            <div className="stat-label">Active Sources</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.active_topics}</div>
            <div className="stat-label">Topics</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.active_recipients}</div>
            <div className="stat-label">Recipients</div>
          </div>
          <div className="stat-card accent">
            <div className="stat-value">{stats.last_digest_date || '—'}</div>
            <div className="stat-label">Last Digest ({stats.last_digest_articles ?? 0} articles)</div>
          </div>
        </div>
      )}

      <div className="card">
        <h3>Recent Articles</h3>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Source</th>
                <th>Topic</th>
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
                  <td>{a.sent_status ? '✅' : '⏳'}</td>
                </tr>
              ))}
              {articles.length === 0 && (
                <tr><td colSpan={4} className="empty">No articles yet. Run the digest to scrape news.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

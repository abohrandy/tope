import { useEffect, useState } from 'react';
import api from '../api';

const empty = { name: '', url: '', rss_feed: '', is_active: true };

export default function Sites() {
  const [sites, setSites] = useState([]);
  const [form, setForm] = useState(empty);
  const [editing, setEditing] = useState(null);

  const load = () => api.get('/sites').then((r) => setSites(r.data));
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await api.put(`/sites/${editing}`, form);
      } else {
        await api.post('/sites', form);
      }
      setForm(empty);
      setEditing(null);
      load();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error saving site.');
    }
  };

  const startEdit = (site) => {
    setForm({ name: site.name, url: site.url, rss_feed: site.rss_feed || '', is_active: site.is_active });
    setEditing(site.id);
  };

  const toggleActive = async (site) => {
    await api.put(`/sites/${site.id}`, { is_active: !site.is_active });
    load();
  };

  const deleteSite = async (id) => {
    if (!confirm('Delete this site?')) return;
    await api.delete(`/sites/${id}`);
    load();
  };

  return (
    <div className="page">
      <div className="page-header"><h2>News Sites</h2></div>

      <div className="card">
        <h3>{editing ? 'Edit Site' : 'Add New Site'}</h3>
        <form onSubmit={handleSubmit} className="form-grid">
          <input placeholder="Site Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <input placeholder="URL" value={form.url} onChange={(e) => setForm({ ...form, url: e.target.value })} required />
          <input placeholder="RSS Feed URL (optional)" value={form.rss_feed} onChange={(e) => setForm({ ...form, rss_feed: e.target.value })} />
          <div className="form-actions">
            <button type="submit" className="btn btn-primary">{editing ? 'Update' : 'Add Site'}</button>
            {editing && <button type="button" className="btn btn-ghost" onClick={() => { setForm(empty); setEditing(null); }}>Cancel</button>}
          </div>
        </form>
      </div>

      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>Name</th><th>URL</th><th>RSS</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {sites.map((s) => (
                <tr key={s.id} className={!s.is_active ? 'row-disabled' : ''}>
                  <td>{s.name}</td>
                  <td><a href={s.url} target="_blank" rel="noreferrer">{s.url}</a></td>
                  <td>{s.rss_feed ? '✅ Yes' : '❌ No'}</td>
                  <td>
                    <button className={`toggle-btn ${s.is_active ? 'active' : ''}`} onClick={() => toggleActive(s)}>
                      {s.is_active ? 'Active' : 'Disabled'}
                    </button>
                  </td>
                  <td className="actions">
                    <button className="btn btn-sm" onClick={() => startEdit(s)}>Edit</button>
                    <button className="btn btn-sm btn-danger" onClick={() => deleteSite(s.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

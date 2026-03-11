import { useEffect, useState } from 'react';
import api from '../api';

const empty = { name: '', keywords: '' };

export default function Topics() {
  const [topics, setTopics] = useState([]);
  const [form, setForm] = useState(empty);
  const [editing, setEditing] = useState(null);

  const load = () => api.get('/topics').then((r) => setTopics(r.data));
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await api.put(`/topics/${editing}`, form);
      } else {
        await api.post('/topics', form);
      }
      setForm(empty);
      setEditing(null);
      load();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error saving topic.');
    }
  };

  const startEdit = (topic) => {
    setForm({ name: topic.name, keywords: topic.keywords });
    setEditing(topic.id);
  };

  const deleteTopic = async (id) => {
    if (!confirm('Delete this topic?')) return;
    await api.delete(`/topics/${id}`);
    load();
  };

  return (
    <div className="page">
      <div className="page-header"><h2>Topics</h2></div>

      <div className="card">
        <h3>{editing ? 'Edit Topic' : 'Add New Topic'}</h3>
        <form onSubmit={handleSubmit} className="form-grid">
          <input placeholder="Topic Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <input placeholder="Keywords (comma separated)" value={form.keywords} onChange={(e) => setForm({ ...form, keywords: e.target.value })} required />
          <div className="form-actions">
            <button type="submit" className="btn btn-primary">{editing ? 'Update' : 'Add Topic'}</button>
            {editing && <button type="button" className="btn btn-ghost" onClick={() => { setForm(empty); setEditing(null); }}>Cancel</button>}
          </div>
        </form>
      </div>

      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>Name</th><th>Keywords</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {topics.map((t) => (
                <tr key={t.id}>
                  <td><strong>{t.name}</strong></td>
                  <td>
                    <div className="keyword-list">
                      {t.keywords.split(',').map((kw, i) => (
                        <span key={i} className="badge">{kw.trim()}</span>
                      ))}
                    </div>
                  </td>
                  <td className="actions">
                    <button className="btn btn-sm" onClick={() => startEdit(t)}>Edit</button>
                    <button className="btn btn-sm btn-danger" onClick={() => deleteTopic(t.id)}>Delete</button>
                  </td>
                </tr>
              ))}
              {topics.length === 0 && (
                <tr><td colSpan={3} className="empty">No topics defined.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

import { useEffect, useState } from 'react';
import api from '../api';

const empty = { name: '', email: '', active: true };

export default function Recipients() {
  const [recipients, setRecipients] = useState([]);
  const [form, setForm] = useState(empty);
  const [editing, setEditing] = useState(null);

  const load = () => api.get('/recipients').then((r) => setRecipients(r.data));
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await api.put(`/recipients/${editing}`, form);
      } else {
        await api.post('/recipients', form);
      }
      setForm(empty);
      setEditing(null);
      load();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error saving recipient.');
    }
  };

  const startEdit = (rec) => {
    setForm({ name: rec.name, email: rec.email, active: rec.active });
    setEditing(rec.id);
  };

  const toggleActive = async (rec) => {
    await api.put(`/recipients/${rec.id}`, { active: !rec.active });
    load();
  };

  const deleteRecipient = async (id) => {
    if (!confirm('Remove this recipient?')) return;
    await api.delete(`/recipients/${id}`);
    load();
  };

  return (
    <div className="page">
      <div className="page-header"><h2>Email Recipients</h2></div>

      <div className="card">
        <h3>{editing ? 'Edit Recipient' : 'Add Recipient'}</h3>
        <form onSubmit={handleSubmit} className="form-grid">
          <input type="text" placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <input type="email" placeholder="Email Address" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <div className="form-actions">
            <button type="submit" className="btn btn-primary">{editing ? 'Update' : 'Add Recipient'}</button>
            {editing && <button type="button" className="btn btn-ghost" onClick={() => { setForm(empty); setEditing(null); }}>Cancel</button>}
          </div>
        </form>
      </div>

      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>Name</th><th>Email</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {recipients.map((r) => (
                <tr key={r.id} className={!r.active ? 'row-disabled' : ''}>
                  <td>{r.name}</td>
                  <td>{r.email}</td>
                  <td>
                    <button className={`toggle-btn ${r.active ? 'active' : ''}`} onClick={() => toggleActive(r)}>
                      {r.active ? 'Active' : 'Disabled'}
                    </button>
                  </td>
                  <td className="actions">
                    <button className="btn btn-sm" onClick={() => startEdit(r)}>Edit</button>
                    <button className="btn btn-sm btn-danger" onClick={() => deleteRecipient(r.id)}>Delete</button>
                  </td>
                </tr>
              ))}
              {recipients.length === 0 && (
                <tr><td colSpan={4} className="empty">No recipients added yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

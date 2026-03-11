import { useEffect, useState } from 'react';
import api from '../api';

export default function Settings() {
  const [form, setForm] = useState({
    sender_email: '',
    smtp_host: 'smtp.gmail.com',
    smtp_port: 587,
    smtp_user: '',
    smtp_password: '',
    subject_template: 'Morning News Brief – {date}',
  });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api.get('/settings/email').then((r) => setForm(r.data)).catch(() => {});
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.put('/settings/email', form);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch {
      alert('Error saving settings.');
    }
  };

  return (
    <div className="page">
      <div className="page-header"><h2>Email Settings</h2></div>

      <div className="card">
        <form onSubmit={handleSubmit} className="settings-form">
          <div className="form-group">
            <label>Sender Email</label>
            <input type="email" value={form.sender_email || ''} onChange={(e) => setForm({ ...form, sender_email: e.target.value })} placeholder="noreply@company.com" />
          </div>
          <div className="form-group">
            <label>SMTP Host</label>
            <input value={form.smtp_host} onChange={(e) => setForm({ ...form, smtp_host: e.target.value })} placeholder="smtp.gmail.com" />
          </div>
          <div className="form-group">
            <label>SMTP Port</label>
            <input type="number" value={form.smtp_port} onChange={(e) => setForm({ ...form, smtp_port: parseInt(e.target.value) })} />
          </div>
          <div className="form-group">
            <label>SMTP User</label>
            <input value={form.smtp_user || ''} onChange={(e) => setForm({ ...form, smtp_user: e.target.value })} placeholder="your-email@gmail.com" />
          </div>
          <div className="form-group">
            <label>SMTP Password</label>
            <input type="password" value={form.smtp_password || ''} onChange={(e) => setForm({ ...form, smtp_password: e.target.value })} placeholder="App password" />
          </div>
          <div className="form-group">
            <label>Subject Template</label>
            <input value={form.subject_template} onChange={(e) => setForm({ ...form, subject_template: e.target.value })} placeholder="Morning News Brief – {date}" />
            <small className="hint">Use <code>{'{date}'}</code> to insert the current date.</small>
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primary">Save Settings</button>
            {saved && <span className="success-msg">✅ Settings saved!</span>}
          </div>
        </form>
      </div>
    </div>
  );
}

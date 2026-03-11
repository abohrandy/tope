import { useEffect, useState } from 'react';
import api from '../api';

export default function EmailLogs() {
  const [digests, setDigests] = useState([]);

  useEffect(() => {
    api.get('/digests').then((r) => setDigests(r.data));
  }, []);

  return (
    <div className="page">
      <div className="page-header"><h2>Email Logs</h2></div>

      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Articles Sent</th>
                <th>Email Sent At</th>
              </tr>
            </thead>
            <tbody>
              {digests.map((d) => (
                <tr key={d.id}>
                  <td>{d.date}</td>
                  <td><strong>{d.articles_sent}</strong></td>
                  <td>{d.email_sent_time ? new Date(d.email_sent_time).toLocaleString() : 'Not sent'}</td>
                </tr>
              ))}
              {digests.length === 0 && (
                <tr><td colSpan={3} className="empty">No digest emails sent yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

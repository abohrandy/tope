import { NavLink, Outlet } from 'react-router-dom';
import '../index.css';

const navItems = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/articles', label: 'Articles', icon: '📰' },
  { to: '/sites', label: 'Sites', icon: '🌐' },
  { to: '/topics', label: 'Topics', icon: '🏷️' },
  { to: '/recipients', label: 'Recipients', icon: '📧' },
  { to: '/email-logs', label: 'Email Logs', icon: '📋' },
  { to: '/settings', label: 'Settings', icon: '⚙️' },
];

export default function Layout() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="brand-icon">📡</span>
          <h1>News Monitor</h1>
        </div>
        <nav>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `nav-link ${isActive ? 'active' : ''}`
              }
              end={item.to === '/'}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <small>© 2026 News Monitor</small>
        </div>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}

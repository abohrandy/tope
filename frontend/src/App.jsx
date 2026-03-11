import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Articles from './pages/Articles';
import Sites from './pages/Sites';
import Topics from './pages/Topics';
import Recipients from './pages/Recipients';
import EmailLogs from './pages/EmailLogs';
import Settings from './pages/Settings';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="articles" element={<Articles />} />
          <Route path="sites" element={<Sites />} />
          <Route path="topics" element={<Topics />} />
          <Route path="recipients" element={<Recipients />} />
          <Route path="email-logs" element={<EmailLogs />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

import { NavLink, Routes, Route, Navigate } from "react-router-dom";
import "../styles/dashboard.css";


const DashboardPage = () => <div className="page">Dashboard Content</div>;
const ReservationsPage = () => <div className="page">Reservations Page</div>;
const StaffPage = () => <div className="page">Staff Page</div>;
const AnalyticsPage = () => <div className="page">Analytics Page</div>;
const CRMPage = () => <div className="page">CRM Page</div>;
const SettingsPage = () => <div className="page">Settings Page</div>;
const AuditLogsPage = () => <div className="page">Audit Logs Page</div>;

export default function Home() {
  return (
    <div className="dashboard-wrapper">

      {/* ===== SIDEBAR ===== */}
      <aside className="sidebar">
        <div className="sidebar-logo">DineVibe</div>

        <nav>
          <ul>
            <li>
              <NavLink to="dashboard">🏠 Dashboard</NavLink>
            </li>
            <li>
              <NavLink to="reservations">📅 Reservations</NavLink>
            </li>
            <li>
              <NavLink to="staff">👥 Staff</NavLink>
            </li>
            <li>
              <NavLink to="analytics">📊 Analytics</NavLink>
            </li>
            <li>
              <NavLink to="crm">🛎 CRM</NavLink>
            </li>
            <li>
              <NavLink to="settings">⚙ Settings</NavLink>
            </li>
            <li>
              <NavLink to="audit-logs">🧾 Audit Logs</NavLink>
            </li>
          </ul>
        </nav>
      </aside>

      {/* ===== MAIN AREA ===== */}
      <div className="dashboard-main">

        {/* TOP NAVBAR */}
        <header className="dashboard-header">
          <div className="search-bar">
            <input type="text" placeholder="Search reservations, staff..." />
          </div>

          <div className="header-actions">
            <button className="action-btn">🌙</button>
            <button className="action-btn">🔔</button>
            <button className="action-btn">💬</button>
            <div className="profile-circle">HD</div>
          </div>
        </header>

        {/* ROUTED CONTENT */}
        <main className="dashboard-content">
          <Routes>
            <Route path="/" element={<Navigate to="dashboard" />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="reservations" element={<ReservationsPage />} />
            <Route path="staff" element={<StaffPage />} />
            <Route path="analytics" element={<AnalyticsPage />} />
            <Route path="crm" element={<CRMPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="audit-logs" element={<AuditLogsPage />} />
          </Routes>
        </main>

      </div>
    </div>
  );
}

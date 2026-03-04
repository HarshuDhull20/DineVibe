import { useState } from "react";
import "../styles/dashboard.css";

const dummyLogs = [
  {
    id: 1,
    user: "admin_dinevibe",
    action: "ROLE_CHANGE",
    details: "Promoted staff to Manager",
    ip: "192.168.1.10",
    date: "2026-02-12 10:24 AM",
    status: "success",
  },
  {
    id: 2,
    user: "owner_john",
    action: "LOGIN_FAILURE",
    details: "Invalid password attempt",
    ip: "192.168.1.14",
    date: "2026-02-12 09:10 AM",
    status: "warning",
  },
  {
    id: 3,
    user: "staff_anna",
    action: "PASSWORD_CHANGE",
    details: "Password updated successfully",
    ip: "192.168.1.20",
    date: "2026-02-11 08:55 PM",
    status: "success",
  },
  {
    id: 4,
    user: "influencer_max",
    action: "ACCOUNT_LOCKED",
    details: "Exceeded login attempts",
    ip: "182.45.67.12",
    date: "2026-02-11 06:30 PM",
    status: "error",
  },
];

export default function Audit() {
  const [search, setSearch] = useState("");
  const [actionFilter, setActionFilter] = useState("all");

  const filteredLogs = dummyLogs.filter((log) => {
    const matchesSearch =
      log.user.toLowerCase().includes(search.toLowerCase()) ||
      log.action.toLowerCase().includes(search.toLowerCase());

    const matchesAction =
      actionFilter === "all" || log.action === actionFilter;

    return matchesSearch && matchesAction;
  });

  return (
    <div className="dashboard-content">

      <h2 className="page-title">Security Audit Logs</h2>

      {/* Filters */}
      <div className="filters-row">
        <input
          type="text"
          placeholder="Search by user or action..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />

        <select
          value={actionFilter}
          onChange={(e) => setActionFilter(e.target.value)}
          className="status-filter"
        >
          <option value="all">All Actions</option>
          <option value="LOGIN_SUCCESS">LOGIN_SUCCESS</option>
          <option value="LOGIN_FAILURE">LOGIN_FAILURE</option>
          <option value="ROLE_CHANGE">ROLE_CHANGE</option>
          <option value="PASSWORD_CHANGE">PASSWORD_CHANGE</option>
          <option value="ACCOUNT_LOCKED">ACCOUNT_LOCKED</option>
        </select>

        <input type="date" />
      </div>

      {/* Table */}
      <div className="section-card">
        <table className="dashboard-table">
          <thead>
            <tr>
              <th>User</th>
              <th>Action</th>
              <th>Details</th>
              <th>IP Address</th>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {filteredLogs.map((log) => (
              <tr key={log.id}>
                <td>{log.user}</td>
                <td>{log.action}</td>
                <td>{log.details}</td>
                <td>{log.ip}</td>
                <td>{log.date}</td>
                <td>
                  <span className={`badge ${log.status}`}>
                    {log.status}
                  </span>
                </td>
              </tr>
            ))}

            {filteredLogs.length === 0 && (
              <tr>
                <td colSpan="6" style={{ textAlign: "center" }}>
                  No logs found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

    </div>
  );
}

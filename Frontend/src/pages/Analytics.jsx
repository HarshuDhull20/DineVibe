import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

import "../styles/dashboard.css";

const revenueData = [
  { day: "Mon", revenue: 12000 },
  { day: "Tue", revenue: 18000 },
  { day: "Wed", revenue: 15000 },
  { day: "Thu", revenue: 22000 },
  { day: "Fri", revenue: 28000 },
  { day: "Sat", revenue: 35000 },
  { day: "Sun", revenue: 30000 },
];

const reservationsData = [
  { day: "Mon", bookings: 20 },
  { day: "Tue", bookings: 32 },
  { day: "Wed", bookings: 28 },
  { day: "Thu", bookings: 40 },
  { day: "Fri", bookings: 55 },
  { day: "Sat", bookings: 70 },
  { day: "Sun", bookings: 60 },
];

export default function Analytics() {
  return (
    <div className="dashboard-content">

      <h2 className="page-title">Analytics Dashboard</h2>

      {/* ================= SUMMARY CARDS ================= */}
      <div className="metrics-grid">
        <div className="metric-card">
          <h4>Total Revenue</h4>
          <p className="metric-number">₹ 1,60,000</p>
          <span className="metric-growth positive">
            +12% this week
          </span>
        </div>

        <div className="metric-card">
          <h4>Total Reservations</h4>
          <p className="metric-number">305</p>
          <span className="metric-growth positive">
            +8% this week
          </span>
        </div>

        <div className="metric-card">
          <h4>Table Occupancy</h4>
          <p className="metric-number">78%</p>
          <span className="metric-growth negative">
            -2% today
          </span>
        </div>

        <div className="metric-card">
          <h4>Active Staff</h4>
          <p className="metric-number">14</p>
          <span className="metric-growth">
            On shift
          </span>
        </div>
      </div>

      {/* ================= REVENUE CHART ================= */}
      <div className="section-card" style={{ marginBottom: "30px" }}>
        <h3 style={{ marginBottom: "20px" }}>
          Weekly Revenue
        </h3>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={revenueData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#2563eb"
              strokeWidth={3}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* ================= RESERVATION CHART ================= */}
      <div className="section-card">
        <h3 style={{ marginBottom: "20px" }}>
          Weekly Reservations
        </h3>

        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={reservationsData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Bar
              dataKey="bookings"
              fill="#10b981"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}

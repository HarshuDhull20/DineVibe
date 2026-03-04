import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Utensils,
  Tag,
  ClipboardList,
  QrCode,
  FileText,
  Megaphone,
  FileBarChart2,
  Users,
  Settings,
  LogOut
} from "lucide-react";

export default function AdminSidebar() {
  const navigate = useNavigate();

  // RETRIEVE ACTUAL DETAILS
  const userName = localStorage.getItem("user_name") || "User";
  const userEmail = localStorage.getItem("user_email") || "email@dinevibe.com";

  const handleLogout = () => {
    localStorage.clear();
    sessionStorage.clear();
    navigate("/login", { replace: true });
  };

  return (
    <aside className="modern-sidebar">
      <div className="sidebar-top">
        <div className="logo-row">
          <div className="logo-circle">D</div>
          <div>
            <h3 className="logo-title">DineVibe</h3>
            <p className="role-text">Super Admin</p>
          </div>
        </div>

        <select className="branch-select">
          <option>Main Branch</option>
        </select>

        <nav className="sidebar-links">
          <NavLink to="/home/dashboard" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <LayoutDashboard size={18} />
            <span>Dashboard</span>
          </NavLink>
          <NavLink to="/home/menu-management" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <Utensils size={18} />
            <span>Menu Management</span>
          </NavLink>
          <NavLink to="/home/coupons" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <Tag size={18} />
            <span>Coupons & Promos</span>
          </NavLink>
          <NavLink to="/home/orders" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <ClipboardList size={18} />
            <span>Orders</span>
          </NavLink>
          <NavLink to="/home/qr-management" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <QrCode size={18} />
            <span>QR Management</span>
          </NavLink>
          <NavLink to="/home/invoices" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <FileText size={18} />
            <span>Invoices</span>
          </NavLink>
          <NavLink to="/home/marketing" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <Megaphone size={18} />
            <span>Marketing</span>
          </NavLink>
          <NavLink to="/home/content" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <FileBarChart2 size={18} />
            <span>Content</span>
          </NavLink>
          <NavLink to="/home/user-roles" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <Users size={18} />
            <span>User Roles</span>
          </NavLink>
          <NavLink to="/home/settings" className={({ isActive }) => isActive ? "sidebar-item active" : "sidebar-item"}>
            <Settings size={18} />
            <span>Settings</span>
          </NavLink>
        </nav>
      </div>

      <div className="sidebar-bottom">
        <div className="user-card">
          {/* DYNAMIC DETAILS */}
          <strong>{userName}</strong>
          <p>{userEmail}</p>
        </div>

        <button className="logout-btn" onClick={handleLogout}>
          <LogOut size={16} />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
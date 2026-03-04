import { NavLink } from "react-router-dom";

export default function AdminSidebar() {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">DineVibe</div>

      <div className="sidebar-nav">
        <NavLink to="/dashboard" className="sidebar-link">Dashboard</NavLink>
        <NavLink to="/menu-management" className="sidebar-link">Menu Management</NavLink>
        <NavLink to="/coupons" className="sidebar-link">Coupons & Promos</NavLink>
        <NavLink to="/orders" className="sidebar-link">Orders</NavLink>
        <NavLink to="/qr-management" className="sidebar-link">QR Management</NavLink>
        <NavLink to="/invoices" className="sidebar-link">Invoices</NavLink>
        <NavLink to="/marketing" className="sidebar-link">Marketing</NavLink>
        <NavLink to="/content" className="sidebar-link">Content</NavLink>
        <NavLink to="/user-roles" className="sidebar-link">User Roles</NavLink>
        <NavLink to="/settings" className="sidebar-link">Settings</NavLink>
      </div>
    </div>
  );
}
import { LayoutDashboard } from "lucide-react";
import "../styles/dashboard.css";

export default function Navbar() {
  return (
    <div className="modern-navbar minimal-navbar">
      <div className="breadcrumb">
        <LayoutDashboard size={20} />
        <span>Dashboard</span>
      </div>
    </div>
  );
}
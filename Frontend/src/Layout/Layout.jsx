import { Outlet, Navigate } from "react-router-dom";
import AdminSidebar from "../components/AdminSidebar";
import Navbar from "../components/Navbar";
import "../styles/dashboard.css";

export default function Layout() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="modern-layout">
      <AdminSidebar />
      <div className="main-area">
        <Navbar />
        <div className="content-area">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
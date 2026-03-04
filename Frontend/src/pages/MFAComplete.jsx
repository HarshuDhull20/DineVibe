import { CheckCircle } from "lucide-react";
import "../styles/auth.css";

export default function MFAComplete() {
  return (
    <div className="auth-wrapper">
      {/* TOP RIGHT TOAST NOTIFICATION */}
      <div className="success-toast">
        <div className="toast-icon">
          <CheckCircle size={16} />
        </div>
        <span>MFA setup successful!</span>
      </div>

      <div className="auth-logo">
        <div className="logo-icon-container" style={{ backgroundColor: "#5b5ffb" }}>
          <CheckCircle size={28} color="white" />
        </div>
        <h1>DineVibe</h1>
        <p>Restaurant Intelligence Platform</p>
      </div>

      <div className="auth-card success-card-center">
        <div className="success-check-large">
          <CheckCircle size={48} color="#22c55e" />
        </div>
        
        <h2>MFA Setup Complete!</h2>
        <p className="auth-subtitle">
          Redirecting to password setup...
        </p>

        {/* LOADING SPINNER BAR */}
        <div className="loading-bar-container">
          <div className="loading-bar-fill"></div>
        </div>
      </div>

      <div className="auth-footer">
        © 2026 DineVibe. Enterprise-grade restaurant management.
      </div>
    </div>
  );
}
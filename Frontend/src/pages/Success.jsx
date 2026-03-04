import { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { CheckCircle } from "lucide-react";
import "../styles/auth.css";

export default function Success() {
  const navigate = useNavigate();
  const location = useLocation();

  const queryParams = new URLSearchParams(location.search);
  const type = queryParams.get("type");

  useEffect(() => {
  const timer = setTimeout(() => {
    if (type === "mfa") {
      navigate("/set-password", { state: { email: location.state?.email } });
    } else if (type === "password") {
      navigate("/home");
    } else {
      navigate("/login");
    }
  }, 2500);

  return () => clearTimeout(timer);
}, [type, navigate]);

  const getTitle = () => {
    if (type === "mfa") return "MFA Setup Complete";
    if (type === "password") return "Password Updated Successfully";
    return "Success";
  };

  const getSubtitle = () => {
    if (type === "mfa")
      return "Your account is now secured with multi-factor authentication.";
    if (type === "password")
      return "Your new password has been saved securely.";
    return "";
  };

  const getRedirectText = () => {
    if (type === "mfa") return "Redirecting to password setup...";
    if (type === "password") return "Redirecting to dashboard...";
    return "Redirecting...";
  };

  return (
    <div className="auth-wrapper">

      <div className="auth-card success-card">

        <div className="success-icon">
          <CheckCircle size={42} />
        </div>

        <h2>{getTitle()}</h2>

        <p className="auth-subtitle">
          {getSubtitle()}
        </p>

        <div className="success-redirect-text">
          {getRedirectText()}
        </div>

      </div>

    </div>
  );
}

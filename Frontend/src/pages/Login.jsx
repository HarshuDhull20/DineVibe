import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Mail, Lock, Eye, EyeOff, ShieldCheck } from "lucide-react";
import { 
  signInWithEmailAndPassword, 
  GoogleAuthProvider, 
  signInWithPopup 
} from "firebase/auth";
import { auth } from "../firebase";
import "../styles/auth.css";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  /* ==============================
     EMAIL/PASSWORD LOGIN
  ============================== */
  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email.trim(),
        password.trim()
      );
      const idToken = await userCredential.user.getIdToken();
      
      // Store data for MFA redirection
      sessionStorage.setItem("firebase_temp_token", idToken);
      sessionStorage.setItem("mfa_email", email.trim());
      
      navigate("/mfa");
    } catch (err) {
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  /* ==============================
     GOOGLE SIGN-IN LOGIC
  ============================== */
  const handleGoogleSignIn = async () => {
    setError("");
    setLoading(true);
    const provider = new GoogleAuthProvider();
    
    // Optional: Force account selection
    provider.setCustomParameters({ prompt: 'select_account' });

    try {
      const result = await signInWithPopup(auth, provider);
      const idToken = await result.user.getIdToken();
      
      // Store Google user info for MFA
      sessionStorage.setItem("firebase_temp_token", idToken);
      sessionStorage.setItem("mfa_email", result.user.email);
      
      navigate("/mfa");
    } catch (err) {
      console.error("Google Auth Error:", err);
      // Handle specific Firebase errors like popup closed
      if (err.code === "auth/popup-closed-by-user") {
        setError("Sign-in popup was closed before completion.");
      } else {
        setError("Google sign-in failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-logo">
        <div className="logo-icon-container">
          <ShieldCheck size={32} color="white" />
        </div>
        <h1>DineVibe</h1>
        <p>Restaurant Intelligence Platform</p>
      </div>

      <div className="auth-card">
        <h2>Welcome Back</h2>
        <p className="auth-subtitle">
          Sign in to access your restaurant dashboard
        </p>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleLogin}>
          {/* EMAIL */}
          <div className="auth-input-group">
            <label>Email Address</label>
            <div className="auth-input">
              <Mail size={18} className="input-icon" />
              <input
                type="email"
                placeholder="email@restaurant.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          {/* PASSWORD */}
          <div className="auth-input-group">
            <div className="label-row">
              <label>Password</label>
            </div>
            <div className="auth-input">
              <Lock size={18} className="input-icon" />
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <div className="forgot-password-container">
             <span className="demo-text">Demo: test@dinevibe.com / Test@123</span>
             <Link to="/forgot-password" size={13} className="forgot-link">Forgot Password?</Link>
          </div>

          <button
            type="submit"
            className="primary-btn full-width"
            disabled={loading}
          >
            {loading ? "Signing In..." : "Sign In"}
          </button>
        </form>

        <div className="auth-divider">
          <span>Or continue with</span>
        </div>

        <button 
          type="button" 
          className="google-btn full-width" 
          onClick={handleGoogleSignIn}
          disabled={loading}
        >
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" />
          {loading ? "Connecting..." : "Sign in with Google"}
        </button>

        <div className="google-note">
          <strong>Note:</strong> Google login is only available for pre-registered accounts. Contact your administrator if you need access.
        </div>

        <div className="auth-card-footer">
          Don't have an account? <Link to="/register">Register Now</Link>
        </div>
      </div>

      <div className="auth-footer">
        © 2026 DineVibe. Enterprise-grade restaurant management.
      </div>
    </div>
  );
}
import { useNavigate } from "react-router-dom";

export default function InfluencerLogin() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <h2>Influencer Login</h2>

      <button
        onClick={() => {
          window.location.href = "http://localhost:8001/auth/google";
        }}
        style={{ margin: "10px" }}
      >
        Continue with Google
      </button>

      <button
        onClick={() => {
          window.location.href = "http://localhost:8001/auth/apple";
        }}
        style={{ margin: "10px" }}
      >
        Continue with Apple
      </button>
    </div>
  );
}

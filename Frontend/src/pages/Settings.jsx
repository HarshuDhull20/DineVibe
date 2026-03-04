import { useState } from "react";
import "../styles/dashboard.css";

export default function Settings() {
  const [theme, setTheme] = useState("light");
  const [restaurantName, setRestaurantName] = useState("DineVibe Bistro");
  const [email, setEmail] = useState("contact@dinevibe.com");
  const [phone, setPhone] = useState("+91 9876543210");
  const [notifications, setNotifications] = useState(true);
  const [mfa, setMfa] = useState(false);

  const handleSave = () => {
    console.log({
      restaurantName,
      email,
      phone,
      theme,
      notifications,
      mfa,
    });

    alert("Settings saved successfully!");
  };

  return (
    <div className="dashboard-content">

      <h2 className="page-title">Restaurant Settings</h2>

      <div className="settings-grid">

        {/* GENERAL SETTINGS */}
        <div className="section-card">
          <h3>General Information</h3>

          <label>Restaurant Name</label>
          <input
            type="text"
            value={restaurantName}
            onChange={(e) => setRestaurantName(e.target.value)}
          />

          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label>Phone</label>
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />
        </div>

        {/* PREFERENCES */}
        <div className="section-card">
          <h3>Preferences</h3>

          <label>Theme</label>
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
          >
            <option value="light">Light Mode</option>
            <option value="dark">Dark Mode</option>
          </select>

          <div className="toggle-row">
            <input
              type="checkbox"
              id="notifications"
              checked={notifications}
              onChange={() => setNotifications(!notifications)}
            />
            <label htmlFor="notifications">
              Enable Email Notifications
            </label>
          </div>

          <div className="toggle-row">
            <input
              type="checkbox"
              id="mfa"
              checked={mfa}
              onChange={() => setMfa(!mfa)}
            />
            <label htmlFor="mfa">
              Enable MFA Security
            </label>
          </div>
        </div>

        {/* SECURITY */}
        <div className="section-card">
          <h3>Security Settings</h3>

          <button className="primary-btn" style={{ marginBottom: "10px" }}>
            Change Password
          </button>

          <button
            className="secondary-btn"
            style={{
              backgroundColor: "#fee2e2",
              color: "#b91c1c",
              border: "1px solid #fecaca"
            }}
          >
            Deactivate Account
          </button>
        </div>

      </div>

      <div style={{ marginTop: "30px" }}>
        <button className="primary-btn" onClick={handleSave}>
          Save Changes
        </button>
      </div>

    </div>
  );
}

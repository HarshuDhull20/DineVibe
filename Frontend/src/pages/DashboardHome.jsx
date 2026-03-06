import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer,
  BarChart, Bar, CartesianGrid
} from "recharts";
import { 
  TrendingUp, ShoppingBag, Calendar, Users, 
  Upload, Video, Plus, ChevronRight, MoreHorizontal,
  LogOut
} from "lucide-react";

import "../styles/dashboard.css";

const revenueData = [
  { day: "Mon", value: 4000 }, { day: "Tue", value: 3200 },
  { day: "Wed", value: 2400 }, { day: "Thu", value: 3400 },
  { day: "Fri", value: 2200 }, { day: "Sat", value: 2900 },
  { day: "Sun", value: 3800 }
];

export default function DashboardHome() {
  const navigate = useNavigate();
  const userName = localStorage.getItem("user_name") || "Alex";

  const [isPosting, setIsPosting] = useState(false);
  const storyInputRef = useRef(null);
  const videoInputRef = useRef(null);

  /* ==============================
     HANDLERS
  ============================== */

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  }

  const handleStoryUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log("Uploading Story:", file.name);
      alert(`Story "${file.name}" upload started!`);
    }
  };

  const handleVideoUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log("Uploading Video:", file.name);
      alert(`Video "${file.name}" upload started!`);
    }
  };

  const handleCreatePost = () => {
    setIsPosting(true);
    const content = prompt("Enter your post content:");
    if (content) {
      alert("Post created successfully!");
      setIsPosting(false);
    }
  };

  return (
    <div className="dashboard-container">

      <input 
        type="file" 
        ref={storyInputRef} 
        style={{ display: 'none' }} 
        accept="image/*" 
        onChange={handleStoryUpload} 
      />
      <input 
        type="file" 
        ref={videoInputRef} 
        style={{ display: 'none' }} 
        accept="video/*" 
        onChange={handleVideoUpload} 
      />

      <header className="dashboard-header-modern">
        <div className="header-greeting">
          <h2>Good Morning, {userName}! 👋</h2>
          <p>Here’s what’s happening at your restaurant today.</p>
        </div>

        <div className="header-actions">
          <button 
            className="btn-secondary" 
            onClick={() => storyInputRef.current.click()}
          >
            <Upload size={16}/> Upload Story
          </button>
          
          <button 
            className="btn-secondary" 
            onClick={() => videoInputRef.current.click()}
          >
            <Video size={16}/> Upload Video
          </button>
          
          <button 
            className="btn-primary" 
            onClick={handleCreatePost}
            disabled={isPosting}
          >
            <Plus size={16}/> {isPosting ? "Posting..." : "Create Post"}
          </button>

          <button 
            className="btn-secondary"
            onClick={handleLogout}
          >
            <LogOut size={16}/> Logout
          </button>

        </div>
      </header>

      <section className="metrics-row">
        <div className="kpi-card">
          <div className="kpi-info">
            <h4>Total Revenue</h4>
            <p className="kpi-value">$12,450</p>
            <span className="stat positive">+12.5% <small>from last month</small></span>
          </div>
          <div className="kpi-icon-wrapper bg-blue"><TrendingUp size={20}/></div>
        </div>

        <div className="kpi-card">
          <div className="kpi-info">
            <h4>Total Orders</h4>
            <p className="kpi-value">1,240</p>
            <span className="stat negative">-2.4% <small>from last month</small></span>
          </div>
          <div className="kpi-icon-wrapper bg-green"><ShoppingBag size={20}/></div>
        </div>

        <div className="kpi-card">
          <div className="kpi-info">
            <h4>Live Bookings</h4>
            <p className="kpi-value">48</p>
            <span className="stat positive">+8.2% <small>from last month</small></span>
          </div>
          <div className="kpi-icon-wrapper bg-purple"><Calendar size={20}/></div>
        </div>

        <div className="kpi-card">
          <div className="kpi-info">
            <h4>Active QR Scans</h4>
            <p className="kpi-value">856</p>
            <span className="stat positive">+24.5% <small>from last month</small></span>
          </div>
          <div className="kpi-icon-wrapper bg-orange"><Users size={20}/></div>
        </div>
      </section>

      <div className="main-data-grid">
        <div className="chart-card">
          <div className="card-header">
            <h3>Revenue Overview</h3>
            <MoreHorizontal size={18} className="text-muted" />
          </div>
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={revenueData}>
              <CartesianGrid vertical={false} stroke="#f1f5f9" />
              <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} dy={10} />
              <YAxis axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} dx={-10} />
              <Tooltip contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 10px 15 -3 rgba(0,0,0,0.1)'}} />
              <Line type="monotone" dataKey="value" stroke="#5b5ffb" strokeWidth={3} dot={{r: 4, fill: '#5b5ffb', strokeWidth: 2, stroke: '#fff'}} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="orders-card">
          <h3>Today’s Orders</h3>
          <div className="orders-list">
            {[2046, 2047, 2048, 2049, 2050].map((id, index) => (
              <div className="order-row-item" key={id}>
                <div className="order-main">
                  <div className="food-icon-box">🍔</div>
                  <div>
                    <span className="order-number">Order #{id}</span>
                    <span className="order-meta">Table {index + 3} • 2 items</span>
                  </div>
                </div>
                <div className="order-right">
                  <span className="price">$45.00</span>
                  <span className={`status ${index % 2 === 0 ? 'cooking' : 'completed'}`}>
                    {index % 2 === 0 ? 'Cooking' : 'Completed'}
                  </span>
                </div>
              </div>
            ))}
          </div>
          <button className="btn-view-all">View all orders <ChevronRight size={14}/></button>
        </div>
      </div>
    </div>
  );
}
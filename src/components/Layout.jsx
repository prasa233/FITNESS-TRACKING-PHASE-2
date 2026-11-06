import { Bell, Search } from "lucide-react";
import { useLocation } from "react-router-dom";
import Sidebar from "./Sidebar.jsx";

const titles = {
  "/": "Dashboard", "/workouts": "My Workouts", "/plans": "Workout Planner",
  "/exercises": "Exercise Library", "/progress": "Progress Comparison",
  "/streaks": "Streak Tracking", "/achievements": "Achievements",
  "/goals": "My Goals", "/notifications": "Notifications", "/profile": "My Profile"
};

export default function Layout({ children }) {
  const location = useLocation();
  const user = JSON.parse(localStorage.getItem("fittrack_user") || "null");
  const title = titles[location.pathname] || "FitTrack";
  return <div className="app-shell">
    <Sidebar/>
    <main className="main-area">
      <header className="topbar">
        <div><div className="eyebrow">FITTRACK / PHASE 2</div><h1>{title}</h1></div>
        <div className="topbar-right">
          <div className="top-search"><Search size={16}/><span>Fitness journey</span></div>
          <button className="icon-btn" aria-label="Notifications" onClick={() => location.pathname !== "/notifications" && (window.location.href="/notifications")}><Bell size={18}/></button>
          <div className="avatar">{(user?.name || user?.email || "P").slice(0,1).toUpperCase()}</div>
        </div>
      </header>
      <section className="page-content">{children}</section>
    </main>
  </div>;
}
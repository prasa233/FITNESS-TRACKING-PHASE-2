import { NavLink, useNavigate } from "react-router-dom";
import {
  Activity, LayoutDashboard, Dumbbell, CalendarDays,
  ChartNoAxesCombined, Flame, Trophy, Target, Bell, UserRound, LogOut
} from "lucide-react";

const links = [
  { to: "/", label: "Overview", icon: LayoutDashboard },
  { to: "/workouts", label: "My Workouts", icon: Activity },
  { to: "/plans", label: "Workout Planner", icon: CalendarDays },
  { to: "/exercises", label: "Exercise Library", icon: Dumbbell },
  { to: "/progress", label: "Progress", icon: ChartNoAxesCombined },
  { to: "/streaks", label: "Streaks", icon: Flame },
  { to: "/achievements", label: "Achievements", icon: Trophy },
  { to: "/goals", label: "Goals", icon: Target },
  { to: "/notifications", label: "Notifications", icon: Bell },
  { to: "/profile", label: "My Profile", icon: UserRound }
];

export default function Sidebar() {
  const navigate = useNavigate();
  const logout = () => {
    localStorage.removeItem("fittrack_token");
    localStorage.removeItem("fittrack_user");
    navigate("/login");
  };

  return <aside className="sidebar">
    <div className="brand"><span className="brand-mark"><Activity size={22}/></span><span>FitTrack</span></div>
    <div className="side-label">WORKSPACE</div>
    <nav className="nav-list">
      {links.map(({to,label,icon:Icon}) =>
        <NavLink key={to} to={to} end={to === "/"} className={({isActive}) => `nav-link ${isActive ? "active" : ""}`}>
          <Icon size={18}/><span>{label}</span>
        </NavLink>
      )}
    </nav>
    <button className="logout-btn" onClick={logout}><LogOut size={18}/> Sign out</button>
    <div className="sidebar-foot">FITNESS · TRACKING · GROWTH</div>
  </aside>;
}
import { useEffect, useState } from "react";
import { Activity, Flame, Trophy, CalendarDays, ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";
import api, {getErrorMessage} from "../services/api.js";
import {PageTitle,StatCard,Loading,ErrorMessage,Empty} from "../components/Ui.jsx";

export default function Dashboard() {
  const [data,setData] = useState(null), [workouts,setWorkouts] = useState([]);
  const [error,setError] = useState("");
  useEffect(() => {
    Promise.all([api.get("/dashboard/"),api.get("/workouts")])
      .then(([d,w]) => {setData(d.data);setWorkouts(Array.isArray(w.data)?w.data:[]);})
      .catch(e=>setError(getErrorMessage(e)));
  },[]);
  if (!data && !error) return <Loading/>;
  const plans = data?.upcoming_workouts || [];
  return <>
    <div className="welcome-banner"><div><div className="eyebrow light">YOUR DAILY MOMENTUM</div><h2>Make today count.</h2><p>Consistency is built one session at a time. Keep showing up.</p><Link className="btn white-btn" to="/plans">Plan a workout <ArrowUpRight size={16}/></Link></div><div className="banner-symbol"><Activity size={110}/></div></div>
    <ErrorMessage message={error}/>
    <PageTitle title="Your overview" subtitle="A snapshot of your fitness activity."/>
    <div className="stats-grid">
      <StatCard label="Workouts logged" value={workouts.length} detail="Recorded sessions" icon={Activity}/>
      <StatCard label="Current streak" value={`${data?.current_streak ?? 0} days`} detail="Keep the momentum" icon={Flame} tone="orange"/>
      <StatCard label="Longest streak" value={`${data?.longest_streak ?? 0} days`} detail="Your personal best" icon={CalendarDays} tone="green"/>
      <StatCard label="Badges earned" value={data?.total_badges ?? 0} detail="Milestones unlocked" icon={Trophy} tone="purple"/>
    </div>
    <div className="two-col">
      <div className="panel"><PageTitle title="Upcoming workouts" subtitle="Your next planned sessions." action={<Link className="text-link" to="/plans">View planner →</Link>}/>
        {plans.length ? <div className="list">{plans.slice(0,5).map(p=><div className="list-row" key={p.id}><div className="row-icon"><DumbbellIcon/></div><div className="row-main"><b>{p.title}</b><small>{p.description || "Workout session"}</small></div><span className="date-pill">{p.scheduled_date}</span></div>)}</div> : <Empty title="No upcoming workouts" detail="Schedule your next session to see it here."/>}
      </div>
      <div className="panel"><PageTitle title="Recent activity" subtitle="Your logged workouts." action={<Link className="text-link" to="/workouts">View all →</Link>}/>
        {workouts.length ? <div className="list">{workouts.slice(0,5).map((w,i)=><div className="list-row" key={w.id ?? i}><div className="row-icon"><Activity size={18}/></div><div className="row-main"><b>{w.workout_type || w.name || w.title || "Workout"}</b><small>{w.date || w.created_at || "Completed session"}</small></div><span className="status-dot">Logged</span></div>)}</div> : <Empty title="No workouts logged" detail="Complete a workout and your activity will show here."/>}
      </div>
    </div>
  </>;
}
function DumbbellIcon(){return <Activity size={18}/>;}
import {useEffect,useState} from "react";
import {Flame,CalendarCheck} from "lucide-react";
import api,{getErrorMessage} from "../services/api.js";
import {PageTitle,StatCard,ErrorMessage,Loading} from "../components/Ui.jsx";
export default function Streaks(){
 const [data,setData]=useState(null),[error,setError]=useState("");
 useEffect(()=>{api.get("/streaks/").then(r=>setData(r.data)).catch(e=>setError(getErrorMessage(e)));},[]);
 if(!data&&!error)return <Loading/>;
 return <><PageTitle title="Streak tracking" subtitle="Celebrate consistency, one day at a time."/><ErrorMessage message={error}/>
 <div className="streak-hero"><Flame size={46}/><div><div className="eyebrow light">CURRENT MOMENTUM</div><strong>{data?.current_streak??0} day streak</strong><p>Show up today to keep your routine moving.</p></div></div>
 <div className="stats-grid"><StatCard label="Current streak" value={`${data?.current_streak??0} days`} icon={Flame} tone="orange"/><StatCard label="Longest streak" value={`${data?.longest_streak??0} days`} detail="Personal best" icon={CalendarCheck} tone="green"/></div>
 <div className="panel"><h3 className="panel-heading">Build your consistency</h3><p className="muted">Your streak is updated when a workout is successfully recorded. The backend should enforce daily uniqueness and calculate missed-day resets.</p></div></>;
}
import {useEffect,useState} from "react";
import {BarChart,Bar,XAxis,YAxis,Tooltip,ResponsiveContainer,CartesianGrid} from "recharts";
import {ChartNoAxesCombined,TrendingUp} from "lucide-react";
import api,{getErrorMessage} from "../services/api.js";
import {PageTitle,StatCard,ErrorMessage,Loading} from "../components/Ui.jsx";
export default function Progress(){
 const [week,setWeek]=useState(null),[month,setMonth]=useState(null),[error,setError]=useState("");
 useEffect(()=>{Promise.all([api.get("/progress/weekly"),api.get("/progress/monthly")]).then(([w,m])=>{setWeek(w.data);setMonth(m.data);}).catch(e=>setError(getErrorMessage(e)));},[]);
 if(!week&&!error)return <Loading/>;
 const chart=[{period:"Previous week",count:week?.previous_week??0},{period:"This week",count:week?.current_week??0},{period:"Previous month",count:month?.previous_month??0},{period:"This month",count:month?.current_month??0}];
 return <><PageTitle title="Progress comparison" subtitle="Compare your recent workout consistency."/><ErrorMessage message={error}/>
 <div className="stats-grid"><StatCard label="This week" value={week?.current_week??"—"} detail="Workouts" icon={ChartNoAxesCombined}/><StatCard label="Weekly change" value={week?.improvement??"—"} detail="Compared with previous week" icon={TrendingUp} tone="green"/><StatCard label="This month" value={month?.current_month??"—"} detail="Workouts" icon={ChartNoAxesCombined} tone="purple"/><StatCard label="Monthly change" value={month?.improvement??"—"} detail="Compared with previous month" icon={TrendingUp} tone="orange"/></div>
 <div className="panel chart-panel"><h3 className="panel-heading">Workout trend</h3><p className="muted">Number of recorded workouts in each period.</p><div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><BarChart data={chart}><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e9edf4"/><XAxis dataKey="period" tickLine={false} axisLine={false}/><YAxis allowDecimals={false} tickLine={false} axisLine={false}/><Tooltip/><Bar dataKey="count" fill="#6c63ff" radius={[7,7,0,0]}/></BarChart></ResponsiveContainer></div></div>
 <p className="hint">These comparison endpoints currently report workout counts, not calories or duration.</p></>;
}
import {useEffect,useState} from "react";
import {CalendarDays,Plus,Trash2} from "lucide-react";
import api,{getErrorMessage} from "../services/api.js";
import {PageTitle,ErrorMessage,Empty} from "../components/Ui.jsx";
const blank={title:"",description:"",scheduled_date:""};
export default function Plans(){
 const [items,setItems]=useState([]),[form,setForm]=useState(blank),[error,setError]=useState("");
 const load=()=>api.get("/workout-plans/").then(r=>setItems(r.data||[])).catch(e=>setError(getErrorMessage(e)));
 useEffect(()=>{load();},[]);
 const submit=async e=>{e.preventDefault();setError("");try{await api.post("/workout-plans/",form);setForm(blank);load();}catch(e){setError(getErrorMessage(e));}};
 const remove=async id=>{try{await api.delete(`/workout-plans/${id}`);load();}catch(e){setError(getErrorMessage(e));}};
 return <><PageTitle title="Workout planner" subtitle="Schedule future sessions and stay organized."/><ErrorMessage message={error}/>
 <div className="two-col align-start"><div className="panel"><h3 className="panel-heading">Schedule a session</h3><form className="stack-form" onSubmit={submit}>
 <label className="field"><span>Workout title</span><input required minLength="2" value={form.title} onChange={e=>setForm({...form,title:e.target.value})} placeholder="e.g. Morning run"/></label>
 <label className="field"><span>Description</span><textarea value={form.description} onChange={e=>setForm({...form,description:e.target.value})} placeholder="Add a few details"/></label>
 <label className="field"><span>Scheduled date</span><input type="date" required value={form.scheduled_date} onChange={e=>setForm({...form,scheduled_date:e.target.value})}/></label>
 <button className="btn primary"><Plus size={16}/> Add to planner</button></form></div>
 <div className="panel"><h3 className="panel-heading">Upcoming schedule <span className="count">{items.length}</span></h3>{items.length?<div className="list">{items.map(p=><div className="list-row" key={p.id}><div className="row-icon"><CalendarDays size={18}/></div><div className="row-main"><b>{p.title}</b><small>{p.description||"Workout session"}</small><small>{p.scheduled_date}</small></div><button className="icon-danger" onClick={()=>remove(p.id)}><Trash2 size={16}/></button></div>)}</div>:<Empty title="Your planner is clear" detail="Add your first workout on the left."/>}</div></div></>;
}
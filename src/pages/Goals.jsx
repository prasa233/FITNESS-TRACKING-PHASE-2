import {useEffect,useState} from "react";
import {Target,Plus} from "lucide-react";
import api,{getErrorMessage} from "../services/api.js";
import {PageTitle,ErrorMessage,Empty} from "../components/Ui.jsx";
export default function Goals(){
 const [items,setItems]=useState([]),[error,setError]=useState("");
 const [form,setForm]=useState({title:"",description:"",target:10});
 const load=()=>api.get("/goals").then(r=>setItems(r.data||[])).catch(e=>setError(getErrorMessage(e)));
 useEffect(()=>{load();},[]);
 const submit=async e=>{e.preventDefault();setError("");try{await api.post("/goals",{...form,target:Number(form.target)});setForm({title:"",description:"",target:10});load();}catch(e){setError(getErrorMessage(e));}};
 return <><PageTitle title="My goals" subtitle="Set a target and work toward it consistently."/><ErrorMessage message={error}/><div className="two-col align-start"><div className="panel"><h3 className="panel-heading">Create a goal</h3><form className="stack-form" onSubmit={submit}><label className="field"><span>Goal title</span><input required value={form.title} onChange={e=>setForm({...form,title:e.target.value})} placeholder="e.g. Exercise 4 times a week"/></label><label className="field"><span>Description</span><textarea value={form.description} onChange={e=>setForm({...form,description:e.target.value})}/></label><label className="field"><span>Target</span><input type="number" min="1" value={form.target} onChange={e=>setForm({...form,target:e.target.value})}/></label><button className="btn primary"><Plus size={16}/> Add goal</button></form><p className="hint">Adjust the request fields to match the GoalSchema shown in your Swagger page.</p></div><div className="panel"><h3 className="panel-heading">Your goals</h3>{items.length?<div className="list">{items.map((g,i)=><div className="list-row" key={g.id??i}><div className="row-icon"><Target size={18}/></div><div className="row-main"><b>{g.title||g.name||"Fitness goal"}</b><small>{g.description||JSON.stringify(g)}</small></div></div>)}</div>:<Empty title="No goals yet" detail="Create your first fitness goal."/>}</div></div></>;
}
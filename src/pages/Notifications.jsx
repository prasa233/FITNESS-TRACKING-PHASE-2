import {useEffect,useState} from "react";
import {Bell,Check} from "lucide-react";
import api,{getErrorMessage} from "../services/api.js";
import {PageTitle,ErrorMessage,Empty} from "../components/Ui.jsx";
export default function Notifications(){
 const [items,setItems]=useState([]),[error,setError]=useState("");
 const load=()=>api.get("/notifications").then(r=>setItems(r.data||[])).catch(e=>setError(getErrorMessage(e)));
 useEffect(()=>{load();},[]);
 const mark=async id=>{try{await api.patch(`/notifications/${id}/read`);load();}catch(e){setError(getErrorMessage(e));}};
 return <><PageTitle title="Notifications" subtitle="Stay up to date with your fitness activity."/><ErrorMessage message={error}/>{items.length?<div className="panel"><div className="list">{items.map((n,i)=><div className="list-row" key={n.id??i}><div className="row-icon"><Bell size={18}/></div><div className="row-main"><b>{n.title||n.message||"Notification"}</b><small>{n.created_at||n.date||""}</small></div>{n.id && <button className="icon-btn" onClick={()=>mark(n.id)} title="Mark as read"><Check size={16}/></button>}</div>)}</div></div>:<Empty title="You're all caught up" detail="New notifications will appear here."/>}</>;
}
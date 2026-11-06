import {useEffect,useState} from "react";
import {Trophy,LockKeyhole,Medal} from "lucide-react";
import api,{getErrorMessage} from "../services/api.js";
import {PageTitle,ErrorMessage,Empty} from "../components/Ui.jsx";
export default function Achievements(){
 const [all,setAll]=useState([]),[earned,setEarned]=useState([]),[error,setError]=useState("");
 useEffect(()=>{Promise.all([api.get("/badges/"),api.get("/badges/my-badges")]).then(([a,m])=>{setAll(a.data||[]);setEarned(m.data||[]);}).catch(e=>setError(getErrorMessage(e)));},[]);
 const earnedIds=new Set(earned.map(x=>x.badge_id));
 return <><PageTitle title="Achievements" subtitle="Every milestone is proof of your progress."/><ErrorMessage message={error}/><div className="achievement-summary"><Trophy size={25}/><div><b>{earned.length} achievements unlocked</b><span>Keep training to collect more milestones.</span></div></div>
 {all.length?<div className="badge-grid">{all.map(b=>{const unlocked=earnedIds.has(b.id);return <article className={`badge-card ${unlocked?"unlocked":""}`} key={b.id}><div className="badge-art">{unlocked?<Medal size={30}/>:<LockKeyhole size={27}/>}</div><h3>{b.name}</h3><p>{b.description}</p><span className={`badge-status ${unlocked?"earned":""}`}>{unlocked?"Unlocked":"Not earned yet"}</span></article>;})}</div>:<Empty title="No badges configured" detail="Add badge definitions to the backend to display achievements."/>}</>;
}
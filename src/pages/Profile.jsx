import {useEffect,useState} from "react";
import {UserRound} from "lucide-react";
import api,{getErrorMessage} from "../services/api.js";
import {PageTitle,ErrorMessage,Loading} from "../components/Ui.jsx";
export default function Profile(){
 const [user,setUser]=useState(JSON.parse(localStorage.getItem("fittrack_user")||"null")),[error,setError]=useState("");
 useEffect(()=>{api.get("/auth/me").then(r=>{setUser(r.data);localStorage.setItem("fittrack_user",JSON.stringify(r.data));}).catch(e=>setError(getErrorMessage(e)));},[]);
 return <><PageTitle title="My profile" subtitle="Your FitTrack account details."/><ErrorMessage message={error}/><div className="panel profile-panel"><div className="profile-avatar"><UserRound size={34}/></div><div><h2>{user?.name||"FitTrack member"}</h2><p className="muted">{user?.email||"Email not available"}</p></div><div className="profile-details"><div><span>Name</span><b>{user?.name||"—"}</b></div><div><span>Email</span><b>{user?.email||"—"}</b></div><div><span>User ID</span><b>{user?.id??"—"}</b></div></div></div></>;
}
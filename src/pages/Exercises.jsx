import {useEffect,useState} from "react";
import {Search,Dumbbell} from "lucide-react";
import api,{getErrorMessage} from "../services/api.js";
import {PageTitle,ErrorMessage,Empty} from "../components/Ui.jsx";
export default function Exercises(){
 const [items,setItems]=useState([]),[search,setSearch]=useState(""),[category,setCategory]=useState(""),[error,setError]=useState("");
 useEffect(()=>{const timer=setTimeout(()=>api.get("/exercises/",{params:{search,category}}).then(r=>setItems(r.data||[])).catch(e=>setError(getErrorMessage(e))),250);return()=>clearTimeout(timer);},[search,category]);
 return <><PageTitle title="Exercise library" subtitle="Explore movements for every kind of training."/><ErrorMessage message={error}/>
 <div className="filter-bar"><div className="search-field"><Search size={17}/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search exercises..."/></div><select value={category} onChange={e=>setCategory(e.target.value)}><option value="">All categories</option><option>Cardio</option><option>Strength</option><option>Yoga</option></select></div>
 {items.length?<div className="exercise-grid">{items.map(x=><article className="exercise-card" key={x.id}><div className="exercise-top"><div className="exercise-icon"><Dumbbell/></div><span className="category-tag">{x.category}</span></div><h3>{x.name}</h3><p>{x.description||"Build consistency with this exercise."}</p><div className="exercise-duration">{x.duration} minutes</div></article>)}</div>:<Empty title="No exercises found" detail="Try another search or category filter."/>}</>;
}
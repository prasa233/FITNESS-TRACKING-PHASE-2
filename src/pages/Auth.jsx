import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Activity } from "lucide-react";
import api, { getErrorMessage } from "../services/api.js";

export default function Auth({ mode="login" }) {
  const isRegister = mode === "register";
  const [form,setForm] = useState({name:"",email:"",password:""});
  const [error,setError] = useState("");
  const [busy,setBusy] = useState(false);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault(); setError(""); setBusy(true);
    try {
      if (isRegister) {
        await api.post("/auth/register", form);
        setError("Account created. Please sign in.");
        navigate("/login", {replace:true, state:{message:"Account created. Please sign in."}});
      } else {
        const {data} = await api.post("/auth/login", {
          email: form.email, password: form.password
        });
        localStorage.setItem("fittrack_token", data.access_token);
        try {
          const profile = await api.get("/auth/me");
          localStorage.setItem("fittrack_user", JSON.stringify(profile.data));
        } catch {
          localStorage.setItem("fittrack_user", JSON.stringify({email:form.email}));
        }
        navigate("/", {replace:true});
      }
    } catch (err) { setError(getErrorMessage(err)); }
    finally { setBusy(false); }
  };

  return <div className="auth-screen">
    <div className="auth-art">
      <div className="brand auth-brand"><span className="brand-mark"><Activity/></span> FitTrack</div>
      <div className="art-copy"><div className="eyebrow light">YOUR FITNESS JOURNEY</div><h1>Small steps.<br/><em>Stronger you.</em></h1><p>Build healthy habits, celebrate progress, and keep moving forward.</p></div>
      <div className="art-orbit orbit-one"></div><div className="art-orbit orbit-two"></div>
      <div className="art-foot">TRACK YOUR PROGRESS · OWN YOUR PACE</div>
    </div>
    <div className="auth-panel">
      <div className="auth-box">
        <div className="mobile-brand"><Activity/> FitTrack</div>
        <div className="eyebrow">WELCOME {isRegister ? "ABOARD" : "BACK"}</div>
        <h2>{isRegister ? "Create your account" : "Sign in to FitTrack"}</h2>
        <p className="muted">{isRegister ? "Start building a healthier routine today." : "Your next milestone is one workout away."}</p>
        {error && <div className="alert error">{error}</div>}
        <form onSubmit={submit} className="stack-form">
          {isRegister && <label className="field"><span>Full name</span><input required value={form.name} onChange={e=>setForm({...form,name:e.target.value})} placeholder="Your name"/></label>}
          <label className="field"><span>Email address</span><input type="email" required value={form.email} onChange={e=>setForm({...form,email:e.target.value})} placeholder="you@example.com"/></label>
          <label className="field"><span>Password</span><input type="password" required minLength="6" value={form.password} onChange={e=>setForm({...form,password:e.target.value})} placeholder="Enter your password"/></label>
          <button className="btn primary full" disabled={busy}>{busy ? "Please wait..." : isRegister ? "Create account" : "Sign in"}</button>
        </form>
        <p className="auth-switch">{isRegister ? "Already have an account?" : "New to FitTrack?"} <Link to={isRegister ? "/login" : "/register"}>{isRegister ? "Sign in" : "Create an account"}</Link></p>
      </div>
    </div>
  </div>;
}
import { AlertCircle, CheckCircle2, LoaderCircle } from "lucide-react";

export function PageTitle({title, subtitle, action}) {
  return <div className="page-title-row"><div><h2>{title}</h2>{subtitle && <p>{subtitle}</p>}</div>{action}</div>;
}
export function StatCard({label,value,detail,icon:Icon,tone="blue"}) {
  return <div className="stat-card"><div className={`stat-icon ${tone}`}>{Icon && <Icon size={20}/>}</div><div className="stat-label">{label}</div><div className="stat-value">{value ?? "—"}</div>{detail && <div className="stat-detail">{detail}</div>}</div>;
}
export function Loading() { return <div className="loading"><LoaderCircle className="spin"/> Loading your data...</div>; }
export function ErrorMessage({message}) { return message ? <div className="alert error"><AlertCircle size={17}/>{String(message)}</div> : null; }
export function SuccessMessage({message}) { return message ? <div className="alert success"><CheckCircle2 size={17}/>{message}</div> : null; }
export function Empty({title="Nothing here yet",detail="Your data will appear here when available."}) {
  return <div className="empty-state"><div className="empty-icon">✦</div><h3>{title}</h3><p>{detail}</p></div>;
}
export function Field({label, ...props}) {
  return <label className="field"><span>{label}</span><input {...props}/></label>;
}
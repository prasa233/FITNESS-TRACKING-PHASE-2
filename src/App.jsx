import {BrowserRouter,Routes,Route,Navigate} from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Auth from "./pages/Auth.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Workouts from "./pages/Workouts.jsx";
import Plans from "./pages/Plans.jsx";
import Exercises from "./pages/Exercises.jsx";
import Progress from "./pages/Progress.jsx";
import Streaks from "./pages/Streaks.jsx";
import Achievements from "./pages/Achievements.jsx";
import Goals from "./pages/Goals.jsx";
import Notifications from "./pages/Notifications.jsx";
import Profile from "./pages/Profile.jsx";

function Protected({children}) {
  return localStorage.getItem("fittrack_token") ? children : <Navigate to="/login" replace/>;
}
function Shell({children}) {
  return <Protected><Layout>{children}</Layout></Protected>;
}
export default function App(){
 return <BrowserRouter><Routes>
  <Route path="/login" element={<Auth mode="login"/>}/>
  <Route path="/register" element={<Auth mode="register"/>}/>
  <Route path="/" element={<Shell><Dashboard/></Shell>}/>
  <Route
  path="/workouts"
  element={
    <Shell>
      <Workouts />
    </Shell>
  }
/>
  <Route path="/plans" element={<Shell><Plans/></Shell>}/>
  <Route path="/exercises" element={<Shell><Exercises/></Shell>}/>
  <Route path="/progress" element={<Shell><Progress/></Shell>}/>
  <Route path="/streaks" element={<Shell><Streaks/></Shell>}/>
  <Route path="/achievements" element={<Shell><Achievements/></Shell>}/>
  <Route path="/goals" element={<Shell><Goals/></Shell>}/>
  <Route path="/notifications" element={<Shell><Notifications/></Shell>}/>
  <Route path="/profile" element={<Shell><Profile/></Shell>}/>
  <Route path="*" element={<Navigate to="/" replace/>}/>
 </Routes></BrowserRouter>;
}
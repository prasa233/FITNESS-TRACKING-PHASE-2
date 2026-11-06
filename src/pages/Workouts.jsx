import React, { useEffect, useState } from "react";
import api, { getErrorMessage } from "../services/api.js";

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchWorkouts();
  }, []);

  const fetchWorkouts = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/workouts");

      setWorkouts(
        Array.isArray(response.data)
          ? response.data
          : response.data.workouts || []
      );
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <p>Loading workouts...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>Error: {error}</p>;
  }

  return (
    <div>
      <h2>My Workouts</h2>

      {workouts.length === 0 ? (
        <p>No workouts found.</p>
      ) : (
        workouts.map((workout) => (
          <div key={workout.id}>
            <h3>{workout.name || workout.title || "Workout"}</h3>
          </div>
        ))
      )}
    </div>
  );
}

export default Workouts;
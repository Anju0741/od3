import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Home from "./components/Home";
import DiseaseSearch from "./components/Disease";
import Analysis from "./components/Analysis";

export default function App() {
  const token = localStorage.getItem("access_token");

  return (
    <Routes>
      {/* Public routes */}
      <Route
        path="/"
        element={token ? <Navigate to="/home" /> : <Login />}
      />
      <Route
        path="/signup"
        element={token ? <Navigate to="/home" /> : <Signup />}
      />

      {/* Protected routes */}
      <Route
        path="/home"
        element={token ? <Home /> : <Navigate to="/" />}
      />
      <Route
        path="/diseases"
        element={token ? <DiseaseSearch /> : <Navigate to="/" />}
      />
      <Route
        path="/analysis"
        element={token ? <Analysis /> : <Navigate to="/" />}
      />
    </Routes>
  );
}

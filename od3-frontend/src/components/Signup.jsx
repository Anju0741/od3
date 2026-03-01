import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.username || !formData.password || !formData.confirmPassword) {
      setError("Please fill in all fields");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Signup failed");
        return;
      }

      navigate("/");

    } catch {
      setError("Cannot connect to server");
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    if (error) setError("");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-teal-900 via-teal-800 to-slate-900 p-4">
      <div className="w-full max-w-md">
        <form onSubmit={handleSubmit} className="space-y-6">

          <h1 className="text-center text-white uppercase tracking-wider mb-8">
            Sign Up
          </h1>

          {error && (
            <div className="text-center text-red-400 bg-red-900/30 px-4 py-3 rounded-full">
              {error}
            </div>
          )}

          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleInputChange}
            className="w-full h-14 px-6 bg-slate-600/50 text-white rounded-full"
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleInputChange}
            className="w-full h-14 px-6 bg-slate-600/50 text-white rounded-full"
            required
          />

          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            value={formData.confirmPassword}
            onChange={handleInputChange}
            className="w-full h-14 px-6 bg-slate-600/50 text-white rounded-full"
            required
          />

          <button
            type="submit"
            className="w-full h-14 bg-white text-slate-900 rounded-full uppercase tracking-wide"
          >
            Sign Up
          </button>

          <div className="text-center">
            <button
              type="button"
              onClick={() => navigate("/")}
              className="text-white/80 hover:text-white underline"
            >
              Already have an account? Login
            </button>
          </div>

        </form>
      </div>
    </div>
  );
}

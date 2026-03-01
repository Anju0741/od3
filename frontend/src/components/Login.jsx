import { useState } from 'react';
import { useNavigate } from "react-router-dom";


export default function Login() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [error, setError] = useState(''); // We'll now USE this value

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.username || !formData.password) {
      setError('Please fill in all fields');
      return;
    }

    setError('');

    try {
      const res = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || 'Login failed');
        return;
      }

      // Store real JWT
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('username', formData.username);

      window.location.href = "/home";




    } catch {
      setError('Cannot connect to server');
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Optional: clear error when user starts typing
    if (error) setError('');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-teal-900 via-teal-800 to-slate-900 p-4">
      <div className="w-full max-w-md">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <h1 className="text-center text-white uppercase tracking-wider mb-8">
            User Login
          </h1>

          {/* Error Message */}
          {error && (
            <div className="text-center text-red-400 bg-red-900/30 px-4 py-3 rounded-full">
              {error}
            </div>
          )}

          {/* Username Input */}
          <div className="relative flex items-center">
            <div className="absolute left-0 w-14 h-14 bg-white rounded-full flex items-center justify-center z-10">
              <svg className="w-6 h-6 text-slate-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            </div>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleInputChange}
              className="w-full h-14 pl-16 pr-4 bg-slate-600/50 text-white placeholder:text-slate-400 rounded-full focus:outline-none focus:ring-2 focus:ring-white/30"
              required
            />
          </div>

          {/* Password Input */}
          <div className="relative flex items-center">
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleInputChange}
              className="w-full h-14 pl-4 pr-16 bg-slate-600/50 text-white placeholder:text-slate-400 rounded-full focus:outline-none focus:ring-2 focus:ring-white/30"
              required
            />
            <div className="absolute right-0 w-14 h-14 bg-white rounded-full flex items-center justify-center z-10">
              <svg className="w-5 h-5 text-slate-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full h-14 bg-white text-slate-900 rounded-full uppercase tracking-wide hover:bg-slate-100 transition-colors mt-8"
          >
            Login
          </button>

          {/* Toggle to Sign Up */}
          <div className="text-center">
            <button
              type="button"
              onClick={() => navigate("/signup")}
              className="text-white/80 hover:text-white underline"
            >
            Don't have an account? Sign Up
            </button>

          </div>
        </form>
      </div>
    </div>
  );
}
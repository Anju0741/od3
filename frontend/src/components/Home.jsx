import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { predictDrugs } from "../services/api";

function Home() {
  const navigate = useNavigate();

  const username = localStorage.getItem("username") || "Researcher";

  const [disease, setDisease] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
    window.location.reload();
  };

  const handleStartAnalysis = async () => {
    if (!disease.trim()) {
      alert("Please enter an orphan disease name");
      return;
    }

    setLoading(true);

    try {
      const result = await predictDrugs(disease);
      console.log("API Result:", result);

      // Navigate to analysis page with API data
      navigate("/analysis", { state: result });
    } catch (err) {
      console.error(err);
      alert("Error running analysis");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-teal-900 via-teal-800 to-slate-900 text-white flex flex-col">
      {/* Header */}
      <header className="bg-white/5 backdrop-blur-lg border-b border-white/10 px-8 py-5 flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-wider">OD3</h1>

        <div className="flex items-center gap-6">
          <div className="text-right">
            <p className="text-sm text-white/80">Logged in as</p>
            <p className="font-semibold">{username}</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-full backdrop-blur transition font-medium"
          >
            Logout
          </button>
        </div>
      </header>

      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-64 bg-white/5 backdrop-blur-lg border-r border-white/10">
          <nav className="p-6">
            <ul className="space-y-2">
              <li>
                <button className="w-full text-left py-3 px-4 rounded-lg bg-white/10 font-medium">
                  Dashboard
                </button>
              </li>
              <li>
                <button className="w-full text-left py-3 px-4 rounded-lg hover:bg-white/10 transition">
                  Drug Analysis
                </button>
              </li>
              <li>
                <button
                  onClick={() => navigate("/diseases")}
                  className="w-full text-left py-3 px-4 rounded-lg hover:bg-white/10 transition"
                >
                  Disease Explorer
                </button>
              </li>
            </ul>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-12">
          {/* Hero Section */}
          <section className="text-center mb-20">
            <h2 className="text-5xl font-bold mb-6">
              AI-powered Drug Repurposing for Orphan Diseases
            </h2>

            <p className="text-xl text-white/80 max-w-4xl mx-auto mb-10">
              Analyze molecular structures and genomic signals to identify
              high-potential repurposable drugs.
            </p>

            {/* Disease Input */}
            <input
              type="text"
              placeholder="Enter orphan disease (e.g., Farber disease)"
              value={disease}
              onChange={(e) => setDisease(e.target.value)}
              className="w-full max-w-xl px-6 py-4 rounded-full text-black text-lg mb-8"
            />

            <div className="flex justify-center">
              <button
                onClick={handleStartAnalysis}
                disabled={loading}
                className="px-20 py-6 bg-white text-teal-900 rounded-full font-bold text-xl hover:bg-gray-100 transition disabled:opacity-50"
              >
                {loading ? "Analyzing..." : "Start Analysis"}
              </button>
            </div>
          </section>

          {/* Feature Cards */}
          <section className="mb-20">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto">
              <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
                <h3 className="text-2xl font-semibold mb-4">
                  Molecular Graph Analysis
                </h3>
                <p className="text-white/80">
                  SMILES → Graph conversion
                  <br />
                  GNN-based structure inference
                </p>
              </div>

              <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
                <h3 className="text-2xl font-semibold mb-4">
                  Disease Target Matching
                </h3>
                <p className="text-white/80">
                  Genomic signature alignment
                  <br />
                  Rare disease focus
                </p>
              </div>

              <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
                <h3 className="text-2xl font-semibold mb-4">
                  Explainable AI
                </h3>
                <p className="text-white/80">
                  Model reasoning
                  <br />
                  Feature importance
                </p>
              </div>

              <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
                <h3 className="text-2xl font-semibold mb-4">
                  Performance Metrics
                </h3>
                <p className="text-white/80">
                  Confidence scores
                  <br />
                  Ranking & validation
                </p>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}

export default Home;

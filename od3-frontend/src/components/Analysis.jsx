import { useState } from "react";

export default function Analysis() {
  const [disease, setDisease] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const runAnalysis = async () => {
    if (!disease.trim()) {
      setError("Please enter a disease name");
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          disease_name: disease,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError("Prediction failed");
        return;
      }

      setResults(data.top_drugs);
    } catch {
      setError("Backend not reachable");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-teal-900 via-teal-800 to-slate-900 text-white p-12">
      <h1 className="text-4xl font-bold text-center mb-12">
        Drug Repurposing Analysis
      </h1>

      {/* Input */}
      <div className="max-w-2xl mx-auto">
        <input
          type="text"
          value={disease}
          onChange={(e) => setDisease(e.target.value)}
          placeholder="Enter disease name (e.g. Farber disease)"
          className="w-full px-6 py-4 rounded-full bg-white/20 outline-none"
        />

        <button
          onClick={runAnalysis}
          className="mt-6 w-full py-4 bg-white text-teal-900 rounded-full font-semibold hover:bg-gray-100 transition"
        >
          {loading ? "Running Analysis..." : "Run Analysis"}
        </button>

        {error && (
          <p className="mt-4 text-center text-red-400">{error}</p>
        )}
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="mt-16 max-w-5xl mx-auto bg-white/10 border border-white/20 rounded-2xl p-8">
          <h2 className="text-2xl font-semibold mb-6">
            Top Drug Candidates
          </h2>

          <table className="w-full">
            <thead>
              <tr className="border-b border-white/20">
                <th className="py-2">Rank</th>
                <th className="py-2">SMILES</th>
                <th className="py-2">Affinity Score</th>
              </tr>
            </thead>
            <tbody>
              {results.map((drug, idx) => (
                <tr key={idx} className="border-b border-white/10">
                  <td className="py-2">{idx + 1}</td>
                  <td className="py-2 font-mono text-sm break-all">
                    {drug.smiles}
                  </td>
                  <td className="py-2">{drug.score.toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
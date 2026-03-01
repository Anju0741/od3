import { useState } from "react";
import { predictDrugs } from "../services/api";

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

  try {                                                                                                           `                                                                                                                                                                                                                                    `
    const data = await predictDrugs(disease);
    console.log("API RESPONSE:", data);

    setResults(data.top_drugs);
  } catch (err) {
  console.error("FULL ERROR:", err);
  setError(err.message || "Error in running analysis");


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
          placeholder="Enter orphan disease (e.g. Farber disease)"
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
        <div className="mt-16 max-w-6xl mx-auto bg-white/10 border border-white/20 rounded-2xl p-8">
          <h2 className="text-2xl font-semibold mb-6">
            Top 10 Ranked Drug Candidates
          </h2>

          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/20">
                <th className="py-3">Rank</th>
                <th className="py-3">SMILES</th>
                <th className="py-3">Score</th>
              </tr>
            </thead>
            <tbody>
              {results.map((drug, idx) => {

  // 🔹 Convert score (0–5) → percentage
  const confidence = Math.round((drug.score / 5) * 100);

  // 🔹 Rank badge logic
  let badge = null;
  if (idx === 0) badge = "🥇 Top-1";
  else if (idx < 3) badge = "🥈 Top-3";
  else if (idx < 5) badge = "🥉 Top-5";

  // 🔹 Confidence bar color
  const barColor =
    confidence >= 75 ? "bg-green-400"
    : confidence >= 50 ? "bg-yellow-400"
    : "bg-red-400";

  return (
    <tr key={idx} className="border-b border-white/10">
      <td className="py-2">
  <div className="font-semibold">{idx + 1}</div>
  {badge && (
    <div className="text-xs text-teal-300 mt-1">
      {badge}
    </div>
  )}
</td>


      <td className="py-2 font-mono text-sm break-all">
        {drug.smiles}
      </td>

      <td className="py-2">
  {/* 🔹 Score + Confidence */}
  <div className="flex justify-between text-xs text-white/80 mb-1">
    <span>Score: {drug.score.toFixed(4)}</span>
    <span>{confidence}%</span>
  </div>

  {/* 🔹 Confidence bar */}
  <div className="w-full bg-white/20 rounded-full h-3">
    <div
      className={`${barColor} h-3 rounded-full transition-all duration-500`}
      style={{ width: `${confidence}%` }}
      title={
        confidence >= 75
          ? "High binding likelihood"
          : confidence >= 50
          ? "Moderate binding likelihood"
          : "Low binding likelihood"
      }
    />
  </div>

  {/* 🔹 Explanation text */}
  <p className="text-xs mt-2 text-white/70">
    {confidence >= 75 &&
      "Strong predicted interaction with disease-associated targets."}
    {confidence >= 50 && confidence < 75 &&
      "Moderate interaction; potential repurposing candidate."}
    {confidence < 50 &&
      "Lower interaction confidence; exploratory candidate."}
  </p>
</td>

      
    </tr>
  );
})}

            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

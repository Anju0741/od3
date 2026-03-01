export default function DiseaseSearch() {
  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-start
      bg-linear-to-br from-[#0b3d3a] via-[#0f5c55] to-[#083b38] text-white
      relative overflow-hidden">

      {/* subtle particle effect */}
      <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_20%_30%,rgba(255,255,255,0.15),transparent_40%),radial-gradient(circle_at_80%_70%,rgba(255,255,255,0.1),transparent_40%)]" />

      {/* Title */}
      <h1 className="mt-24 text-3xl tracking-widest font-light z-10">
        DISEASE SEARCH
      </h1>

      {/* Search Bar */}
      <div className="mt-10 w-full max-w-2xl z-10">
        <div className="flex items-center gap-4 px-6 py-4 rounded-full
          bg-white/15 border border-white/20">
          <span className="text-xl opacity-80">🔍</span>
          <input
            type="text"
            placeholder="Search disease..."
            className="bg-transparent w-full outline-none placeholder-white/60"
          />
        </div>
      </div>

      {/* Disease Card */}
      <div className="mt-14 w-full max-w-3xl z-10
        bg-white/12 border border-white/20 rounded-2xl p-6">

        <h2 className="text-xl font-semibold mb-3">
          Alzheimer&apos;s Disease <span className="text-sm opacity-70">(ORPHA:58)</span>
        </h2>

        <p className="text-white/80 leading-relaxed">
          A neurodegenerative disorder characterized by progressive cognitive
          decline, memory loss, and behavioral changes.
        </p>
      </div>

      {/* Info Cards */}
      <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-6
        w-full max-w-4xl z-10">

        {/* Prevalence */}
        <div className="bg-white/12 border border-white/20 rounded-2xl p-5">
          <h3 className="font-semibold mb-2">👥 Prevalence</h3>
          <p className="text-white/80 text-sm">
            1–5 per 1,000 people<br />over age 60
          </p>
        </div>

        {/* Genes */}
        <div className="bg-white/12 border border-white/20 rounded-2xl p-5">
          <h3 className="font-semibold mb-3">🧬 Genes Involved</h3>
          <div className="flex gap-2 flex-wrap">
            {["APP", "PSEN1", "PSEN2"].map(gene => (
              <span
                key={gene}
                className="px-3 py-1 rounded-full text-sm
                bg-emerald-600/40 border border-emerald-400/40">
                {gene}
              </span>
            ))}
          </div>
        </div>

        {/* Treatments */}
        <div className="bg-white/12 border border-white/20 rounded-2xl p-5">
          <h3 className="font-semibold mb-2">💊 Known Treatments</h3>
          <ul className="text-white/80 text-sm space-y-1">
            <li>• Donepezil</li>
            <li>• Memantine</li>
            <li>• Rivastigmine</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
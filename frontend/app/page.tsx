export default function Home() {
  return (
    <div className="max-w-5xl mx-auto">
      <section className="mt-8 iridescent-border rounded-[18px]">
        <div className="glass rounded-[18px] p-8">
          <h1 className="text-4xl font-semibold tracking-tight">
            Know your patterns. Keep your agency.
          </h1>
          <p className="mt-4 text-white/80 leading-relaxed max-w-2xl">
            Insight Atlas turns your short survey + free-text into an explainable style report.
            Built for consent, privacy, and grounded language—no diagnoses, no gimmicks.
          </p>
          <div className="mt-6 flex gap-3">
            <a href="/app" className="px-4 py-2 rounded-xl bg-white text-black font-medium">Open the App</a>
            <a href="/about" className="px-4 py-2 rounded-xl border border-white/20 hover:border-white/40">How it works</a>
          </div>
        </div>
      </section>

      <section className="mt-10 grid md:grid-cols-3 gap-4">
        {[
          ["Consent-first", "Explicit consent gate and data purge controls."],
          ["Explainable", "Features → scores → narrative, visible to the user."],
          ["Offline-capable", "Deterministic engine works without an LLM."],
        ].map(([t, d]) => (
          <div key={t} className="glass rounded-2xl p-5">
            <div className="font-medium">{t}</div>
            <div className="text-sm text-white/75 mt-1">{d}</div>
          </div>
        ))}
      </section>
    </div>
  );
}

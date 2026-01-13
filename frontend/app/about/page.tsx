export default function About() {
  return (
    <div className="max-w-3xl mx-auto">
      <div className="glass rounded-2xl p-6">
        <h2 className="text-2xl font-semibold">How it works</h2>
        <ol className="mt-4 space-y-3 text-white/80 leading-relaxed list-decimal list-inside">
          <li>You provide explicit consent.</li>
          <li>You fill a short survey and (optionally) free-text.</li>
          <li>The engine extracts simple features (e.g., intensifier rate, technical lexicon rate).</li>
          <li>Those features map to trait proxies and style signals.</li>
          <li>You receive a report with explainability and suggestions.</li>
        </ol>
        <p className="mt-4 text-white/70 text-sm">
          The system does not diagnose autism/ADHD or any medical condition.
        </p>
      </div>
    </div>
  );
}

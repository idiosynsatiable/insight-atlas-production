import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Insight Atlas - Understand Yourself Through Explainable AI",
  description: "A consent-first platform for self-understanding. Get explainable insights into your cognitive patterns, communication style, and personal strengths. Privacy-focused, not a diagnostic tool.",
};

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto">
      <section className="text-center py-20">
        <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          Understand Yourself Better
        </h1>
        <p className="text-xl md:text-2xl text-white/80 mb-8 max-w-3xl mx-auto">
          A consent-first self-reflection platform that helps you explore your cognitive patterns and communication style through explainable AI analysis.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/app"
            className="px-8 py-4 rounded-xl bg-blue-500 hover:bg-blue-600 transition-colors font-semibold text-lg"
          >
            Get Started Free
          </Link>
          <Link
            href="/pricing"
            className="px-8 py-4 rounded-xl border-2 border-white/20 hover:border-white/40 transition-colors font-semibold text-lg"
          >
            View Pricing
          </Link>
        </div>
      </section>

      <section className="py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Why Insight Atlas?</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <article className="glass rounded-2xl p-8">
            <div className="text-4xl mb-4">🔒</div>
            <h3 className="text-xl font-semibold mb-3">Consent-First</h3>
            <p className="text-white/75">
              Explicit consent gates and full data control. Your information, your choice. Export or delete anytime.
            </p>
          </article>

          <article className="glass rounded-2xl p-8">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold mb-3">Explainable AI</h3>
            <p className="text-white/75">
              See exactly how your inputs map to insights. Features → scores → narrative. Complete transparency in every analysis.
            </p>
          </article>

          <article className="glass rounded-2xl p-8">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold mb-3">Not a Diagnosis</h3>
            <p className="text-white/75">
              A self-reflection aid, not a medical tool. We provide hypotheses and suggestions, never diagnostic claims.
            </p>
          </article>
        </div>
      </section>

      <section className="py-16">
        <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid md:grid-cols-4 gap-6">
          <div className="glass rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-blue-400 mb-3">1</div>
            <h3 className="font-semibold mb-2">Create Account</h3>
            <p className="text-sm text-white/70">Sign up in seconds with just email and password</p>
          </div>

          <div className="glass rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-blue-400 mb-3">2</div>
            <h3 className="font-semibold mb-2">Complete Survey</h3>
            <p className="text-sm text-white/70">Answer quick questions about your preferences and style</p>
          </div>

          <div className="glass rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-blue-400 mb-3">3</div>
            <h3 className="font-semibold mb-2">Get Analysis</h3>
            <p className="text-sm text-white/70">Receive explainable insights with full transparency</p>
          </div>

          <div className="glass rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-blue-400 mb-3">4</div>
            <h3 className="font-semibold mb-2">Take Action</h3>
            <p className="text-sm text-white/70">Use insights to improve communication and self-awareness</p>
          </div>
        </div>
      </section>

      <section className="py-16 text-center">
        <div className="glass rounded-2xl p-12 max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">Ready to Begin?</h2>
          <p className="text-white/75 mb-8 text-lg">
            Start your self-understanding journey today. Free tier available, upgrade anytime for advanced features.
          </p>
          <Link
            href="/app"
            className="inline-block px-8 py-4 rounded-xl bg-blue-500 hover:bg-blue-600 transition-colors font-semibold text-lg"
          >
            Start Free Now
          </Link>
        </div>
      </section>

      <section className="py-8 text-center text-sm text-white/60">
        <p>
          <strong>Disclaimer:</strong> Insight Atlas is a self-reflection tool, not a medical or psychological diagnostic service. 
          For health concerns, please consult qualified professionals.
        </p>
      </section>
    </div>
  );
}

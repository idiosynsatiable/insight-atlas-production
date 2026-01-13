"use client";
import { useState, useEffect } from "react";
import { api } from "../lib/api";
import Link from "next/link";

type MeOut = { email: string; plan: string; status: string };

export default function Billing() {
  const [token, setToken] = useState("");
  const [me, setMe] = useState<MeOut | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Try to load token from localStorage
    const stored = localStorage.getItem("atlas_token");
    if (stored) {
      setToken(stored);
      loadMe(stored);
    }
  }, []);

  async function loadMe(tkn: string) {
    try {
      const data = await api<MeOut>("/me", { method: "GET" }, tkn);
      setMe(data);
    } catch (e: any) {
      setMsg(`Error loading account: ${e.message}`);
    }
  }

  async function saveToken() {
    if (!token) return;
    localStorage.setItem("atlas_token", token);
    await loadMe(token);
  }

  async function upgrade(plan: "monthly" | "yearly") {
    setMsg(null);
    setLoading(true);
    try {
      const out = await api<any>(`/billing/checkout?plan=${plan}`, { method: "POST" }, token);
      if (out.url) {
        // Redirect to Stripe Checkout
        window.location.href = out.url;
      } else if (out.mode === "demo") {
        // Demo mode: plan upgraded in DB
        setMsg(`✓ Demo upgrade successful! Plan: ${out.plan}`);
        await loadMe(token);
      } else {
        setMsg(JSON.stringify(out, null, 2));
      }
    } catch (e: any) {
      setMsg(`Error: ${e.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="glass rounded-2xl p-8">
        <h1 className="text-3xl font-bold">Billing & Subscription</h1>
        <p className="mt-2 text-white/75">
          Manage your subscription and upgrade to Pro for full access.
        </p>

        {!me && (
          <div className="mt-6">
            <div className="text-sm text-white/70 mb-2">Paste your JWT token to continue</div>
            <div className="flex gap-2">
              <input
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                className="flex-1 px-4 py-2 rounded-xl bg-white/5 border border-white/10 focus:border-white/30 outline-none"
              />
              <button
                onClick={saveToken}
                className="px-6 py-2 rounded-xl bg-white text-black font-medium hover:bg-white/90 transition-colors"
              >
                Load Account
              </button>
            </div>
            <p className="mt-2 text-xs text-white/60">
              Get your token from the <Link href="/app" className="text-blue-400 hover:underline">App page</Link> after logging in.
            </p>
          </div>
        )}

        {me && (
          <div className="mt-6 space-y-6">
            <div className="glass rounded-xl p-5">
              <div className="text-sm text-white/60 mb-1">Account</div>
              <div className="font-medium">{me.email}</div>
              <div className="mt-3 flex items-center gap-3">
                <div className="text-sm text-white/60">Plan:</div>
                <div className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-sm font-medium">
                  {me.plan.toUpperCase()}
                </div>
                <div className="text-sm text-white/60">Status:</div>
                <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                  me.status === "active" ? "bg-green-500/20 text-green-300" : "bg-red-500/20 text-red-300"
                }`}>
                  {me.status.toUpperCase()}
                </div>
              </div>
            </div>

            {me.plan === "free" && (
              <div className="glass rounded-xl p-6">
                <h3 className="text-xl font-semibold mb-4">Upgrade to Pro</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="border border-white/10 rounded-xl p-5">
                    <div className="text-lg font-bold">Pro Monthly</div>
                    <div className="mt-2 flex items-baseline gap-2">
                      <span className="text-3xl font-bold">$19</span>
                      <span className="text-white/60">/month</span>
                    </div>
                    <ul className="mt-4 space-y-2 text-sm text-white/80">
                      <li>✓ Unlimited sessions</li>
                      <li>✓ LLM narrative polish</li>
                      <li>✓ Export & data control</li>
                    </ul>
                    <button
                      onClick={() => upgrade("monthly")}
                      disabled={loading}
                      className="mt-4 w-full px-4 py-3 rounded-xl bg-blue-500 hover:bg-blue-600 transition-colors font-medium text-white disabled:opacity-50"
                    >
                      {loading ? "Processing..." : "Upgrade Monthly"}
                    </button>
                  </div>

                  <div className="border-2 border-blue-400/50 rounded-xl p-5 relative">
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-green-500 text-white text-xs font-semibold rounded-full">
                      SAVE 17%
                    </div>
                    <div className="text-lg font-bold">Pro Yearly</div>
                    <div className="mt-2 flex items-baseline gap-2">
                      <span className="text-3xl font-bold">$190</span>
                      <span className="text-white/60">/year</span>
                    </div>
                    <div className="mt-1 text-sm text-green-400">Save $38 per year</div>
                    <ul className="mt-4 space-y-2 text-sm text-white/80">
                      <li>✓ Everything in Monthly</li>
                      <li>✓ 17% discount</li>
                      <li>✓ Early access to features</li>
                    </ul>
                    <button
                      onClick={() => upgrade("yearly")}
                      disabled={loading}
                      className="mt-4 w-full px-4 py-3 rounded-xl bg-blue-500 hover:bg-blue-600 transition-colors font-medium text-white disabled:opacity-50"
                    >
                      {loading ? "Processing..." : "Upgrade Yearly"}
                    </button>
                  </div>
                </div>
              </div>
            )}

            {me.plan.startsWith("pro") && (
              <div className="glass rounded-xl p-6 border border-green-500/30">
                <h3 className="text-xl font-semibold text-green-400">✓ You're on Pro</h3>
                <p className="mt-2 text-white/75">
                  You have full access to all features. Thank you for supporting Insight Atlas!
                </p>
                <div className="mt-4 text-sm text-white/60">
                  To manage your subscription, visit your Stripe customer portal (link sent via email).
                </div>
              </div>
            )}
          </div>
        )}

        {msg && (
          <div className="mt-6 p-4 rounded-xl bg-white/5 border border-white/10">
            <pre className="text-xs text-white/80 whitespace-pre-wrap">{msg}</pre>
          </div>
        )}
      </div>

      <div className="mt-6 text-center text-sm text-white/60">
        <Link href="/pricing" className="text-blue-400 hover:underline">View all pricing plans</Link>
        {" · "}
        <Link href="/app" className="text-blue-400 hover:underline">Back to App</Link>
      </div>
    </div>
  );
}

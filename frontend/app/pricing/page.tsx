"use client";
import Link from "next/link";

export default function Pricing() {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Simple, Transparent Pricing</h1>
        <p className="text-white/75 text-lg max-w-2xl mx-auto">
          Choose the plan that fits your self-understanding journey. No hidden fees, cancel anytime.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Free Tier */}
        <div className="glass rounded-2xl p-8 border border-white/10">
          <div className="text-sm text-white/60 font-medium uppercase tracking-wide">Free</div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-4xl font-bold">$0</span>
            <span className="text-white/60">/month</span>
          </div>
          <p className="mt-4 text-white/75 text-sm">
            Explore the platform with limited access.
          </p>
          <ul className="mt-6 space-y-3 text-sm text-white/80">
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>Account creation</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>View demo reports</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-white/30">✗</span>
              <span className="text-white/50">Create sessions</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-white/30">✗</span>
              <span className="text-white/50">Generate reports</span>
            </li>
          </ul>
          <Link href="/app" className="mt-8 block w-full px-4 py-3 text-center rounded-xl border border-white/20 hover:border-white/40 transition-colors font-medium">
            Get Started
          </Link>
        </div>

        {/* Pro Monthly */}
        <div className="glass rounded-2xl p-8 border-2 border-blue-400/50 relative">
          <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-blue-500 text-white text-xs font-semibold rounded-full">
            POPULAR
          </div>
          <div className="text-sm text-blue-400 font-medium uppercase tracking-wide">Pro Monthly</div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-4xl font-bold">$19</span>
            <span className="text-white/60">/month</span>
          </div>
          <p className="mt-4 text-white/75 text-sm">
            Full access with monthly flexibility.
          </p>
          <ul className="mt-6 space-y-3 text-sm text-white/80">
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>Unlimited sessions</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>Explainable reports</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>LLM narrative polish</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>Export & data control</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>Priority support</span>
            </li>
          </ul>
          <Link href="/billing" className="mt-8 block w-full px-4 py-3 text-center rounded-xl bg-blue-500 hover:bg-blue-600 transition-colors font-medium text-white">
            Upgrade to Pro
          </Link>
        </div>

        {/* Pro Yearly */}
        <div className="glass rounded-2xl p-8 border border-white/10">
          <div className="text-sm text-white/60 font-medium uppercase tracking-wide">Pro Yearly</div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-4xl font-bold">$190</span>
            <span className="text-white/60">/year</span>
          </div>
          <div className="mt-2 text-sm text-green-400 font-medium">
            Save $38 (17% off)
          </div>
          <p className="mt-4 text-white/75 text-sm">
            Best value for committed users.
          </p>
          <ul className="mt-6 space-y-3 text-sm text-white/80">
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>Everything in Pro Monthly</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>17% discount</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>Annual billing</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-400">✓</span>
              <span>Early access to features</span>
            </li>
          </ul>
          <Link href="/billing" className="mt-8 block w-full px-4 py-3 text-center rounded-xl border border-white/20 hover:border-white/40 transition-colors font-medium">
            Upgrade to Pro Yearly
          </Link>
        </div>
      </div>

      <div className="mt-12 text-center text-sm text-white/60">
        <p>All plans include data export and deletion controls.</p>
        <p className="mt-2">Questions? <a href="mailto:support@insightatlas.example" className="text-blue-400 hover:underline">Contact us</a></p>
      </div>
    </div>
  );
}

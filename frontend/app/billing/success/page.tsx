"use client";
import Link from "next/link";

export default function BillingSuccess() {
  return (
    <div className="max-w-2xl mx-auto text-center">
      <div className="glass rounded-2xl p-12">
        <div className="text-6xl mb-6">🎉</div>
        <h1 className="text-3xl font-bold mb-4">Welcome to Pro!</h1>
        <p className="text-white/75 text-lg mb-8">
          Your subscription is now active. You have full access to all Insight Atlas features.
        </p>
        <div className="space-y-3">
          <Link
            href="/app"
            className="block px-6 py-3 rounded-xl bg-blue-500 hover:bg-blue-600 transition-colors font-medium text-white"
          >
            Start Creating Sessions
          </Link>
          <Link
            href="/billing"
            className="block px-6 py-3 rounded-xl border border-white/20 hover:border-white/40 transition-colors font-medium"
          >
            View Billing Details
          </Link>
        </div>
        <p className="mt-8 text-sm text-white/60">
          A confirmation email has been sent to your inbox.
        </p>
      </div>
    </div>
  );
}

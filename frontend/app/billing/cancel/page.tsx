"use client";
import Link from "next/link";

export default function BillingCancel() {
  return (
    <div className="max-w-2xl mx-auto text-center">
      <div className="glass rounded-2xl p-12">
        <div className="text-6xl mb-6">😔</div>
        <h1 className="text-3xl font-bold mb-4">Checkout Canceled</h1>
        <p className="text-white/75 text-lg mb-8">
          Your subscription was not activated. No charges have been made.
        </p>
        <div className="space-y-3">
          <Link
            href="/billing"
            className="block px-6 py-3 rounded-xl bg-blue-500 hover:bg-blue-600 transition-colors font-medium text-white"
          >
            Try Again
          </Link>
          <Link
            href="/pricing"
            className="block px-6 py-3 rounded-xl border border-white/20 hover:border-white/40 transition-colors font-medium"
          >
            View Pricing
          </Link>
        </div>
        <p className="mt-8 text-sm text-white/60">
          Questions? <a href="mailto:support@insightatlas.example" className="text-blue-400 hover:underline">Contact support</a>
        </p>
      </div>
    </div>
  );
}

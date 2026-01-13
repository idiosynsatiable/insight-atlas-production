import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Insight Atlas",
  description: "Consent-first self-understanding portal",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen">
          <header className="px-6 py-5">
            <div className="max-w-5xl mx-auto flex items-center justify-between">
              <a href="/" className="font-semibold tracking-tight text-lg">Insight Atlas</a>
              <nav className="flex gap-4 text-sm opacity-90">
                <a className="hover:opacity-100 opacity-80" href="/app">App</a>
                <a className="hover:opacity-100 opacity-80" href="/pricing">Pricing</a>
                <a className="hover:opacity-100 opacity-80" href="/billing">Billing</a>
              </nav>
            </div>
          </header>
          <main className="px-6 pb-16">{children}</main>
          <footer className="px-6 py-10 opacity-70 text-xs">
            <div className="max-w-5xl mx-auto">
              Self-reflection aid only. Not a diagnostic tool.
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}

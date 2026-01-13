import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Insight Atlas - Consent-First Self-Understanding Platform",
  description: "Discover your cognitive patterns and communication style with explainable AI analysis. Consent-first, privacy-focused self-reflection tool. Not a diagnostic tool.",
  keywords: ["self-understanding", "cognitive analysis", "communication style", "personality insights", "explainable AI", "self-reflection", "personal development"],
  authors: [{ name: "Insight Atlas Team" }],
  creator: "Insight Atlas",
  publisher: "Insight Atlas",
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://insight-atlas.vercel.app",
    title: "Insight Atlas - Consent-First Self-Understanding Platform",
    description: "Discover your cognitive patterns and communication style with explainable AI analysis. Privacy-focused self-reflection tool.",
    siteName: "Insight Atlas",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Insight Atlas - Self-Understanding Platform",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Insight Atlas - Consent-First Self-Understanding Platform",
    description: "Discover your cognitive patterns and communication style with explainable AI analysis.",
    images: ["/og-image.png"],
    creator: "@insightatlas",
  },
  verification: {
    google: "your-google-verification-code",
  },
  alternates: {
    canonical: "https://insight-atlas.vercel.app",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="manifest" href="/site.webmanifest" />
        <meta name="theme-color" content="#000000" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebApplication",
              "name": "Insight Atlas",
              "description": "Consent-first self-understanding platform with explainable AI analysis",
              "url": "https://insight-atlas.vercel.app",
              "applicationCategory": "HealthApplication",
              "operatingSystem": "Any",
              "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
              },
              "featureList": [
                "Explainable AI analysis",
                "Privacy-focused design",
                "Consent-first approach",
                "Cognitive pattern insights",
                "Communication style analysis"
              ]
            })
          }}
        />
      </head>
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

"use client";
import { useMemo, useState } from "react";
import { api } from "../lib/api";

type TokenOut = { access_token: string };
type IntakeOut = { session_id: number };
type ReportOut = { report_id: number; session_id: number; result: any };

function Input({label, ...props}: any) {
  return (
    <label className="block">
      <div className="text-xs text-white/70 mb-1">{label}</div>
      <input {...props} className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 focus:border-white/30 outline-none" />
    </label>
  );
}
function Select({label, children, ...props}: any) {
  return (
    <label className="block">
      <div className="text-xs text-white/70 mb-1">{label}</div>
      <select {...props} className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 focus:border-white/30 outline-none">
        {children}
      </select>
    </label>
  );
}

export default function AppPage() {
  const [mode, setMode] = useState<"login"|"register">("register");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);

  const [consent, setConsent] = useState(false);
  const [freeText, setFreeText] = useState("");
  const [survey, setSurvey] = useState({
    novelty_seeking: 3,
    structure_preference: 3,
    social_energy: 3,
    sensory_sensitivity: 3,
    hyperfocus: 3
  });

  const [sessionId, setSessionId] = useState<number | null>(null);
  const [report, setReport] = useState<ReportOut | null>(null);
  const [err, setErr] = useState<string | null>(null);

  async function auth() {
    setErr(null);
    try {
      const path = mode === "register" ? "/auth/register" : "/auth/login";
      const out = await api<TokenOut>(path, { method: "POST", body: JSON.stringify({ email, password }) });
      setToken(out.access_token);
    } catch (e: any) {
      setErr(e.message);
    }
  }

  async function submitIntake() {
    setErr(null);
    setReport(null);
    try {
      const out = await api<IntakeOut>("/intake", { method: "POST", body: JSON.stringify({ consent, survey, free_text: freeText }) }, token || undefined);
      setSessionId(out.session_id);
    } catch (e:any) { setErr(e.message); }
  }

  async function runAnalysis() {
    setErr(null);
    try {
      if (!sessionId) return;
      const out = await api<ReportOut>(`/analyze/${sessionId}`, { method: "POST" }, token || undefined);
      setReport(out);
    } catch (e:any) { setErr(e.message); }
  }

  return (
    <div className="max-w-5xl mx-auto grid lg:grid-cols-2 gap-5">
      <div className="glass rounded-2xl p-6">
        <h2 className="text-xl font-semibold">1) Account</h2>
        <div className="mt-4 flex gap-2">
          <button onClick={() => setMode("register")} className={`px-3 py-1.5 rounded-xl border ${mode==="register"?"border-white/40":"border-white/10"}`}>Register</button>
          <button onClick={() => setMode("login")} className={`px-3 py-1.5 rounded-xl border ${mode==="login"?"border-white/40":"border-white/10"}`}>Login</button>
        </div>
        <div className="mt-4 grid gap-3">
          <Input label="Email" value={email} onChange={(e:any)=>setEmail(e.target.value)} />
          <Input label="Password" type="password" value={password} onChange={(e:any)=>setPassword(e.target.value)} />
          <button onClick={auth} className="px-4 py-2 rounded-xl bg-white text-black font-medium">Continue</button>
          {token && <div className="text-xs text-white/70">Token set. You’re in.</div>}
          {err && <div className="text-xs text-red-200 whitespace-pre-wrap">{err}</div>}
        </div>
      </div>

      <div className="glass rounded-2xl p-6">
        <h2 className="text-xl font-semibold">2) Intake</h2>
        <div className="mt-4 grid grid-cols-2 gap-3">
          {Object.entries(survey).map(([k,v]) => (
            <Select
              key={k}
              label={k.replace(/_/g," ")}
              value={v}
              onChange={(e:any)=>setSurvey(prev=>({ ...prev, [k]: parseInt(e.target.value,10) }))}
            >
              {[1,2,3,4,5].map(n => <option key={n} value={n}>{n}</option>)}
            </Select>
          ))}
        </div>

        <div className="mt-4">
          <div className="text-xs text-white/70 mb-1">Free text (optional)</div>
          <textarea value={freeText} onChange={(e)=>setFreeText(e.target.value)} className="w-full min-h-[140px] px-3 py-2 rounded-xl bg-white/5 border border-white/10 focus:border-white/30 outline-none" />
        </div>

        <label className="mt-3 flex items-center gap-2 text-sm text-white/80">
          <input type="checkbox" checked={consent} onChange={(e)=>setConsent(e.target.checked)} />
          I consent to analysis and understand this is not a diagnosis.
        </label>

        <div className="mt-4 flex gap-2">
          <button onClick={submitIntake} className="px-4 py-2 rounded-xl bg-white text-black font-medium">Create session</button>
          <button onClick={runAnalysis} disabled={!sessionId} className="px-4 py-2 rounded-xl border border-white/20 disabled:opacity-40">Analyze</button>
        </div>

        {sessionId && <div className="mt-3 text-xs text-white/70">Session ID: {sessionId}</div>}
      </div>

      <div className="glass rounded-2xl p-6 lg:col-span-2">
        <h2 className="text-xl font-semibold">3) Report</h2>
        {!report && <div className="mt-3 text-white/70 text-sm">Run analysis to generate an explainable report.</div>}
        {report && (
          <div className="mt-4 grid md:grid-cols-2 gap-4">
            <div className="glass rounded-2xl p-4">
              <div className="font-medium">Scores</div>
              <pre className="mt-2 text-xs text-white/80 whitespace-pre-wrap">{JSON.stringify(report.result.scores, null, 2)}</pre>
            </div>
            <div className="glass rounded-2xl p-4">
              <div className="font-medium">Narrative</div>
              <ul className="mt-2 list-disc list-inside text-sm text-white/85 space-y-2">
                {report.result.narrative.hypotheses.map((h:string, idx:number)=>(
                  <li key={idx}>{h}</li>
                ))}
              </ul>
              <div className="mt-3 text-xs text-white/70">Explainability (sample)</div>
              <pre className="mt-2 text-xs text-white/80 whitespace-pre-wrap">{JSON.stringify(report.result.narrative.explainability, null, 2)}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

"use client";
import { useEffect, useState } from "react";
const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
export default function Home() {
  const [status, setStatus] = useState<"checking" | "connected" | "error">("checking");
  useEffect(() => { fetch(`${apiUrl}/api/health`).then((r) => { if (!r.ok) throw new Error(); return r.json(); }).then(() => setStatus("connected")).catch(() => setStatus("error")); }, []);
  const message = status === "checking" ? "Checking backend connection…" : status === "connected" ? "Backend is healthy and ready for development." : "Backend is unavailable. Start FastAPI and try again.";
  return <main className="min-h-screen px-6 py-16"><section className="mx-auto max-w-5xl"><div className="mb-16 max-w-3xl"><p className="mb-4 text-sm font-semibold uppercase tracking-widest text-indigo-600">Phase 0 foundation</p><h1 className="text-5xl font-bold tracking-tight sm:text-6xl">Smart events, built intelligently.</h1><p className="mt-6 text-xl leading-8 text-slate-600">Agentic AI Smart Event Management System — a scalable foundation for future event workflows, assistants, and automation.</p></div><div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200"><h2 className="text-lg font-semibold">System status</h2><p className="mt-2 text-slate-600">{message}</p><span className={`mt-5 inline-flex rounded-full px-3 py-1 text-sm font-medium ${status === "connected" ? "bg-emerald-100 text-emerald-700" : status === "error" ? "bg-rose-100 text-rose-700" : "bg-amber-100 text-amber-700"}`}>{status}</span></div></section></main>;
}

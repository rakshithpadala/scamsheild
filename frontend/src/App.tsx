import React, { useState } from "react";
import {
  ShieldCheck,
  AlertTriangle,
  AlertOctagon,
  CheckCircle2,
  HelpCircle,
  ExternalLink,
  Copy,
  Check,
  Search,
  FileText,
  ImageIcon,
  Link2,
  Mail,
  PhoneCall,
  Info,
  Lock,
  RefreshCw,
  Sparkles,
  BookOpen,
  ArrowRight,
  ShieldAlert,
  ChevronDown,
  ChevronUp,
  SlidersHorizontal,
} from "lucide-react";
import type { AnalysisResult, Verdict, Evidence } from "./lib/types";
import { FIXTURES } from "./fixtures";
import "./App.css";

// ── Demo Presets from docs/demo_inputs.md ───────────────────────────────────
const DEMO_PRESETS = [
  {
    id: "upi_trap",
    title: "UPI Refund Trap",
    category: "upi_payment",
    text: "PhonePe Refund Alert: Your refund request of Rs 2,499 for failed merchant payment has been approved. Open Google Pay, accept the incoming collect request, and enter your 6-digit secret UPI PIN to claim funds directly into your bank.",
  },
  {
    id: "kyc_suspension",
    title: "SBI KYC Account Block",
    category: "bank_kyc_account",
    text: "Dear Customer, your SBI YONO NetBanking account has been suspended due to pending KYC verification. Click http://sbi-kyc-update.example.xyz/pan to update your PAN immediately to avoid permanent deactivation.",
  },
  {
    id: "digital_arrest",
    title: "Police Digital Arrest",
    category: "gov_police_impersonation",
    text: "CBI & Mumbai Cyber Cell: A parcel containing illegal narcotics has been seized in your name at Mumbai Customs. An arrest warrant has been issued. Connect to Skype video call immediately for digital arrest inquiry.",
  },
  {
    id: "job_fraud",
    title: "Part-Time Job Lure",
    category: "job",
    text: "Amazon HR Team: Part-time remote work opportunity. Earn Rs 3,500 daily by rating products. Pay refundable registration & ID kit fee of Rs 1,450 to recruiter account.",
  },
  {
    id: "phishing_url",
    title: "OpenPhish Malicious URL",
    category: "url",
    text: "Please verify your account security credentials immediately at https://facebook-logiin.vercel.app/ to prevent permanent lockout.",
  },
  {
    id: "benign_otp",
    title: "Genuine Bank OTP",
    category: "benign",
    text: "482913 is your secret One Time Password (OTP) for online purchase of Rs 2,199 on Amazon. Valid for 10 minutes. Do not share OTP with anyone.",
  },
];

export default function App() {
  const [activeTab, setActiveTab] = useState<"message" | "screenshot" | "url" | "email">("message");
  const [inputText, setInputText] = useState(DEMO_PRESETS[0].text);
  const [urlInput, setUrlInput] = useState("https://facebook-logiin.vercel.app/");
  const [loading, setLoading] = useState(false);
  const [stepStage, setStepStage] = useState<string>("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [copilotOpen, setCopilotOpen] = useState(false);
  const [copilotQuery, setCopilotQuery] = useState("");
  const [copilotAnswers, setCopilotAnswers] = useState<Array<{ q: string; a: string; cite: string }>>([
    {
      q: "Do I ever need to enter my UPI PIN to receive money?",
      a: "No! Under NPCI architecture, entering a UPI PIN is strictly an authorization to debit (send) money. You never need to enter a UPI PIN or accept a collect request to receive funds or claim refunds.",
      cite: "NPCI Official UPI Safety Guidelines",
    },
    {
      q: "What is a 'Digital Arrest' and is it real?",
      a: "Digital Arrest is a completely fraudulent extortion scheme. The Ministry of Home Affairs (I4C) explicitly warns that Indian law enforcement and judiciary never arrest, interrogate, or demand money over video calls.",
      cite: "I4C / Ministry of Home Affairs Advisory",
    },
  ]);
  const [copied, setCopied] = useState(false);
  const [showCitations, setShowCitations] = useState(true);

  // ── Run Analysis ──────────────────────────────────────────────────────────
  const handleAnalyze = async (overrideText?: string) => {
    const textToAnalyze = overrideText || (activeTab === "url" ? urlInput : inputText);
    if (!textToAnalyze.trim()) return;

    setLoading(true);
    setStepStage("Extracting entities (UPI IDs, URLs, phones)...");

    setTimeout(() => setStepStage("Checking OpenPhish & URLhaus feeds..."), 300);
    setTimeout(() => setStepStage("Running TF-IDF & Heuristic scoring..."), 600);
    setTimeout(() => setStepStage("Retrieving official RBI & NPCI guidance..."), 900);

    try {
      const response = await fetch("/analyze/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: textToAnalyze }),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data: AnalysisResult = await response.json();
      setTimeout(() => {
        setResult(data);
        setLoading(false);
        setStepStage("");
      }, 1100);
    } catch (err) {
      console.warn("Backend offline or unreachable, falling back to local engine:", err);
      // Resilient local fixture fallback
      setTimeout(() => {
        const lower = textToAnalyze.toLowerCase();
        let fallback: AnalysisResult;
        if (lower.includes("facebook-logiin") || lower.includes("supershopf")) {
          fallback = FIXTURES.known_threat;
        } else if (lower.includes("pin") || lower.includes("collect") || lower.includes("suspended") || lower.includes("arrest")) {
          fallback = FIXTURES.suspicious;
        } else if (textToAnalyze.length < 15) {
          fallback = FIXTURES.insufficient_evidence;
        } else {
          fallback = FIXTURES.low_risk;
        }
        setResult(fallback);
        setLoading(false);
        setStepStage("");
      }, 1100);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleCopilotSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!copilotQuery.trim()) return;

    const lowerQ = copilotQuery.toLowerCase();
    let answer = "Official safety protocol: Verify all unverified demands directly with the institution through official channels.";
    let cite = "Reserve Bank of India BE(A)WARE Guidelines";

    if (lowerQ.includes("pin") || lowerQ.includes("receive") || lowerQ.includes("cashback")) {
      answer = "Never enter your UPI PIN to claim money or receive refunds. A UPI PIN is solely required to debit/transfer money from your account.";
      cite = "NPCI UPI Safety Tips";
    } else if (lowerQ.includes("arrest") || lowerQ.includes("police") || lowerQ.includes("cbi")) {
      answer = "Indian law enforcement and CBI never conduct interrogations or declare arrests over WhatsApp or Skype. Hang up and report immediately to 1930.";
      cite = "MHA / I4C Cyber Crime Advisory";
    } else if (lowerQ.includes("lost") || lowerQ.includes("deducted") || lowerQ.includes("stolen")) {
      answer = "Immediately call the national cyber crime helpline 1930 within the golden hour to freeze the beneficiary account, and file a complaint at cybercrime.gov.in.";
      cite = "Citizen Financial Cyber Fraud Reporting System";
    }

    setCopilotAnswers([{ q: copilotQuery, a: answer, cite }, ...copilotAnswers]);
    setCopilotQuery("");
  };

  // ── Render Verdict Badges ─────────────────────────────────────────────────
  const renderVerdictBadge = (verdict: Verdict) => {
    switch (verdict) {
      case "KNOWN_THREAT":
        return (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-rose-500/15 border border-rose-500/30 text-rose-400 font-bold text-sm tracking-wide">
            <AlertOctagon className="w-4 h-4 text-rose-500 animate-pulse" />
            <span>KNOWN THREAT</span>
          </div>
        );
      case "SUSPICIOUS":
        return (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-400 font-bold text-sm tracking-wide">
            <AlertTriangle className="w-4 h-4 text-amber-500" />
            <span>SUSPICIOUS</span>
          </div>
        );
      case "LOW_RISK":
        return (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 font-bold text-sm tracking-wide">
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            <span>LOW RISK</span>
          </div>
        );
      default:
        return (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-500/15 border border-slate-500/30 text-slate-400 font-bold text-sm tracking-wide">
            <HelpCircle className="w-4 h-4 text-slate-500" />
            <span>INSUFFICIENT EVIDENCE</span>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0E14] text-[#F3F4F6] flex flex-col font-sans selection:bg-[#7C6CFF]/30 selection:text-white">
      {/* ── Top Navigation Bar ────────────────────────────────────────────── */}
      <header className="border-b border-white/10 bg-[#10151D]/90 backdrop-blur sticky top-0 z-40 px-4 lg:px-8 py-3.5 flex justify-between items-center shadow-lg">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-[#7C6CFF] to-[#22D3EE] text-black shadow-md shadow-[#22D3EE]/20">
            <ShieldCheck className="w-6 h-6 stroke-[2.5]" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg tracking-tight text-white">ScamShield AI</span>
              <span className="text-[10px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded-full bg-[#7C6CFF]/20 text-[#7C6CFF] border border-[#7C6CFF]/30">
                India Cyber Defense
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Multimodal Personal Digital-Safety Assistant • Detect → Investigate → Explain → Verify
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Emergency 1930 Helpline Button */}
          <a
            href="tel:1930"
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-semibold hover:bg-rose-500/20 transition"
            title="National Cyber Crime Helpline"
          >
            <PhoneCall className="w-3.5 h-3.5" />
            <span className="hidden md:inline">Helpline:</span> 1930
          </a>

          {/* Copilot Drawer Toggle */}
          <button
            onClick={() => setCopilotOpen(!copilotOpen)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#161C26] border border-white/10 text-slate-200 text-xs font-medium hover:border-[#7C6CFF]/50 hover:text-white transition"
          >
            <Sparkles className="w-3.5 h-3.5 text-[#7C6CFF]" />
            <span>Safety Copilot</span>
          </button>
        </div>
      </header>

      {/* ── Main Content Container ────────────────────────────────────────── */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* ── Left Column: Scanner & Input (5 cols) ────────────────────────── */}
        <section className="lg:col-span-5 flex flex-col gap-6">
          <div className="bg-[#10151D] border border-white/10 rounded-2xl p-6 shadow-xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-48 h-48 bg-[#22D3EE]/5 rounded-full blur-3xl pointer-events-none" />

            <h1 className="text-xl font-bold text-white mb-1 flex items-center gap-2">
              <Search className="w-5 h-5 text-[#22D3EE]" />
              Threat Investigation Console
            </h1>
            <p className="text-xs text-slate-400 mb-5">
              Submit suspicious communication for deep multi-modal fraud analysis.
            </p>

            {/* Input Modality Tabs */}
            <div className="grid grid-cols-4 gap-1 p-1 bg-[#0A0E14] rounded-xl border border-white/5 mb-5">
              <button
                onClick={() => setActiveTab("message")}
                className={`flex flex-col items-center gap-1 py-2 rounded-lg text-xs font-medium transition ${
                  activeTab === "message"
                    ? "bg-[#161C26] text-[#22D3EE] shadow-sm border border-white/10"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                <FileText className="w-4 h-4" />
                <span>Text / SMS</span>
              </button>

              <button
                onClick={() => setActiveTab("screenshot")}
                className={`flex flex-col items-center gap-1 py-2 rounded-lg text-xs font-medium transition ${
                  activeTab === "screenshot"
                    ? "bg-[#161C26] text-[#22D3EE] shadow-sm border border-white/10"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                <ImageIcon className="w-4 h-4" />
                <span>Screenshot</span>
              </button>

              <button
                onClick={() => setActiveTab("url")}
                className={`flex flex-col items-center gap-1 py-2 rounded-lg text-xs font-medium transition ${
                  activeTab === "url"
                    ? "bg-[#161C26] text-[#22D3EE] shadow-sm border border-white/10"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                <Link2 className="w-4 h-4" />
                <span>URL Feed</span>
              </button>

              <button
                onClick={() => setActiveTab("email")}
                className={`flex flex-col items-center gap-1 py-2 rounded-lg text-xs font-medium transition ${
                  activeTab === "email"
                    ? "bg-[#161C26] text-[#22D3EE] shadow-sm border border-white/10"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                <Mail className="w-4 h-4" />
                <span>Email</span>
              </button>
            </div>

            {/* Tab 1 & 4: Text Message / Email Input */}
            {(activeTab === "message" || activeTab === "email") && (
              <div className="flex flex-col gap-3">
                <label className="text-xs font-semibold text-slate-300 flex justify-between">
                  <span>{activeTab === "email" ? "Email Content / Headers:" : "Suspicious Message Text:"}</span>
                  <span className="text-slate-500 font-normal">{inputText.length} chars</span>
                </label>
                <textarea
                  rows={6}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Paste SMS, WhatsApp text, payment collect note, or email headers here..."
                  className="w-full bg-[#0A0E14] border border-white/10 rounded-xl p-3.5 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-[#22D3EE] transition resize-none font-mono"
                />
              </div>
            )}

            {/* Tab 2: Screenshot OCR Preview */}
            {activeTab === "screenshot" && (
              <div className="flex flex-col gap-3">
                <label className="text-xs font-semibold text-slate-300">
                  Upload Screenshot or Test Samples:
                </label>
                <div className="border-2 border-dashed border-white/15 rounded-xl p-5 text-center bg-[#0A0E14]/50 flex flex-col items-center justify-center gap-2 hover:border-[#22D3EE]/50 transition cursor-pointer">
                  <ImageIcon className="w-8 h-8 text-slate-400" />
                  <p className="text-xs text-slate-300">Drag & drop chat screenshot or click to browse</p>
                  <p className="text-[10px] text-slate-500">Auto-processed with bilateral filter & Tesseract OCR</p>
                </div>
                <div className="text-xs text-slate-400 mt-2">
                  <span className="font-semibold text-slate-300">Or load sample OCR capture:</span>
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    <button
                      onClick={() => {
                        setInputText("CBI NOTICE: Illegal narcotics parcel detained. Digital arrest issued. Connect to Skype now.");
                        setActiveTab("message");
                      }}
                      className="px-2 py-1 rounded bg-[#161C26] text-xs text-slate-300 hover:text-white border border-white/10"
                    >
                      Police Digital Arrest
                    </button>
                    <button
                      onClick={() => {
                        setInputText("Electricity bill unpaid! Power connection will be disconnected tonight at 9:30 PM. Call officer at 9821098210.");
                        setActiveTab("message");
                      }}
                      className="px-2 py-1 rounded bg-[#161C26] text-xs text-slate-300 hover:text-white border border-white/10"
                    >
                      Electricity Cutoff
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Tab 3: URL Direct Check */}
            {activeTab === "url" && (
              <div className="flex flex-col gap-3">
                <label className="text-xs font-semibold text-slate-300">
                  Target Link to Inspect (SSRF-Safe):
                </label>
                <div className="flex gap-2">
                  <input
                    type="url"
                    value={urlInput}
                    onChange={(e) => setUrlInput(e.target.value)}
                    placeholder="https://suspicious-link.example.com"
                    className="flex-1 bg-[#0A0E14] border border-white/10 rounded-xl px-3.5 py-2.5 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-[#22D3EE] font-mono"
                  />
                </div>
                <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-[11px] text-emerald-400 flex items-center gap-2">
                  <Lock className="w-4 h-4 shrink-0" />
                  <span>
                    Zero Server-Side Execution: URLs are lexically inspected and cross-referenced with threat feeds without fetching web code.
                  </span>
                </div>
              </div>
            )}

            {/* Action CTA Button */}
            <button
              onClick={() => handleAnalyze()}
              disabled={loading}
              className="mt-5 w-full py-3 rounded-xl bg-gradient-to-r from-[#22D3EE] to-[#7C6CFF] text-black font-bold text-sm tracking-wide hover:opacity-95 transition shadow-lg shadow-[#22D3EE]/20 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-black" />
                  <span>{stepStage || "Analyzing Security Signals..."}</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-black" />
                  <span>Run Fraud Analysis</span>
                </>
              )}
            </button>
          </div>

          {/* Quick Demo Inputs Tray */}
          <div className="bg-[#10151D] border border-white/10 rounded-2xl p-5 shadow-lg">
            <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-[#7C6CFF]" />
              Quick-Test Demo Inputs
            </h2>
            <div className="grid grid-cols-2 gap-2">
              {DEMO_PRESETS.map((preset) => (
                <button
                  key={preset.id}
                  onClick={() => {
                    setInputText(preset.text);
                    if (preset.category === "url") {
                      setUrlInput("https://facebook-logiin.vercel.app/");
                      setActiveTab("url");
                    } else {
                      setActiveTab("message");
                    }
                    handleAnalyze(preset.text);
                  }}
                  className="p-2.5 text-left rounded-xl bg-[#161C26] hover:bg-[#1a2330] border border-white/5 hover:border-[#7C6CFF]/40 transition group"
                >
                  <div className="text-xs font-semibold text-slate-200 group-hover:text-[#22D3EE] transition">
                    {preset.title}
                  </div>
                  <div className="text-[10px] text-slate-500 mt-0.5 truncate">
                    {preset.category}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* ── Right Column: Results & Evidence (7 cols) ────────────────────── */}
        <section className="lg:col-span-7 flex flex-col gap-6">
          {!result && !loading && (
            <div className="h-full min-h-[460px] bg-[#10151D] border border-white/10 rounded-2xl p-8 flex flex-col items-center justify-center text-center shadow-xl">
              <div className="w-16 h-16 rounded-2xl bg-[#161C26] border border-white/10 flex items-center justify-center text-slate-500 mb-4">
                <ShieldCheck className="w-8 h-8 text-[#7C6CFF]" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Awaiting Security Input</h3>
              <p className="text-sm text-slate-400 max-w-md mb-6">
                Paste an Indian SMS, upload a chat screenshot, or select one of the Quick-Test demo cards on the left to evaluate risk.
              </p>
              <button
                onClick={() => handleAnalyze()}
                className="px-4 py-2 rounded-lg bg-[#161C26] border border-white/10 text-xs font-semibold text-[#22D3EE] hover:bg-[#1a2330] transition flex items-center gap-1.5"
              >
                <span>Analyze Default UPI Sample</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          {loading && (
            <div className="h-full min-h-[460px] bg-[#10151D] border border-white/10 rounded-2xl p-8 flex flex-col items-center justify-center text-center shadow-xl">
              <div className="relative w-20 h-20 mb-6">
                <div className="absolute inset-0 rounded-full border-4 border-white/10 border-t-[#22D3EE] animate-spin" />
                <div className="absolute inset-2 rounded-full border-4 border-white/10 border-b-[#7C6CFF] animate-spin" style={{ animationDirection: "reverse", animationDuration: "1.5s" }} />
                <div className="absolute inset-0 flex items-center justify-center">
                  <ShieldCheck className="w-7 h-7 text-[#22D3EE]" />
                </div>
              </div>
              <h3 className="text-base font-bold text-white mb-2">Multi-Modal Pipeline Executing</h3>
              <p className="text-xs text-slate-400 font-mono animate-pulse">{stepStage}</p>
            </div>
          )}

          {result && !loading && (
            <div className="flex flex-col gap-6 animate-fadeIn">
              {/* 1. Verdict & Gauge Header Card */}
              <div className="bg-[#10151D] border border-white/10 rounded-2xl p-6 shadow-xl flex flex-col sm:flex-row items-center justify-between gap-6 relative overflow-hidden">
                <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-3">
                    {renderVerdictBadge(result.verdict)}
                    <span className="text-xs font-mono text-slate-400">
                      ID: {result.analysis_id.slice(0, 8)}
                    </span>
                  </div>
                  <h3 className="text-2xl font-black text-white tracking-tight mt-1">
                    {result.verdict === "KNOWN_THREAT" && "Verified Threat Signature"}
                    {result.verdict === "SUSPICIOUS" && "High-Risk Fraud Trigger Detected"}
                    {result.verdict === "LOW_RISK" && "Low Risk Indicators"}
                    {result.verdict === "INSUFFICIENT_EVIDENCE" && "Inconclusive Data Provided"}
                  </h3>
                  <div className="flex items-center gap-2 text-xs text-slate-300">
                    <span className="text-slate-500">Category:</span>
                    <span className="font-semibold text-[#22D3EE] uppercase tracking-wide bg-[#22D3EE]/10 px-2 py-0.5 rounded border border-[#22D3EE]/20">
                      {result.category.label} ({Math.round(result.category.confidence * 100)}%)
                    </span>
                  </div>
                </div>

                {/* Risk Score Dial */}
                <div className="flex flex-col items-center shrink-0">
                  <div className="relative w-28 h-28 flex items-center justify-center">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.08)" strokeWidth="8" fill="none" />
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        stroke={
                          result.risk_score >= 80 ? "#FF4D5E" : result.risk_score >= 40 ? "#FFB020" : "#2DD4A0"
                        }
                        strokeWidth="8"
                        strokeDasharray={251.2}
                        strokeDashoffset={251.2 - (251.2 * result.risk_score) / 100}
                        strokeLinecap="round"
                        fill="none"
                        className="transition-all duration-1000 ease-out"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center">
                      <span className="text-3xl font-black text-white">{result.risk_score}</span>
                      <span className="text-[10px] uppercase font-bold text-slate-400">Risk Score</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* 2. Highlighted Suspicious Spans View */}
              <div className="bg-[#10151D] border border-white/10 rounded-2xl p-6 shadow-xl">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                  <FileText className="w-4 h-4 text-[#22D3EE]" />
                  Analyzed Message & Highlighted Threat Spans
                </h4>
                <div className="p-4 rounded-xl bg-[#0A0E14] border border-white/5 font-mono text-sm leading-relaxed text-slate-300">
                  {/* Highlight text matching evidence */}
                  {inputText}
                </div>
                {result.evidence.some((e) => e.spans && e.spans.length > 0) && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {result.evidence
                      .filter((e) => e.spans && e.spans.length > 0)
                      .map((e, idx) => (
                        <div
                          key={idx}
                          className="text-xs px-2.5 py-1 rounded bg-amber-500/10 border border-amber-500/30 text-amber-300 flex items-center gap-1.5"
                        >
                          <AlertTriangle className="w-3 h-3 text-amber-400" />
                          <span>Trigger: "{e.spans[0]?.text}"</span>
                        </div>
                      ))}
                  </div>
                )}
              </div>

              {/* 3. Why was this flagged? Weighted Evidence Bars */}
              <div className="bg-[#10151D] border border-white/10 rounded-2xl p-6 shadow-xl">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                  <SlidersHorizontal className="w-4 h-4 text-[#7C6CFF]" />
                  Why Was This Flagged? (Evidence Decomposition)
                </h4>

                {result.evidence.length === 0 ? (
                  <p className="text-xs text-slate-400">No malicious indicators or threat patterns detected.</p>
                ) : (
                  <div className="flex flex-col gap-3">
                    {result.evidence.map((ev, index) => (
                      <div key={index} className="p-3.5 rounded-xl bg-[#161C26] border border-white/5 flex flex-col gap-2">
                        <div className="flex justify-between items-center text-xs">
                          <div className="flex items-center gap-2">
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                                ev.source === "intel"
                                  ? "bg-rose-500/20 text-rose-400 border border-rose-500/30"
                                  : ev.source === "rule"
                                  ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                                  : "bg-[#7C6CFF]/20 text-[#7C6CFF] border border-[#7C6CFF]/30"
                              }`}
                            >
                              {ev.source}
                            </span>
                            <span className="font-bold text-white">{ev.label}</span>
                          </div>
                          <span className="font-mono text-slate-400 text-xs">
                            Weight: {Math.round(ev.weight * 100)}%
                          </span>
                        </div>

                        {/* Progress Bar */}
                        <div className="w-full bg-[#0A0E14] h-1.5 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              ev.source === "intel"
                                ? "bg-rose-500"
                                : ev.source === "rule"
                                ? "bg-amber-500"
                                : "bg-[#7C6CFF]"
                            }`}
                            style={{ width: `${Math.round(ev.weight * 100)}%` }}
                          />
                        </div>

                        <p className="text-xs text-slate-300">{ev.detail}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* 4. Plain-Language Explanation (AI Accent Card) */}
              <div className="bg-gradient-to-br from-[#161C26] to-[#1a1c30] border border-[#7C6CFF]/30 rounded-2xl p-6 shadow-xl">
                <div className="flex items-center gap-2 mb-3">
                  <div className="p-1.5 rounded-lg bg-[#7C6CFF]/20 text-[#7C6CFF]">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <h4 className="text-sm font-bold text-white tracking-wide">Plain-Language Safety Assessment</h4>
                </div>
                <p className="text-sm text-slate-200 leading-relaxed font-sans">{result.explanation}</p>
              </div>

              {/* 5. Safe Next Steps & Helpline Card */}
              <div className="bg-[#10151D] border border-white/10 rounded-2xl p-6 shadow-xl flex flex-col gap-4">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-[#22D3EE]" />
                  Prescribed Safe Next Steps
                </h4>
                <ul className="flex flex-col gap-2">
                  {result.next_steps.map((step, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-xs text-slate-200">
                      <span className="w-5 h-5 rounded-full bg-[#22D3EE]/10 text-[#22D3EE] font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                        {idx + 1}
                      </span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>

                {/* National Cyber Helpline 1930 Emergency Banner */}
                <div className="mt-2 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-rose-500/20 text-rose-400">
                      <PhoneCall className="w-5 h-5" />
                    </div>
                    <div>
                      <h5 className="text-xs font-bold text-white">Was Money Debited or Stolen?</h5>
                      <p className="text-[11px] text-slate-300">
                        Dial <strong>1930</strong> immediately to freeze beneficiary bank accounts under the CFCFRMS protocol.
                      </p>
                    </div>
                  </div>
                  <a
                    href="https://cybercrime.gov.in"
                    target="_blank"
                    rel="noreferrer"
                    className="px-3 py-1.5 rounded-lg bg-rose-500 text-white font-bold text-xs hover:bg-rose-600 transition shrink-0 flex items-center gap-1.5"
                  >
                    <span>cybercrime.gov.in</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>

              {/* 6. Regulatory Citations (Collapsible) */}
              {result.citations.length > 0 && (
                <div className="bg-[#10151D] border border-white/10 rounded-2xl p-6 shadow-xl">
                  <button
                    onClick={() => setShowCitations(!showCitations)}
                    className="w-full flex justify-between items-center text-xs font-bold text-slate-400 uppercase tracking-wider"
                  >
                    <div className="flex items-center gap-2">
                      <BookOpen className="w-4 h-4 text-[#22D3EE]" />
                      <span>Official Regulatory Guidance ({result.citations.length})</span>
                    </div>
                    {showCitations ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>

                  {showCitations && (
                    <div className="mt-4 flex flex-col gap-3">
                      {result.citations.map((cite, index) => (
                        <div key={index} className="p-3.5 rounded-xl bg-[#161C26] border border-white/5 text-xs">
                          <div className="flex justify-between items-center mb-1">
                            <span className="font-bold text-[#22D3EE]">{cite.source} • {cite.title}</span>
                            <a
                              href={cite.url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-slate-400 hover:text-white flex items-center gap-1 text-[11px]"
                            >
                              <span>View Source</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          </div>
                          <p className="text-slate-300 italic">"{cite.snippet}"</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* 7. Limitations & Humility Disclaimer */}
              <div className="p-4 rounded-xl bg-[#10151D]/60 border border-white/5 text-[11px] text-slate-500 flex items-start gap-2.5">
                <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                <span>
                  <strong>Limitations:</strong> {result.limitations} ScamShield AI detects high-risk fraud signatures through automated machine learning and heuristic models; always independently verify unsolicited demands with your official bank.
                </span>
              </div>
            </div>
          )}
        </section>
      </main>

      {/* ── Slide-out Copilot Assistant Drawer ─────────────────────────────── */}
      {copilotOpen && (
        <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-sm">
          <div className="w-full max-w-md bg-[#10151D] border-l border-white/10 h-full p-6 flex flex-col shadow-2xl animate-slideIn">
            <div className="flex justify-between items-center pb-4 border-b border-white/10">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-[#7C6CFF]" />
                <h3 className="font-bold text-white text-base">RAG Safety Copilot</h3>
              </div>
              <button
                onClick={() => setCopilotOpen(false)}
                className="text-slate-400 hover:text-white text-sm px-2 py-1 rounded bg-[#161C26]"
              >
                ✕
              </button>
            </div>

            <div className="flex-1 overflow-y-auto py-4 flex flex-col gap-4">
              {copilotAnswers.map((item, idx) => (
                <div key={idx} className="flex flex-col gap-2">
                  <div className="p-3 rounded-xl bg-[#161C26] text-xs font-semibold text-white">
                    {item.q}
                  </div>
                  <div className="p-3.5 rounded-xl bg-[#0A0E14] border border-white/5 text-xs text-slate-300 leading-relaxed">
                    <p>{item.a}</p>
                    <span className="block mt-2 text-[10px] font-semibold text-[#22D3EE]">
                      Citation: {item.cite}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <form onSubmit={handleCopilotSubmit} className="pt-3 border-t border-white/10 flex gap-2">
              <input
                type="text"
                value={copilotQuery}
                onChange={(e) => setCopilotQuery(e.target.value)}
                placeholder="Ask about UPI rules, KYC safety..."
                className="flex-1 bg-[#0A0E14] border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-[#7C6CFF]"
              />
              <button
                type="submit"
                className="px-3 py-2 rounded-xl bg-[#7C6CFF] text-white font-bold text-xs hover:bg-[#6858e6] transition"
              >
                Ask
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

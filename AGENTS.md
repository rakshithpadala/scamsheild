# SCAMSHIELD AI — MASTER PROMPT v2 (6-day, token-efficient, human + LLM split)

You are a senior full-stack ML engineer and product designer building **ScamShield AI** with me. Keep this file in the workspace rules file. It is the source of truth. Follow it over any default behaviour.

## 1. Product
ScamShield AI is a multimodal personal digital-safety assistant (India-focused). A user submits a message, screenshot, URL or email and gets: verdict, 0–100 risk score, likely scam category, evidence with highlighted text spans, URL analysis, threat-intel evidence, plain-language explanation, cited official guidance (RAG), safe next steps, and limitations. Philosophy: **Detect → Investigate → Explain → Verify → Act Safely.** Contribution: multimodal, evidence-based personal scam analysis (not a new fraud-detection invention). University AI/ML project (Mumbai University syllabus) that must also be a working demo. **Submission: Thu 8 Oct 2026. Day 1 = Fri 2 Oct.**

## 2. Non-negotiable principles
1. The LLM never decides the verdict. ML + rules + threat intel produce evidence; the LLM only explains it and orchestrates Copilot tools.
2. Never overclaim ("high-risk characteristics detected", never "definitely a scam"). Always include a limitations note.
3. Verdicts are exactly `KNOWN_THREAT`, `SUSPICIOUS`, `LOW_RISK`, `INSUFFICIENT_EVIDENCE`. No threat-intel match is NOT proof of safety. Intel `unavailable` is never treated as `no_match`.
4. Never ask for OTP, UPI PIN or passwords; never store credentials; never impersonate a bank/police/government. If money may be lost, show 1930 and cybercrime.gov.in.
5. Optimise for recall (false negatives are dangerous). Report precision, recall, F1, ROC-AUC, confusion matrix, FPR, FNR; never accuracy alone. Select models by recall at acceptable FPR.
6. No auto-retraining from user feedback. Never visit or render submitted URLs server-side (lexical analysis + intel lookup only; SSRF-safe).
7. Be honest about data: scam categories use synthetic data + rules, evaluated on a hand-written test set. Never claim a metric you did not measure.

## 3. DIVISION OF LABOUR (critical for token efficiency)
**HUMAN does (do not do these yourself unless I ask):** installs, project scaffolding commands (Vite/shadcn/pip), downloading datasets and RAG documents, `.env`, the 60-row hand-written test set, reviewing synthetic data, demo inputs/screenshots, UI component picks and microcopy (`docs/copy.md`), running commands, manual UI verification, git routine, report/PPT/video writing.
**YOU do:** reasoning-heavy code, tests, training scripts, notebooks wiring, and **reviewing my work when asked**.

**Expected human file locations (read them when needed; never regenerate them):**
- `ml/data/raw/sms/SMSSpamCollection`, `ml/data/raw/tranco/top-1m.csv`, `ml/data/raw/openphish/feed_YYYYMMDD.txt` (multiple), `ml/data/raw/urlhaus/csv_recent.csv`
- `ml/data/handwritten_test.csv` (columns `text,label_scam,category,has_url`; never train on it)
- `knowledge_base/raw/*.pdf` + `knowledge_base/sources.csv` (file,title,publisher,url,date_accessed,topic)
- `docs/DATA.md`, `docs/copy.md`, `docs/ui_picks.md`, `docs/demo_inputs.md`, `ml/data/demo_screenshots/`
- `scripts/validate_my_work.py` (I run it; you never need to rewrite it)

**REVIEW PROTOCOL.** When I send a review request, check the named files against these criteria and reply in **≤15 lines** as `PASS` or a numbered `FIX` list with row/line references. Do not rewrite my files unless asked.
- Hand-written test set: ≥60 rows, ≥15 benign incl. hard negatives (genuine bank alerts, real-style OTP notices, courier updates), 4 per scam category, India-realistic, varied tone, no real phone numbers/emails, no overlap with synthetic data, correct labels and allowed category values.
- Synthetic data: variety, realism, label correctness, no repeated templates, no real personal data.
- RAG sources: official publishers only, relevant topics (UPI PIN/QR, fake cashback, investment fraud, unknown apps, KYC/OTP, impersonation, reporting 1930, money-lost steps), text-selectable PDFs.
- `docs/copy.md`: plain language for elderly users, no overclaiming, matches the four verdict labels, safe consent and limitations text.
- Bug batches: fix in priority order, edit only necessary files, run tests, reply ≤8 lines.
- Final audit: list only failures/risks (secrets, leftover `# MOCK:`, unmeasured metrics, missing tests).

## 4. TOKEN DISCIPLINE (apply to every task)
- Edit only the files named. Do not reprint unchanged files. No explanations of code unless asked. Reply ≤8 lines (≤15 for reviews).
- Never read `ml/data/raw`, model artifacts, `node_modules`, or logs in full. Read file heads/tails or run a count/summary script.
- Do not open the browser or take screenshots unless I ask; I verify the UI manually and send a bug batch.
- LLM calls inside the app use a small model, capped `max_tokens`, and a cache keyed by analysis hash. Default to the **template explanation**; use the LLM explanation only when `USE_LLM_EXPLANATION=true`.
- One phase per session. At the end of each task: run tests/ruff, then report **what works / what is mocked / what's next** in ≤8 lines, then STOP and wait for "continue".

## 4b. FREE-TIER MODE (I have no paid subscription; quota is limited)
- Assume limited quota and rate limits. Prefer **one complete file per answer** over many small edits; do not re-read large files; do not run parallel agents or sub-agents.
- Before any task estimated to need more than ~10 file edits, split it into steps and tell me the step list in ≤5 lines, then do step 1 only.
- If you hit a quota/rate-limit error, tell me the exact next step to resume, and list the work I can do meanwhile.
- The **app's own LLM is optional and free-tier only**: `LLMClient` supports `gemini` (default), `groq`, `ollama`, and `template`, selected by `LLM_PROVIDER`. Handle 429/timeouts with backoff and **silently fall back to template**. Default `USE_LLM_EXPLANATION=false`. Never send real user data to a free-tier provider; use demo data only.
- Add `ml/artifacts/demo_cache.json`: precomputed explanations for the 10 inputs in `docs/demo_inputs.md`, used when the LLM is unavailable so the demo never depends on network or quota.

## 5. Stack (do not substitute)
Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2 (**SQLite**), httpx; scikit-learn, XGBoost, pandas, joblib; TF-IDF, sentence-transformers `all-MiniLM-L6-v2`, spaCy `en_core_web_sm`; OpenCV + pytesseract; SHAP; MLflow (local); **VectorStore interface with NumPy+JSON implementation** (pgvector = documented future work); provider-agnostic `LLMClient` (free providers gemini/groq/ollama + template fallback, strict-JSON, timeout/backoff); SSE for progress. Frontend: Vite + React + TS, Tailwind, shadcn/ui, Framer Motion, Recharts, lucide-react, TanStack Query, Zustand. Docker Compose = backend + frontend (+ MLflow). GitHub Actions CI (ruff, pytest, frontend build, docker build). pytest + a few Vitest.

**Repo:** `backend/app/{api,core,services,ml,rules,intel,rag,agent,db,schemas}`, `backend/tests`, `ml/{data,notebooks,training,artifacts}`, `knowledge_base`, `frontend/src/{components,pages,features,lib,store,fixtures}`, `docs`, `scripts`, `docker-compose.yml`, `.github/workflows/ci.yml`.

## 6. API contract (define Pydantic + `frontend/src/lib/types.ts` + 4 fixture JSONs FIRST, one per verdict)
Endpoints: `POST /analyze/message|url|screenshot|email`, `GET /analyze/stream/{id}` (SSE stages: reading, extracting_links, checking_feeds, scoring, explaining), `GET /analysis/{id}`, `GET /analysis/history`, `POST /copilot/chat`, `POST /feedback`, `GET /patterns/summary`, `GET /models/metrics`, `GET /health`.

`AnalysisResult`: `analysis_id`, `input_type`, `verdict`, `risk_score` (0–100), `category{label,confidence}`, `evidence[{id,label,weight,source(rule|ml|intel),spans,detail}]`, `entities{urls,phones,emails,upi_ids}`, `url_results[{url,ml_risk,features,intel{status(match|no_match|unavailable),provider}}]`, `ocr{text,confidence}`, `explanation`, `next_steps[]`, `citations[{source,title,page,snippet,url}]`, `limitations`, `model_version`.

Validation: size/type limits on uploads, URL sanitisation, rate limiting, no PII in logs, safe error messages.

## 7. ML, rules, fusion, data
- **Text scam/ham:** TF-IDF + LR, KNN, DT, RF, SVM, XGBoost on UCI SMS; log all to MLflow; pick by recall at acceptable FPR.
- **Category (10 merged classes):** `bank_kyc_account, upi_payment, cashback_reward_lottery, job, investment, loan, delivery, gov_police_impersonation, tech_support, other` (map to the 14-label taxonomy in docs). Train on synthetic data: **have the LLM write ~8 seed messages per class in at most 2–3 prompts, then expand programmatically with a script (no further LLM calls)** (template/slot substitution for names, amounts, brands, links, fillers) to ~70 per class; mark `synthetic=true`. Compare TF-IDF+LR vs MiniLM embeddings+LR on the human's hand-written test set. Rule-based category fallback.
- **Rule engine (≥12 rules, each returns evidence with spans, unit-tested with positive/negative cases):** urgency; account block/suspension threat; OTP/PIN/password/CVV request; KYC/verification; prize/lottery/cashback; fee/advance payment; QR/"scan to receive"; external/shortened link; APK/unknown app; brand/bank/government/police impersonation; arrest/legal threat; suspicious phone/UPI ID; email: Reply-To mismatch, display-name spoofing.
- **URL model:** ≥25 lexical features (length, subdomain count, digit ratio, special chars, entropy, suspicious tokens, IP host, punycode, TLD, https, path depth, query length…). Benign = Tranco, malicious = OpenPhish + URLhaus. **Split by registered domain** (GroupShuffleSplit). Train LR/RF/XGBoost, SHAP on the best tree model. If a metric >99%, investigate leakage and tell me.
- **Threat intel:** `ThreatProvider` interface; OpenPhish + URLhaus adapters; local cache + refresh function; statuses match/no_match/unavailable.
- **Risk fusion:** transparent weighted combination of text prob, URL prob, rule score, intel status; verified intel match overrides to `KNOWN_THREAT`; fit/validate weights on held-out data (grid search or small LR meta-model), document in `docs/EVAL.md`; calibrated 0–100 score. ≥8 edge-case tests (intel override, intel unavailable, text-only, URL-only, no signals, conflicting signals).
- **Explainability:** LR coefficients for text, SHAP for URL model, highlighted spans.
- **OCR:** OpenCV (grayscale, denoise, threshold, upscale) → Tesseract → same pipeline; return OCR confidence; editable text in UI.
- **Email:** paste-only; `email` module header parse + 2 email rules; reuse message pipeline.
- **Syllabus notebooks (not on critical path; each exports JSON to `ml/artifacts/`):** clustering (K-Means + hierarchical, GMM optional, silhouette), PCA 2-D, Apriori (mlxtend) on indicator co-occurrence, Ridge/Linear regression (MAE/R²), BFS/DFS/UCS/Greedy/A* over an entity graph (networkx; documented heuristic; compare nodes expanded and path cost).

## 8. RAG, LLM, Copilot
- RAG: ingest `knowledge_base/raw` → chunk (keep source/title/page) → MiniLM embeddings → VectorStore (NumPy+JSON) → top-k retrieval. Test with 5 gold questions (e.g. "Is entering my UPI PIN necessary to receive money?").
- Explanation: input = fused JSON + retrieved chunks; output strict JSON `{explanation, next_steps, used_citations}`; schema-validate; fall back to template if invalid or unsupported. Guardrail tests: never request OTP/PIN/passwords, never claim certainty, always include limitations.
- Copilot has two modes: **offline mode (default, no LLM)** = keyword/intent router → tools → answer assembled from retrieved cited text; **LLM mode (optional)** = bounded tool loop (max 5 steps) over `analyze_message`, `check_url`, `retrieve_guidance`, `compare_with_known_patterns`; return tool calls to the UI; answer factual safety questions only from retrieved sources with citations; if retrieval is empty, say so.

## 9. UI spec
"Calm security command-center", dark-first, light toggle if time permits. Tokens: bg `#0A0E14`, surface `#10151D`, raised `#161C26`, border `rgba(255,255,255,.08)`; verdict colours KNOWN `#FF4D5E`, SUSPICIOUS `#FFB020`, LOW `#2DD4A0`, INSUFFICIENT `#8B95A7`; AI accent `#7C6CFF`; primary `#22D3EE`; fonts Geist/Inter + JetBrains Mono for URLs; 16–20px radius, restrained glass, 150–250ms motion, reduced-motion respected, WCAG AA, never colour-only, mobile-responsive, plain language for elderly users. Use text from `docs/copy.md` and components from `docs/ui_picks.md` where provided.
Pages: Home/Scanner (tabs Message/Screenshot/URL/Email), Result, History, Copilot drawer, Pattern Explorer, Model Lab, About/Limitations.
**Result page order:** (1) animated risk gauge + verdict badge → (2) category chip + confidence → (3) original text with highlighted suspicious spans → (4) "Why was this flagged?" weighted evidence bars grouped by ML/Rules/Intel → (5) plain-language explanation (AI accent card) → (6) safe next steps + reporting card (1930, cybercrime.gov.in) → (7) citations (collapsible) + limitations. Also: live SSE stepper, screenshot page with side-by-side editable OCR, URL anatomy card (subdomain/domain/TLD) with provider pills, Copilot tool-call chips, loading/empty/error states, consent notice. Build against `frontend/src/fixtures` behind `VITE_USE_MOCK` until the API is ready.

## 10. 6-DAY PLAN (your tasks; human tasks are in my checklist)
- **Day 1:** repo skeleton, FastAPI + SQLite, schemas + TS types + fixtures (commit first), preprocessing, entity extraction, rule engine + tests, text model comparison in MLflow, `POST /analyze/message` with simple fusion + template explanation. Frontend: shell, design tokens, Home, Result page from fixtures.
- **Day 2:** SSE stages; seed-and-expand synthetic data (show me 20 samples, then stop for my review); category models vs hand-written set; Fusion v1 + tests; frontend: stepper, real API, History, error/empty states.
- **Day 3:** URL features + dataset + domain-grouped training + SHAP; intel adapters + cache; `/analyze/url`; integrate into message fusion; OCR + `/analyze/screenshot`; URL and Screenshot pages.
- **Day 4:** RAG + gold-question tests; LLMClient + strict-JSON explanation with fallback + guardrail tests; Copilot loop + chips UI; email endpoint; feedback endpoint; citations/explanation/limitations UI.
- **Day 5:** notebooks + JSON exports; `/patterns/summary`, `/models/metrics`; Model Lab + Pattern Explorer; remaining pytest; CI; Docker Compose from clean clone; real numbers into `docs/EVAL.md`. **FEATURE FREEZE at end of day.**
- **Day 6:** polish only (microcopy, mobile, accessibility), rate limits, README with mermaid diagram, report tables from `docs/EVAL.md` on request. **Day 7 (8 Oct): buffer, no features.**

**Cut ladder if behind (cut first → last):** LLM explanation/LLM-mode Copilot (keep templates + offline Copilot) → optional adapters/GMM/DistilBERT → Docker/CI polish → email page → Pattern Explorer interactivity → Copilot streaming → history filters → light theme → RAG docs (min 5) → categories (min 6). **Never cut:** message scanner, URL scanner, screenshot OCR, fusion + evidence view, model comparison with real metrics, RAG citations, working demo.

## 11. Working protocol and Definition of Done
1. Start of each task: 3–5 line plan (files, tests, done-when), then implement.
2. Define contracts first; small conventional commits; type hints; secrets only in `.env`.
3. Mark stubs `# MOCK:` and list them in `docs/KNOWN_GAPS.md`; replace as you go.
4. Real metrics only, logged in MLflow and copied to `docs/EVAL.md`.
5. If a dataset/API is unavailable, state the assumption and take the simplest option; ask only when blocked.
6. **Done =** `docker compose up` runs from a clean clone; a new user can submit a message, screenshot, URL or email and understand the result, the evidence, and what to verify next, without being asked for credentials; MLflow shows the model comparison; CI is green.

**Begin now:** acknowledge in ≤5 lines, confirm you have read the human-owned file locations and review protocol, then start Day 1 backend tasks. Wait for my "continue" after each task.

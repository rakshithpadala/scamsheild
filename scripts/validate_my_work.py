#!/usr/bin/env python3
"""ScamShield - validate the work YOU do by hand (zero LLM tokens).

Put this file at  scripts/validate_my_work.py  in your repo root and run:

    python scripts/validate_my_work.py setup
    python scripts/validate_my_work.py env
    python scripts/validate_my_work.py data
    python scripts/validate_my_work.py rag
    python scripts/validate_my_work.py handwritten
    python scripts/validate_my_work.py demo
    python scripts/validate_my_work.py all

Output lines are PASS / WARN / FAIL. Only paste the FAIL/WARN lines to the LLM.
Uses only the Python standard library, so it works before you install packages.
"""
import csv
import glob
import importlib.util
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
results = {"PASS": 0, "WARN": 0, "FAIL": 0}


def out(level, msg):
    results[level] += 1
    print(f"[{level}] {msg}")


def p(*parts):
    return os.path.join(ROOT, *parts)


def count_lines(path, skip_comments=False):
    n = 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip() and not (skip_comments and line.startswith("#")):
                n += 1
    return n


def cmd_version(cmd):
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20, check=False)
        return (r.stdout or r.stderr).strip().splitlines()[0]
    except (subprocess.SubprocessError, OSError):
        return "found (version unreadable)"


# ----------------------------------------------------------------- setup
def check_setup():
    v = sys.version_info
    if (v.major, v.minor) >= (3, 11):
        out("PASS", f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        out("FAIL", f"Python {v.major}.{v.minor} found, need 3.11+")
    for name, cmd in [
        ("Node", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
        ("Git", ["git", "--version"]),
        ("Docker", ["docker", "--version"]),
        ("Tesseract", ["tesseract", "--version"]),
    ]:
        ver = cmd_version(cmd)
        out("PASS" if ver else "FAIL", f"{name}: {ver or 'NOT FOUND on PATH'}")
    pkgs = ["fastapi", "uvicorn", "pydantic", "sqlalchemy", "pandas", "sklearn",
            "xgboost", "joblib", "mlflow", "sentence_transformers", "spacy", "shap",
            "cv2", "pytesseract", "pypdf", "numpy", "mlxtend", "networkx", "httpx", "pytest"]
    missing = [x for x in pkgs if importlib.util.find_spec(x) is None]
    if missing:
        out("FAIL", "Python packages missing (activate your venv?): " + ", ".join(missing))
    else:
        out("PASS", "All required Python packages import")
    if importlib.util.find_spec("spacy"):
        if importlib.util.find_spec("en_core_web_sm"):
            out("PASS", "spaCy model en_core_web_sm installed")
        else:
            out("FAIL", "spaCy model missing: python -m spacy download en_core_web_sm")
    if os.path.isdir(p("frontend", "node_modules")):
        out("PASS", "frontend/node_modules present")
    else:
        out("WARN", "frontend/node_modules missing (run npm install in frontend/)")


# ------------------------------------------------------------------- env
def check_env():
    envp = p(".env")
    if not os.path.exists(envp):
        out("FAIL", ".env not found (copy .env.example to .env and add your key)")
    else:
        with open(envp, encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        provider = re.search(r"^LLM_PROVIDER\s*=\s*(\S+)", txt, re.MULTILINE)
        prov = provider.group(1).lower() if provider else ""
        has_key = re.search(r"^(GEMINI_API_KEY|GROQ_API_KEY|OPENROUTER_API_KEY|ANTHROPIC_API_KEY|OPENAI_API_KEY|LLM_API_KEY)\s*=\s*\S{10,}",
                            txt, re.MULTILINE)
        if prov in ("ollama", "none", "template"):
            out("PASS", f"LLM_PROVIDER={prov} (no API key needed)")
        elif has_key:
            out("PASS", "LLM API key present in .env (value not printed)")
        else:
            out("FAIL", "No free-tier key found in .env. Add GEMINI_API_KEY or GROQ_API_KEY, or set LLM_PROVIDER=ollama or template")
    gi = p(".gitignore")
    gtxt = ""
    if os.path.exists(gi):
        with open(gi, encoding="utf-8", errors="ignore") as f:
            gtxt = f.read()
    for needed in [".env", "ml/data/raw", "node_modules", ".venv"]:
        out("PASS" if needed in gtxt else "FAIL", f".gitignore contains '{needed}'")


# ------------------------------------------------------------------ data
def check_data():
    sms = p("ml", "data", "raw", "sms", "SMSSpamCollection")
    if os.path.exists(sms):
        n = count_lines(sms)
        out("PASS" if 5000 <= n <= 6000 else "WARN", f"UCI SMS Spam: {n} lines (expect ~5,574)")
    else:
        out("FAIL", "Missing ml/data/raw/sms/SMSSpamCollection")

    tr = glob.glob(p("ml", "data", "raw", "tranco", "*.csv"))
    if tr:
        n = count_lines(tr[0])
        out("PASS" if n >= 10000 else "FAIL", f"Tranco list: {n} rows ({os.path.basename(tr[0])})")
    else:
        out("FAIL", "Missing ml/data/raw/tranco/*.csv (Tranco list)")

    op = glob.glob(p("ml", "data", "raw", "openphish", "feed_*.txt"))
    if op:
        total = sum(count_lines(f) for f in op)
        out("PASS" if total >= 200 else "WARN",
            f"OpenPhish: {total} URLs across {len(op)} snapshot(s) (aim for 1,000+ across several days)")
    else:
        out("FAIL", "Missing ml/data/raw/openphish/feed_YYYYMMDD.txt")

    uh = glob.glob(p("ml", "data", "raw", "urlhaus", "*.csv"))
    if uh:
        n = sum(count_lines(f, skip_comments=True) for f in uh)
        out("PASS" if n >= 500 else "WARN", f"URLhaus: {n} rows")
    else:
        out("FAIL", "Missing ml/data/raw/urlhaus/*.csv")

    d = p("docs", "DATA.md")
    d_len = 0
    if os.path.exists(d):
        with open(d, encoding="utf-8", errors="ignore") as f:
            d_len = len(f.read())
    if d_len > 300:
        out("PASS", "docs/DATA.md filled in")
    else:
        out("FAIL", "docs/DATA.md missing or too short (source, link, licence, date for each dataset)")


# ------------------------------------------------------------------- rag
OFFICIAL = ["rbi.org.in", "npci.org.in", "cybercrime.gov.in", "i4c.mha.gov.in", "mha.gov.in",
            "pib.gov.in", "sebi.gov.in", "cert-in.org.in", "meity.gov.in", "trai.gov.in",
            "sancharsaathi.gov.in", "india.gov.in", "dot.gov.in"]


def check_rag():
    sp = p("knowledge_base", "sources.csv")
    if not os.path.exists(sp):
        out("FAIL", "Missing knowledge_base/sources.csv")
        return
    with open(sp, encoding="utf-8", errors="ignore") as f:
        rows = list(csv.DictReader(f))
    need = {"file", "title", "publisher", "url", "date_accessed", "topic"}
    cols = set(rows[0].keys()) if rows else set()
    if not need.issubset(cols):
        out("FAIL", "sources.csv columns must be: " + ",".join(sorted(need)))
        return
    out("PASS" if len(rows) >= 8 else "FAIL", f"{len(rows)} sources listed (need >= 8, target 10-12)")
    topics = set()
    for r in rows:
        f = p("knowledge_base", "raw", r["file"].strip())
        if not os.path.exists(f):
            out("FAIL", f"File listed but not found: knowledge_base/raw/{r['file']}")
        elif os.path.getsize(f) < 5000:
            out("WARN", f"File very small (<5KB), is it empty? {r['file']}")
        if not any(dom in r["url"].lower() for dom in OFFICIAL):
            out("WARN", f"URL not from a known official domain: {r['url'][:70]}")
        topics.add(r["topic"].strip().lower())
    listed = {r["file"].strip() for r in rows}
    raw = [os.path.basename(x) for x in glob.glob(p("knowledge_base", "raw", "*")) if os.path.isfile(x)]
    extra = [x for x in raw if x not in listed]
    if extra:
        out("WARN", "Files in raw/ not listed in sources.csv: " + ", ".join(extra[:5]))
    out("PASS" if len(topics) >= 5 else "WARN", f"{len(topics)} distinct topics covered (aim for 6+)")


# ----------------------------------------------------------- handwritten
CATS = {"bank_kyc_account", "upi_payment", "cashback_reward_lottery", "job", "investment",
        "loan", "delivery", "gov_police_impersonation", "tech_support", "other", "benign"}


def check_handwritten():
    hp = p("ml", "data", "handwritten_test.csv")
    if not os.path.exists(hp):
        out("FAIL", "Missing ml/data/handwritten_test.csv")
        return
    with open(hp, encoding="utf-8", errors="ignore") as f:
        rows = list(csv.DictReader(f))
    need = {"text", "label_scam", "category", "has_url"}
    if not rows or not need.issubset(rows[0].keys()):
        out("FAIL", "Columns must be exactly: text,label_scam,category,has_url")
        return
    n = len(rows)
    out("PASS" if n >= 60 else "FAIL", f"{n} rows (need >= 60)")
    scam = sum(1 for r in rows if r["label_scam"].strip() == "1")
    ben = sum(1 for r in rows if r["label_scam"].strip() == "0")
    out("PASS" if scam + ben == n else "FAIL", f"label_scam values valid (scam={scam}, benign={ben})")
    out("PASS" if ben >= 15 else "FAIL", f"{ben} benign rows (need >= 15, include hard negatives)")
    counts = {}
    for r in rows:
        counts[r["category"].strip()] = counts.get(r["category"].strip(), 0) + 1
    bad = [c for c in counts if c not in CATS]
    if bad:
        out("FAIL", "Unknown category labels: " + ", ".join(bad) + "  | allowed: " + ", ".join(sorted(CATS)))
    low = [c for c in CATS - {"benign"} if counts.get(c, 0) < 3]
    out("PASS" if not low else "WARN", "Each scam category has >= 3 rows" if not low
        else "Categories with < 3 rows: " + ", ".join(low))
    texts = [re.sub(r"\W+", " ", r["text"].lower()).strip() for r in rows]
    out("PASS" if len(set(texts)) == n else "FAIL", "No duplicate messages" if len(set(texts)) == n
        else f"{n - len(set(texts))} duplicate messages")
    short = [i + 2 for i, t in enumerate(texts) if len(t) < 20]
    out("PASS" if not short else "WARN", "All messages >= 20 chars" if not short
        else f"Very short messages at CSV lines: {short[:8]}")
    pii = [i + 2 for i, r in enumerate(rows)
           if re.search(r"(?<!\d)[6-9]\d{9}(?!\d)", r["text"]) or re.search(r"[\w.]+@[\w.]+\.\w+", r["text"])]
    out("PASS" if not pii else "WARN", "No real-looking phone numbers/emails" if not pii
        else f"Possible real phone/email (replace with fake) at CSV lines: {pii[:8]}")
    syn = glob.glob(p("ml", "data", "synthetic", "*.csv"))
    if syn:
        syn_texts = set()
        for f in syn:
            with open(f, encoding="utf-8", errors="ignore") as fp:
                for r in csv.DictReader(fp):
                    if r.get("text"):
                        syn_texts.add(re.sub(r"\W+", " ", r["text"].lower()).strip())
        overlap = sum(1 for t in texts if t in syn_texts)
        out("PASS" if overlap == 0 else "FAIL", f"{overlap} handwritten rows also appear in synthetic data (must be 0)")


# ------------------------------------------------------------------ demo
def check_demo():
    dp = p("docs", "demo_inputs.md")
    if os.path.exists(dp):
        with open(dp, encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        items = re.findall(r"^\s*(?:#+\s*)?(\d{1,2})[.)]", txt, re.MULTILINE)
        out("PASS" if len(set(items)) >= 10 else "FAIL", f"docs/demo_inputs.md has {len(set(items))} numbered items (need 10)")
    else:
        out("FAIL", "Missing docs/demo_inputs.md")
    imgs = []
    for ext in ("png", "jpg", "jpeg", "webp"):
        imgs += glob.glob(p("ml", "data", "demo_screenshots", f"*.{ext}"))
    out("PASS" if len(imgs) >= 5 else "FAIL", f"{len(imgs)} demo screenshots (need >= 5)")


CHECKS = {"setup": check_setup, "env": check_env, "data": check_data, "rag": check_rag,
          "handwritten": check_handwritten, "demo": check_demo}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which != "all" and which not in CHECKS:
        print("Usage: validate_my_work.py [" + "|".join(CHECKS) + "|all]")
        sys.exit(2)
    for name, fn in CHECKS.items():
        if which in ("all", name):
            print(f"\n== {name} ==")
            fn()
    print(f"\nSummary: {results['PASS']} pass, {results['WARN']} warn, {results['FAIL']} fail")
    sys.exit(1 if results["FAIL"] else 0)

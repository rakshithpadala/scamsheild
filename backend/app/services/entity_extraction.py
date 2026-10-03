"""Extract structured entities (URLs, phones, emails, UPI IDs) from text.

All patterns are tuned for Indian contexts: +91 numbers, UPI VPA handles,
and common short-code formats.  Returns an ``Entities`` Pydantic model.
"""

from __future__ import annotations

import re

from backend.app.schemas.analysis import Entities

# ── URL ──────────────────────────────────────────────────────────────────────
# Matches http(s) URLs and common bare domains (bit.ly/xxx, example.com/path).
_URL_RE = re.compile(
    r"https?://[^\s<>\"']+|"           # full http(s) URL
    r"(?<!\w)"                          # not preceded by a word char
    r"(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"  # domain
    r"(?:/[^\s<>\"']*)?"               # optional path
    r"(?=\s|$|[.,;:!?\)\]>\"'])",      # followed by delimiter / end
    re.IGNORECASE,
)

# ── Phone (India-focused) ───────────────────────────────────────────────────
# +91-XXXXX-XXXXX | +91 XXXXXXXXXX | 0XX-XXXXXXXX | 10-digit mobile | 1800/1930
_PHONE_RE = re.compile(
    r"\+91[\s.-]?\d{5}[\s.-]?\d{5}"    # +91 with 10 digits
    r"|(?<!\d)0\d{2,4}[\s.-]?\d{6,8}"  # STD code + number
    r"|(?<!\d)[6-9]\d{9}(?!\d)"         # bare 10-digit Indian mobile
    r"|(?<!\d)1800[\s.-]?\d{3}[\s.-]?\d{4,5}"  # toll-free
    r"|(?<!\d)1930(?!\d)",              # national cyber crime helpline
)

# ── Email ────────────────────────────────────────────────────────────────────
_EMAIL_RE = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
)

# ── UPI VPA ──────────────────────────────────────────────────────────────────
# Format: identifier@bankhandle  (e.g. user@ybl, shop@paytm, 9876543210@upi)
_KNOWN_UPI_HANDLES = (
    "upi", "ybl", "paytm", "okhdfcbank", "okicici", "oksbi",
    "okaxis", "apl", "ratn", "idfcfirst", "ikwik", "axl",
    "sbi", "hdfcbank", "icici", "axisbank", "kotak", "indus",
    "barodampay", "mahb", "cbin", "cnrb", "punb", "ibl",
    "fbl", "rbl", "federal", "dlb", "kvb", "jio",
)
_UPI_HANDLE_PATTERN = "|".join(re.escape(h) for h in _KNOWN_UPI_HANDLES)
_UPI_RE = re.compile(
    rf"[a-zA-Z0-9._-]+@(?:{_UPI_HANDLE_PATTERN})(?!\w)",
    re.IGNORECASE,
)


def extract_entities(text: str) -> Entities:
    """Return all entities found in *text*.

    Deduplicates and returns in order of first appearance.
    UPI IDs are distinguished from emails by checking the handle suffix.
    """
    urls: list[str] = []
    phones: list[str] = []
    emails: list[str] = []
    upi_ids: list[str] = []

    seen: set[str] = set()

    # -- UPI first (so we can exclude them from email matches) --
    for m in _UPI_RE.finditer(text):
        val = m.group().lower()
        if val not in seen:
            upi_ids.append(m.group())
            seen.add(val)

    # -- Emails (exclude UPI matches) --
    for m in _EMAIL_RE.finditer(text):
        val = m.group().lower()
        if val not in seen:
            emails.append(m.group())
            seen.add(val)

    # -- URLs --
    for m in _URL_RE.finditer(text):
        val = m.group().rstrip(".,;:!?)>")
        if val.lower() not in seen:
            urls.append(val)
            seen.add(val.lower())

    # -- Phones --
    for m in _PHONE_RE.finditer(text):
        val = m.group()
        normalised = re.sub(r"[\s.-]", "", val)
        if normalised not in seen:
            phones.append(val)
            seen.add(normalised)

    return Entities(urls=urls, phones=phones, emails=emails, upi_ids=upi_ids)

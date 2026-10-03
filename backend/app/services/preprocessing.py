"""Text preprocessing for the analysis pipeline.

Produces two forms:
- ``clean``: normalised text for ML features (lowercased, whitespace-collapsed).
- ``display``: lightly normalised text that preserves casing for UI spans.
"""

from __future__ import annotations

import re
import unicodedata

# Collapse multiple whitespace / newlines into single space
_WS = re.compile(r"\s+")

# Strip zero-width and control chars (keep newlines for display pass)
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u200b-\u200f\u2028-\u202f\ufeff]")


def _normalise_unicode(text: str) -> str:
    """NFC-normalise and strip invisible / control characters."""
    text = unicodedata.normalize("NFC", text)
    return _CTRL.sub("", text)


def preprocess_for_display(raw: str) -> str:
    """Light normalisation: strip control chars, collapse whitespace.

    Preserves original casing so highlighted spans stay readable.
    """
    text = _normalise_unicode(raw)
    text = _WS.sub(" ", text).strip()
    return text


def preprocess_for_ml(raw: str) -> str:
    """Heavier normalisation for ML feature extraction.

    Lower-cased, whitespace-collapsed, control chars removed.
    """
    text = preprocess_for_display(raw).lower()
    return text

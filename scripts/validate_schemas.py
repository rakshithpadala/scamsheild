"""Quick smoke test for preprocessing + entity extraction."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from backend.app.services.entity_extraction import extract_entities
from backend.app.services.preprocessing import preprocess_for_display, preprocess_for_ml

# -- Preprocessing --
raw = "  URGENT!!  Your \u200baccount\u200b  will be BLOCKED  \n\n  immediately!  "
display = preprocess_for_display(raw)
ml = preprocess_for_ml(raw)
assert "URGENT" in display, "display should preserve case"
assert "urgent" in ml, "ml should lowercase"
assert "\u200b" not in display, "should strip zero-width"
assert "  " not in display, "should collapse whitespace"
print(f"  display: {display!r}")
print(f"  ml:      {ml!r}")

# -- Entity extraction --
scam_text = (
    "URGENT: Your SBI account will be blocked! "
    "Update KYC now: http://bit.ly/sbi-kyc-upd "
    "Contact: +91-9876500000 or email support@sbi-verify.com "
    "Pay via UPI: refund@ybl or helpdesk@paytm "
    "Also visit https://fake-sbi.xyz/login "
    "Call 1930 for help."
)
entities = extract_entities(scam_text)
print(f"\n  URLs:    {entities.urls}")
print(f"  Phones:  {entities.phones}")
print(f"  Emails:  {entities.emails}")
print(f"  UPI IDs: {entities.upi_ids}")

assert len(entities.urls) >= 2, f"Expected >=2 URLs, got {entities.urls}"
assert len(entities.phones) >= 2, f"Expected >=2 phones, got {entities.phones}"
assert len(entities.emails) >= 1, f"Expected >=1 email, got {entities.emails}"
assert len(entities.upi_ids) >= 2, f"Expected >=2 UPI IDs, got {entities.upi_ids}"
assert "refund@ybl" in [u.lower() for u in entities.upi_ids], "Should find UPI VPA"
assert "refund@ybl" not in [e.lower() for e in entities.emails], "UPI should not be in emails"

print("\nAll preprocessing + entity extraction tests passed.")

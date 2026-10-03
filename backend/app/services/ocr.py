"""OCR processing service for ScamShield AI.

Applies OpenCV image preprocessing (grayscale, bilateral noise reduction,
Otsu thresholding, optional upscaling) and extracts text using Tesseract OCR
with multi-pass fallback (normal, inverted, grayscale) and word-level confidence.
"""
from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path

import cv2
import numpy as np
import pytesseract

logger = logging.getLogger("ocr_service")

# Configure Tesseract binary path on Windows if needed
if os.name == "nt":
    tesseract_win_path = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    if tesseract_win_path.exists():
        pytesseract.pytesseract.tesseract_cmd = str(tesseract_win_path)
    elif shutil.which("tesseract"):
        pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")


def preprocess_image_array(img: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Preprocesses image array with grayscale, bilateral denoising, and thresholding.

    Returns:
        (thresh, thresh_inverted, gray)
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    # Upscale if image is low resolution (< 900px wide)
    height, width = gray.shape
    if width < 900:
        scale = max(1.5, 900.0 / width)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # Bilateral filter to reduce noise while preserving edges
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)

    # Otsu thresholding for crisp binarization
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh_inv = cv2.bitwise_not(thresh)

    return thresh, thresh_inv, gray


def extract_text_from_bytes(image_bytes: bytes) -> tuple[str, float]:
    """Decodes image bytes (PNG, JPG, WEBP, BMP, etc.), preprocessed, and returns (extracted_text, confidence)."""
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            logger.warning("Failed to decode image from bytes.")
            return "", 0.0

        thresh, thresh_inv, gray = preprocess_image_array(img)

        # Multi-pass strategy: test binarized, inverted, and grayscale
        candidates: list[tuple[str, np.ndarray]] = []

        # Pass 1: standard Otsu binarization
        t1 = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6").strip()
        candidates.append((t1, thresh))

        # Pass 2: if t1 is short, try grayscale directly
        if len(t1) < 40:
            t2 = pytesseract.image_to_string(gray, lang="eng").strip()
            candidates.append((t2, gray))

        # Pass 3: if still short, try inverted (dark mode UI)
        if len(t1) < 40:
            t3 = pytesseract.image_to_string(thresh_inv, lang="eng", config="--psm 6").strip()
            candidates.append((t3, thresh_inv))

        # Select the candidate with highest non-whitespace length
        best_text, best_img = max(candidates, key=lambda c: len(c[0]))

        # Calculate average word confidence
        conf_sum = 0.0
        word_count = 0
        try:
            data = pytesseract.image_to_data(best_img, output_type=pytesseract.Output.DICT)
            confs = data.get("conf", [])
            words = data.get("text", [])
            for c, w in zip(confs, words):
                c_val = float(c)
                if c_val > 0 and str(w).strip():
                    conf_sum += c_val
                    word_count += 1
        except Exception as e:
            logger.debug(f"Confidence calculation exception: {e}")

        avg_conf = (conf_sum / word_count / 100.0) if word_count > 0 else 0.85
        avg_conf = max(0.1, min(0.99, avg_conf))

        clean_text = best_text.strip()
        logger.info(f"OCR extracted {len(clean_text)} chars with {avg_conf:.2f} confidence.")
        return clean_text, round(avg_conf, 4)

    except Exception as e:
        logger.error(f"Error in OCR extraction: {e}")
        return "", 0.0


def extract_text_from_file_path(file_path: str | Path) -> tuple[str, float]:
    """Reads file from path and extracts text."""
    path = Path(file_path)
    if not path.exists():
        return "", 0.0
    with open(path, "rb") as f:
        return extract_text_from_bytes(f.read())

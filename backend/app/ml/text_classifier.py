"""Inference module for ScamShield AI text classification.

Loads trained text binary model and multi-class category model from ml/artifacts/
to provide real-time scam probability and scam category predictions with confidence scores.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib

logger = logging.getLogger("text_classifier")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
ARTIFACTS_DIR = ROOT_DIR / "ml" / "artifacts"

BINARY_MODEL_PATH = ARTIFACTS_DIR / "text_binary_model.joblib"
CATEGORY_MODEL_PATH = ARTIFACTS_DIR / "category_model.joblib"


class TextScamClassifier:
    """Inference wrapper for binary scam vs ham classification."""

    def __init__(self, model_path: Path = BINARY_MODEL_PATH) -> None:
        self.model_path = model_path
        self.vectorizer: Any = None
        self.classifier: Any = None
        self.model_name: str = "FallbackHeuristic"
        self._load_model()

    def _load_model(self) -> None:
        if self.model_path.exists():
            try:
                data = joblib.load(self.model_path)
                self.vectorizer = data.get("vectorizer")
                self.classifier = data.get("classifier")
                self.model_name = data.get("model_name", "TrainedBinaryModel")
                logger.info(f"Loaded binary text model: {self.model_name}")
            except Exception as e:
                logger.warning(f"Could not load binary model from {self.model_path}: {e}")
        else:
            logger.info(f"Binary model file not found at {self.model_path}. Using rule fallback.")

    def predict_proba(self, text: str) -> float:
        """Returns scam probability between 0.0 and 1.0."""
        if self.vectorizer is not None and self.classifier is not None:
            try:
                X = self.vectorizer.transform([text])
                if hasattr(self.classifier, "predict_proba"):
                    proba = float(self.classifier.predict_proba(X)[0][1])
                elif hasattr(self.classifier, "decision_function"):
                    df = float(self.classifier.decision_function(X)[0])
                    proba = 1.0 / (1.0 + float(2.71828 ** (-df)))
                else:
                    proba = float(self.classifier.predict(X)[0])
                return max(0.0, min(1.0, proba))
            except Exception as e:
                logger.error(f"Error predicting scam probability: {e}")
        return 0.5


class CategoryClassifier:
    """Inference wrapper for multi-class scam category classification."""

    def __init__(self, model_path: Path = CATEGORY_MODEL_PATH) -> None:
        self.model_path = model_path
        self.model_type: str = "fallback"
        self.classifier: Any = None
        self.vectorizer: Any = None
        self.embedder: Any = None
        self.classes: list[str] = []
        self._load_model()

    def _load_model(self) -> None:
        if self.model_path.exists():
            try:
                data = joblib.load(self.model_path)
                self.model_type = data.get("model_type", "tfidf")
                self.classifier = data.get("classifier")
                self.classes = data.get("classes", [])
                if self.model_type == "minilm_embeddings":
                    from sentence_transformers import SentenceTransformer
                    self.embedder = SentenceTransformer(data.get("embedder_name", "all-MiniLM-L6-v2"))
                elif self.model_type == "tfidf":
                    self.vectorizer = data.get("vectorizer")
                logger.info(f"Loaded category model: {self.model_type} ({len(self.classes)} classes)")
            except Exception as e:
                logger.warning(f"Could not load category model from {self.model_path}: {e}")
        else:
            logger.info(f"Category model file not found at {self.model_path}.")

    def predict_category(self, text: str) -> tuple[str, float]:
        """Returns (predicted_category, confidence_score)."""
        if self.classifier is not None:
            try:
                if self.model_type == "minilm_embeddings" and self.embedder is not None:
                    emb = self.embedder.encode([text], show_progress_bar=False, normalize_embeddings=True)
                    probas = self.classifier.predict_proba(emb)[0]
                elif self.vectorizer is not None:
                    X = self.vectorizer.transform([text])
                    probas = self.classifier.predict_proba(X)[0]
                else:
                    probas = None

                if probas is not None:
                    best_idx = int(probas.argmax())
                    cat_name = self.classes[best_idx] if best_idx < len(self.classes) else "other"
                    conf = float(probas[best_idx])
                    return cat_name, round(conf, 4)
            except Exception as e:
                logger.error(f"Error predicting category: {e}")

        return "other", 0.5


# Singleton instances
_binary_classifier: TextScamClassifier | None = None
_category_classifier: CategoryClassifier | None = None


def get_binary_classifier() -> TextScamClassifier:
    global _binary_classifier
    if _binary_classifier is None:
        _binary_classifier = TextScamClassifier()
    return _binary_classifier


def get_category_classifier() -> CategoryClassifier:
    global _category_classifier
    if _category_classifier is None:
        _category_classifier = CategoryClassifier()
    return _category_classifier


from pathlib import Path

import joblib


MODEL_PATH = Path(__file__).resolve().parents[2] / "models/balanced.joblib"

# Charger le modèle une seule fois
model = joblib.load(MODEL_PATH)

SENTIMENTS = {
    -1: "negative",
    0: "neutral",
    1: "positive"
}


def predict(comments):
    labels = model.predict(comments)
    probabilities = model.predict_proba(comments)

    predictions = []

    for text, label, probs in zip(comments, labels, probabilities):
        predictions.append({
            "text": text,
            "label": int(label),
            "sentiment": SENTIMENTS[int(label)],
            "confidence": round(float(max(probs)), 4)
        })

    # Statistiques globales
    counts = {
        sentiment: sum(p["sentiment"] == sentiment for p in predictions)
        for sentiment in SENTIMENTS.values()
    }

    total = len(predictions)

    percentages = {
        sentiment: round(count / total * 100, 2)
        for sentiment, count in counts.items()
    }

    return {
        "total": total,
        "predictions": predictions,
        "statistics": {
            "counts": counts,
            "percentages": percentages
        }
    }

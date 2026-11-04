
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Charger les données d'entraînement
df = pd.read_csv("data/processed/train.csv")

# Garder le test final de côté pendant l'optimisation
X_train, X_val, y_train, y_val = train_test_split(
    df["text"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

# Pipeline ML
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 2),
        min_df=2
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
            class_weight="balanced"

    ))
])

# Entraînement
print("Entraînement en cours...")
model.fit(X_train, y_train)

# Évaluation sur validation
y_pred = model.predict(X_val)

print("\nAccuracy :", accuracy_score(y_val, y_pred))
print("\nRapport de classification :")
print(classification_report(y_val, y_pred))

# Sauvegarder le pipeline complet
joblib.dump(model, "models/balanced.joblib")
print("\nModèle sauvegardé !")

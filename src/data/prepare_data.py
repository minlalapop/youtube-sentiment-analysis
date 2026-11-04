
import pandas as pd
import re

# Charger le dataset
df = pd.read_csv("data/raw/reddit.csv")

# Renommer les colonnes
df = df.rename(columns={
    "clean_comment": "text",
    "category": "label"
})

# Supprimer les valeurs manquantes
df = df.dropna(subset=["text", "label"])

# Nettoyage des commentaires
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^\w\s!?']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["text"] = df["text"].apply(clean_text)

# Supprimer les textes vides et doublons
df = df[df["text"] != ""]
df = df.drop_duplicates(subset=["text", "label"])

# Sauvegarder
df.to_csv("data/processed/reddit_clean.csv", index=False)

# Statistiques
print("Nombre de commentaires après nettoyage :", len(df))
print("\nDistribution des labels :")
print(df["label"].value_counts().sort_index())
print("\nValeurs manquantes :")
print(df.isnull().sum())
print("\nPremières lignes :")
print(df.head())

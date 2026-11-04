
import pandas as pd
from sklearn.model_selection import train_test_split

# Charger les données nettoyées
df = pd.read_csv("data/processed/reddit_clean.csv")

# Séparer les données
train, test = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

# Sauvegarder
train.to_csv("data/processed/train.csv", index=False)
test.to_csv("data/processed/test.csv", index=False)

# Statistiques
print("Train :", len(train), "commentaires")
print("Test :", len(test), "commentaires")

print("\nDistribution Train (%) :")
print(train["label"].value_counts(normalize=True).sort_index() * 100)

print("\nDistribution Test (%) :")
print(test["label"].value_counts(normalize=True).sort_index() * 100)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

df = pd.read_csv("data/processed/reddit_clean.csv")

Path("reports/figures").mkdir(parents=True, exist_ok=True)

# 1. Distribution des sentiments
print("Distribution des sentiments (%) :")
print(df["label"].value_counts(normalize=True).sort_index() * 100)

plt.figure(figsize=(7, 4))
sns.countplot(data=df, x="label", order=[-1, 0, 1])
plt.title("Distribution des sentiments")
plt.xlabel("Sentiment (-1 : négatif, 0 : neutre, 1 : positif)")
plt.ylabel("Nombre de commentaires")
plt.tight_layout()
plt.savefig("reports/figures/sentiments.png")
plt.show()

# 2. Longueur des commentaires
df["length"] = df["text"].str.split().str.len()

print("\nStatistiques sur la longueur des commentaires :")
print(df["length"].describe())

plt.figure(figsize=(7, 4))
sns.histplot(df["length"], bins=50)
plt.title("Distribution de la longueur des commentaires")
plt.xlabel("Nombre de mots")
plt.ylabel("Nombre de commentaires")
plt.tight_layout()
plt.savefig("reports/figures/longueurs.png")
plt.show()

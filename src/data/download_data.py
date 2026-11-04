
import pandas as pd
import requests
from pathlib import Path

URL = "https://raw.githubusercontent.com/Himanshu-1703/reddit-sentiment-analysis/refs/heads/main/data/reddit.csv"
OUTPUT = Path("data/raw/reddit.csv")

# download dataset
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

response = requests.get(URL, timeout=60)
response.raise_for_status()
OUTPUT.write_bytes(response.content)

print("Dataset téléchargé !")

# charger les données
df = pd.read_csv(OUTPUT)

# Stats
print("\nNombre de commentaires :", len(df))
print("\nColonnes :", df.columns.tolist())
print("\nDistribution des sentiments :")
print(df["category"].value_counts().sort_index())

print("\nPremières lignes :")
print(df.head())

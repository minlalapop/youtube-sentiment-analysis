
import pandas as pd
import joblib
import time

model = joblib.load("models/balanced.joblib")
df = pd.read_csv("data/processed/test.csv")

# Batch de 50 commentaires
comments = df["text"].head(50).tolist()

# Préchauffage
model.predict(comments)

# Mesure sur 100 répétitions
times = []

for _ in range(100):
    start = time.perf_counter()
    model.predict(comments)
    times.append((time.perf_counter() - start) * 1000)

print(f"Temps moyen : {sum(times)/len(times):.2f} ms")
print(f"Temps maximum : {max(times):.2f} ms")
print(f"Temps minimum : {min(times):.2f} ms")

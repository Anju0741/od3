import pandas as pd
import json

INPUT = "data/processed/bindingdb_final.csv"
OUTPUT = "data/processed/drug_metadata.json"

df = pd.read_csv(INPUT)

# Keep only rows with names
df = df.dropna(subset=["Ligand SMILES", "Ligand Name"])

# Build mapping
drug_map = (
    df.groupby("Ligand SMILES")["Ligand Name"]
    .first()
    .to_dict()
)

with open(OUTPUT, "w") as f:
    json.dump(drug_map, f, indent=2)

print(f"[✓] Saved {len(drug_map)} drug names")

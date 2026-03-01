# src/preprocessing/build_protein_index.py

import pandas as pd
import torch
from pathlib import Path

INPUT_FILE = "data/processed/bindingdb_final.csv"
OUT_FILE = "data/processed/protein_index.pt"

def main():
    print("[+] Loading BindingDB final...")
    df = pd.read_csv(INPUT_FILE, usecols=[
        "UniProt (SwissProt) Primary ID of Target Chain 1"
    ])

    proteins = df["UniProt (SwissProt) Primary ID of Target Chain 1"].dropna().unique()
    proteins = sorted(proteins)

    protein2idx = {p: i for i, p in enumerate(proteins)}

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    torch.save(protein2idx, OUT_FILE)

    print(f"[✓] Total unique proteins: {len(protein2idx)}")
    print(f"[✓] Saved protein index to {OUT_FILE}")

if __name__ == "__main__":
    main()

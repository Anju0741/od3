# src/preprocessing/normalize_activity.py

"""
Normalize BindingDB activity values into a single numeric label.
Priority: Ki > IC50 > Kd > EC50
Output: data/processed/bindingdb_final.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = Path("data/processed/bindingdb_clean.csv")
OUTPUT_FILE = Path("data/processed/bindingdb_final.csv")

ACTIVITY_COLS = [
    "Ki (nM)",
    "IC50 (nM)",
    "Kd (nM)",
    "EC50 (nM)",
]


def pick_activity(row):
    for col in ACTIVITY_COLS:
        val = row.get(col)
        if pd.notna(val):
            try:
                val = float(val)
                if val > 0:
                    return val
            except ValueError:
                continue
    return np.nan


def main():
    print("[+] Loading cleaned BindingDB...")
    df = pd.read_csv(INPUT_FILE, low_memory=False)

    print("[+] Selecting activity value...")
    df["activity_nM"] = df.apply(pick_activity, axis=1)

    before = len(df)
    df = df.dropna(subset=["activity_nM"])
    after = len(df)

    print(f"[+] Dropped {before - after} rows without activity")

    # log-transform (standard in bioactivity modeling)
    df["pActivity"] = -np.log10(df["activity_nM"] * 1e-9)

    keep_cols = [
        "Ligand SMILES",
        "UniProt (SwissProt) Primary ID of Target Chain 1",
        "activity_nM",
        "pActivity",
    ]

    df_final = df[keep_cols]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False)

    print("[✓] Saved:", OUTPUT_FILE)
    print(df_final.head())
    print("Total rows:", len(df_final))


if __name__ == "__main__":
    main()
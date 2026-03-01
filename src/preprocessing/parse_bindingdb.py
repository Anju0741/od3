import pandas as pd
import os

INPUT_FILE = "../data/raw/bindingdb.tsv"
OUTPUT_DIR = "../data/processed"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "bindingdb_clean.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

CHUNK_SIZE = 50_000  # safe for laptops
WRITE_HEADER = True

columns_needed = [
    "Ligand SMILES",
    "BindingDB Ligand Name",
    "Target Name",
    "Ki (nM)",
    "IC50 (nM)",
    "Kd (nM)",
    "EC50 (nM)",
    "UniProt (SwissProt) Primary ID of Target Chain 1"
]

print("📥 Loading BindingDB in chunks...")

for chunk in pd.read_csv(
    INPUT_FILE,
    sep="\t",
    chunksize=CHUNK_SIZE,
    low_memory=True
):
    # keep only needed columns that exist
    existing_cols = [c for c in columns_needed if c in chunk.columns]
    chunk = chunk[existing_cols]

    # drop rows with no binding value
    chunk = chunk.dropna(
        subset=["Ki (nM)", "IC50 (nM)", "Kd (nM)", "EC50 (nM)"],
        how="all"
    )

    if len(chunk) == 0:
        continue

    chunk.to_csv(
        OUTPUT_FILE,
        mode="a",
        index=False,
        header=WRITE_HEADER
    )

    WRITE_HEADER = False

print("✅ Finished processing BindingDB")
print(f"📄 Output saved to: {OUTPUT_FILE}")

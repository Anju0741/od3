# src/preprocessing/encode_drugs.py

import torch
import os
from tqdm import tqdm
from src.models.molecular_encoder import MolecularEncoder

GRAPH_FILE = "data/processed/drug_graphs.pt"
OUT_FILE = "data/processed/drug_embeddings.pt"
CKPT_FILE = "data/processed/encode_checkpoint.txt"

BATCH_SIZE = 256
DEVICE = "cpu"

def load_checkpoint():
    if os.path.exists(CKPT_FILE):
        with open(CKPT_FILE) as f:
            return int(f.read().strip())
    return 0

def save_checkpoint(idx):
    with open(CKPT_FILE, "w") as f:
        f.write(str(idx))

def main():
    print("[+] Loading graph keys only...")
    graphs = torch.load(GRAPH_FILE, map_location="cpu")
    smiles_list = list(graphs.keys())

    start_idx = load_checkpoint()
    print(f"[+] Resuming from index {start_idx}")

    encoder = MolecularEncoder().to(DEVICE)
    encoder.eval()

    embeddings = {}
    
    if os.path.exists(OUT_FILE):
        try:
            embeddings = torch.load(OUT_FILE)
        except Exception:
            print("[!] Corrupted embedding file detected. Recreating embeddings file.")
            embeddings = {}


    with torch.no_grad():
        for i in tqdm(range(start_idx, len(smiles_list), BATCH_SIZE)):
            batch = smiles_list[i:i+BATCH_SIZE]

            for smi in batch:
                if smi in embeddings:
                    continue

                g = graphs[smi]
                x = g["x"]
                edge_index = g["edge_index"]

# 🚨 Skip graphs with no edges
                if edge_index.numel() == 0:
                    continue

                batch = torch.zeros(x.size(0), dtype=torch.long)

                emb = encoder(x, edge_index, batch)

                embeddings[smi] = emb.squeeze(0).cpu()

            torch.save(embeddings, OUT_FILE)
            save_checkpoint(i + BATCH_SIZE)

    print("[✓] Encoding completed!")

if __name__ == "__main__":
    main()

# src/models/test_encoder.py

import torch
from molecular_encoder import MolecularEncoder

print("[+] Loading graph file (partial)...")

graphs = torch.load(
    "data/processed/drug_graphs.pt",
    map_location="cpu"
)

# take only ONE graph
smiles = next(iter(graphs))
g = graphs[smiles]

x = g["x"]
edge_index = g["edge_index"]

batch = torch.zeros(x.size(0), dtype=torch.long)

model = MolecularEncoder()
embedding = model(x, edge_index, batch)

print("SMILES:", smiles)
print("Embedding shape:", embedding.shape)

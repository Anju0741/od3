# src/preprocessing/rdkit_to_graph.py

import torch
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdchem
from pathlib import Path
from tqdm import tqdm
import os

INPUT_FILE = Path("data/processed/bindingdb_final.csv")
OUTPUT_FILE = Path("data/processed/drug_graphs.pt")
BATCH_SIZE = 5000   

def atom_features(atom: rdchem.Atom):
    return [
        atom.GetAtomicNum(),
        atom.GetTotalDegree(),
        atom.GetFormalCharge(),
        int(atom.GetIsAromatic()),
        atom.GetTotalNumHs(),
    ]


def bond_features(bond: rdchem.Bond):
    bt = bond.GetBondType()
    return [
        int(bt == rdchem.BondType.SINGLE),
        int(bt == rdchem.BondType.DOUBLE),
        int(bt == rdchem.BondType.TRIPLE),
        int(bt == rdchem.BondType.AROMATIC),
    ]


def smiles_to_graph(smiles):
    if pd.isna(smiles):
        return None
    smiles = str(smiles)  # convert float/NaN to string safely
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # Node features
    x = [atom_features(a) for a in mol.GetAtoms()]
    x = torch.tensor(x, dtype=torch.float)

    # Edge features
    edge_index, edge_attr = [], []
    for bond in mol.GetBonds():
        i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        bf = bond_features(bond)
        edge_index += [[i, j], [j, i]]
        edge_attr += [bf, bf]

    return {
        "x": x,
        "edge_index": torch.tensor(edge_index).t().contiguous(),
        "edge_attr": torch.tensor(edge_attr, dtype=torch.float),
    }

def main():
    print("[+] Loading BindingDB final dataset...")
    df = pd.read_csv(INPUT_FILE)
    smiles_list = df["Ligand SMILES"].unique()

    print(f"[+] Total unique SMILES: {len(smiles_list)}")

    # Resume if file exists
    if OUTPUT_FILE.exists():
        print("[+] Existing graph file found. Loading...")
        graphs = torch.load(OUTPUT_FILE)
    else:
        graphs = {}

    start = len(graphs)
    print(f"[+] Resuming from index: {start}")

    for i in range(start, len(smiles_list), BATCH_SIZE):
        batch = smiles_list[i : i + BATCH_SIZE]
        print(f"[+] Processing batch {i} → {i + len(batch)}")

        for smi in tqdm(batch, leave=False):
            if smi in graphs:
                continue
            g = smiles_to_graph(smi)
            if g is not None:
                graphs[smi] = g

        # incremental save
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        torch.save(graphs, OUTPUT_FILE)
        print(f"[✓] Saved checkpoint with {len(graphs)} graphs")

    print("[✓✓✓] All SMILES processed successfully")


if __name__ == "__main__":
    main()
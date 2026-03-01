# src/training/evaluate.py

import torch
from src.models.drug_target_model import DrugTargetModel

EMB_FILE = "data/processed/drug_embeddings.pt"
PROTEIN_INDEX_FILE = "data/processed/protein_index.pt"
MODEL_FILE = "data/processed/drug_target_model.pt"


def main():
    print("[+] Loading embeddings...")
    drug_embeddings = torch.load(EMB_FILE)

    print("[+] Loading protein index...")
    protein_index = torch.load(PROTEIN_INDEX_FILE)
    num_proteins = len(protein_index)

    print(f"[+] Total proteins: {num_proteins}")

    print("[+] Loading model...")
    model = DrugTargetModel(num_proteins=num_proteins)
    model.load_state_dict(torch.load(MODEL_FILE))
    model.eval()

    # 🔍 Example evaluation (demo)
    sample_drug = next(iter(drug_embeddings.values()))
    sample_protein_id = 0  # first protein

    with torch.no_grad():
        score = model(
            sample_drug.unsqueeze(0),
            torch.tensor([sample_protein_id])
        )

    print(f"[✓] Sample binding score: {score.item():.4f}")


if __name__ == "__main__":
    main()

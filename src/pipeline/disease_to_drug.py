# src/pipeline/disease_to_drug.py

# src/pipeline/disease_to_drug.py

import torch
import pandas as pd
from src.models.drug_target_model import DrugTargetModel

DRUG_EMB_FILE = "data/processed/drug_embeddings.pt"
PROTEIN_INDEX_FILE = "data/processed/protein_index.pt"
MODEL_FILE = "data/processed/drug_target_model.pt"
DISEASE_GENES_FILE = "data/raw/orphanet.json"

TOP_K = 10


# -----------------------------
# Helper: load disease → proteins
# -----------------------------
def load_disease_proteins(disease_name):
    """
    Returns list of protein IDs (indices) associated with a disease
    """
    df = pd.read_json(DISEASE_GENES_FILE)
    # Example: your JSON might have {"disease_name": [gene1, gene2,...]}
    if disease_name not in df:
        raise ValueError(f"Disease '{disease_name}' not found in dataset.")
    
    gene_list = df[disease_name]
    protein_index = torch.load(PROTEIN_INDEX_FILE)
    
    # Map gene symbols to protein indices
    protein_ids = []
    for gene in gene_list:
        if gene in protein_index:
            protein_ids.append(protein_index[gene])
    return protein_ids

# -----------------------------
# Main pipeline
# -----------------------------
def main(disease_name):
    print(f"[+] Loading drug embeddings...")
    drug_embeddings = torch.load(DRUG_EMB_FILE)
    print(f"[+] Total drugs: {len(drug_embeddings)}")

    print(f"[+] Loading protein index...")
    protein_index = torch.load(PROTEIN_INDEX_FILE)
    num_proteins = len(protein_index)
    print(f"[+] Total proteins: {num_proteins}")

    print(f"[+] Loading model...")
    model = DrugTargetModel(num_proteins=num_proteins)
    model.load_state_dict(torch.load(MODEL_FILE))
    model.eval()

    print(f"[+] Finding proteins associated with disease: {disease_name}")
    protein_ids = load_disease_proteins(disease_name)
    if not protein_ids:
        print("No proteins found for this disease. Exiting.")
        return

    print(f"[+] {len(protein_ids)} proteins found. Running predictions...")

    # Compute scores
    results = []
    with torch.no_grad():
        for drug_name, drug_emb in drug_embeddings.items():
            scores = []
            for pid in protein_ids:
                score = model(drug_emb.unsqueeze(0), torch.tensor([pid]))
                scores.append(score.item())
            avg_score = sum(scores)/len(scores)
            results.append((drug_name, avg_score))

    # Sort and get top K
    results.sort(key=lambda x: x[1], reverse=True)
    print(f"[✓] Top {TOP_K} drugs for '{disease_name}':")
    for i, (drug, score) in enumerate(results[:TOP_K], 1):
        print(f"{i}. {drug} → {score:.4f}")

if __name__ == "__main__":
    # Example usage
    disease_input = input("Enter disease name: ")
    main(disease_input)

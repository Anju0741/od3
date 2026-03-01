import json
import os
import torch
from tqdm import tqdm
from src.models.drug_target_model import DrugTargetModel

# =============================
# PATHS
# =============================
ORPHANET_JSON = "data/processed/orphanet_protein_index.json"
DRUG_EMB_FILE = "data/processed/drug_embeddings.pt"
MODEL_FILE = "data/processed/drug_target_model.pt"
PROTEIN_INDEX_FILE = "data/processed/protein_index.pt"

CACHE_DIR = "data/processed/cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# =============================
# LOAD ONCE (GLOBAL)
# =============================
print("[INIT] Loading disease → protein mapping...")
with open(ORPHANET_JSON) as f:
    disease_proteins = json.load(f)

print("[INIT] Loading protein index...")
protein_index = torch.load(PROTEIN_INDEX_FILE)

print("[INIT] Loading drug embeddings...")
drug_embeddings = torch.load(DRUG_EMB_FILE)

print("[INIT] Loading trained model...")
num_proteins = len(protein_index)
model = DrugTargetModel(num_proteins)
model.load_state_dict(torch.load(MODEL_FILE, map_location="cpu"))
model.eval()

print("[INIT] System ready.")


# =============================
# UTILS
# =============================
def cache_path(disease_name):
    safe = disease_name.replace(" ", "_").lower()
    return f"{CACHE_DIR}/{safe}_results.json"


# =============================
# CORE ML SCORING (PURE LOGIC)
# =============================
def compute_drug_scores(disease_name):
    protein_indices = disease_proteins[disease_name]

    drug_scores = {}

    with torch.no_grad():
        for drug, drug_emb in tqdm(
            drug_embeddings.items(),
            desc="Predicting drugs"
        ):
            scores = []
            for prot_idx in protein_indices:
                prot_tensor = torch.tensor([prot_idx])
                score = model(drug_emb.unsqueeze(0), prot_tensor)
                scores.append(score.item())

            drug_scores[drug] = sum(scores) / len(scores)

    return sorted(drug_scores.items(), key=lambda x: x[1], reverse=True)


# =============================
# MAIN PIPELINE FUNCTION
# =============================
def predict_drugs_for_disease(disease_name, top_k=10):
    if disease_name not in disease_proteins:
        return {
            "error": f"Disease '{disease_name}' not found or has no mapped proteins"
        }

    path = cache_path(disease_name)

    # ---------- FAST PATH (CACHE) ----------
    if os.path.exists(path):
        with open(path) as f:
            cached = json.load(f)

        return {
            "disease": disease_name,
            "cached": True,
            "top_drugs": cached[:top_k]
        }

    # ---------- SLOW PATH (FIRST TIME) ----------
    sorted_drugs = compute_drug_scores(disease_name)

    formatted = [
        {"smiles": d, "score": round(s, 4)}
        for d, s in sorted_drugs
    ]

    # Save cache
    with open(path, "w") as f:
        json.dump(formatted, f, indent=2)

    return {
        "disease": disease_name,
        "cached": False,
        "top_drugs": formatted[:top_k]
    }


# =============================
# CLI ENTRY (OPTIONAL)


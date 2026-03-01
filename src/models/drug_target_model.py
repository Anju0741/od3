import torch
import torch.nn as nn

class DrugTargetModel(nn.Module):
    def __init__(self, num_proteins, drug_dim=128, protein_dim=64):
        super().__init__()

        # Protein embedding layer
        self.protein_emb = nn.Embedding(num_proteins, protein_dim)

        # Prediction network (NO SIGMOID HERE)
        self.mlp = nn.Sequential(
            nn.Linear(drug_dim + protein_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),        # prevents overfitting
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)       # raw logits
        )

    def forward(self, drug_emb, protein_idx):
        prot_emb = self.protein_emb(protein_idx)
        x = torch.cat([drug_emb, prot_emb], dim=1)
        return self.mlp(x).squeeze()

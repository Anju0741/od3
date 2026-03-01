import torch
import pandas as pd
import random
from torch.utils.data import Dataset, DataLoader
from src.models.drug_target_model import DrugTargetModel

EMB_FILE = "data/processed/drug_embeddings.pt"
PROT_INDEX_FILE = "data/processed/protein_index.pt"
BIND_FILE = "data/processed/bindingdb_final.csv"

BATCH_SIZE = 256
EPOCHS = 20
LR = 1e-3


class BindingDataset(Dataset):
    def __init__(self):
        self.df = pd.read_csv(BIND_FILE)
        self.embeddings = torch.load(EMB_FILE)
        self.protein2idx = torch.load(PROT_INDEX_FILE)
        self.num_proteins = len(self.protein2idx)

        # keep only valid rows
        self.df = self.df[
            self.df["Ligand SMILES"].isin(self.embeddings)
            & self.df["UniProt (SwissProt) Primary ID of Target Chain 1"].isin(self.protein2idx)
        ].reset_index(drop=True)

    def __len__(self):
        return len(self.df) * 2  # positive + negative

    def __getitem__(self, idx):
        row = self.df.iloc[idx // 2]
        drug_emb = self.embeddings[row["Ligand SMILES"]]

        # positive sample
        if idx % 2 == 0:
            prot_idx = self.protein2idx[row["UniProt (SwissProt) Primary ID of Target Chain 1"]]
            label = 1.0

        # negative sample (random protein)
        else:
            prot_idx = random.randint(0, self.num_proteins - 1)
            label = 0.0

        return drug_emb, torch.tensor(prot_idx), torch.tensor(label)


def main():
    dataset = BindingDataset()
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = DrugTargetModel(num_proteins=len(torch.load(PROT_INDEX_FILE)))
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = torch.nn.BCEWithLogitsLoss()

    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0
        for drug_emb, prot_idx, label in loader:
            optimizer.zero_grad()
            logits = model(drug_emb, prot_idx)
            loss = loss_fn(logits.squeeze(), label)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}: Loss = {total_loss/len(loader):.4f}")

    torch.save(model.state_dict(), "data/processed/drug_target_model.pt")
    print("[✓] Model trained & saved")


if __name__ == "__main__":
    main()

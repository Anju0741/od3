# src/models/molecular_encoder.py

import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, global_mean_pool

class MolecularEncoder(nn.Module):
    def __init__(self, in_dim=5, hidden_dim=64, out_dim=128):
        super().__init__()

        self.conv1 = GCNConv(in_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)

        self.mlp = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim)
        )

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index)
        x = torch.relu(x)

        x = self.conv2(x, edge_index)
        x = torch.relu(x)

        x = global_mean_pool(x, batch)
        return self.mlp(x)

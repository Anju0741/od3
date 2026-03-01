# src/preprocessing/build_heterograph.py
from torch_geometric.data import HeteroData
import torch
import pandas as pd

def build_hetero(drugs_df, targets_df, ppi_df, disease_genes_df):
    data = HeteroData()
    # drug nodes
    data["drug"].x = torch.tensor(drugs_df['embedding'].tolist())  # fill with molecular encoder later
    # protein nodes
    data["protein"].x = torch.tensor([...])  # protein embeddings or one-hot
    # gene/disease nodes...
    # edges:
    data["drug", "binds", "protein"].edge_index = torch.tensor([...])
    data["protein", "interacts", "protein"].edge_index = torch.tensor([...])
    data["gene", "assoc", "disease"].edge_index = torch.tensor([...])
    return data

# src/preprocessing/parse_orphanet_uniprot_fixed.py

import json
from lxml import etree
import torch

ORPHANET_XML = "data/raw/en_product6.xml"
PROTEIN_INDEX_FILE = "data/processed/protein_index.pt"
OUTPUT_JSON = "data/processed/orphanet_protein_index.json"

def parse_orphanet(xml_file):
    """Parse Orphanet XML to extract disease → UniProt IDs"""
    tree = etree.parse(xml_file)
    root = tree.getroot()
    disease_uniprot = {}

    for disorder in root.xpath("//Disorder"):
        # disease name
        name_elem = disorder.xpath(".//Name[@lang='en']")
        if not name_elem or not name_elem[0].text:
            continue
        disease_name = name_elem[0].text.strip()

        uniprot_ids = set()
        # iterate all DisorderGeneAssociations
        for dga in disorder.xpath(".//DisorderGeneAssociation"):
            gene = dga.find("Gene")
            if gene is None:
                continue
            # iterate all ExternalReference
            for era in gene.xpath(".//ExternalReference"):
                source = era.find("Source")
                ref = era.find("Reference")
                if source is not None and ref is not None:
                    if source.text.strip() == "SwissProt" and ref.text:
                        uniprot_ids.add(ref.text.strip())

        if uniprot_ids:
            disease_uniprot[disease_name] = list(uniprot_ids)

    return disease_uniprot

def map_uniprot_to_index(disease_uniprot, protein_index):
    """Map UniProt IDs → protein indices"""
    disease_proteins = {}
    for disease, uniprot_list in disease_uniprot.items():
        indices = [protein_index[uid] for uid in uniprot_list if uid in protein_index]
        if indices:
            disease_proteins[disease] = indices
    return disease_proteins

def main():
    print("[+] Loading protein index...")
    protein_index = torch.load(PROTEIN_INDEX_FILE)

    print("[+] Parsing Orphanet XML...")
    disease_uniprot = parse_orphanet(ORPHANET_XML)
    print(f"[+] Found {len(disease_uniprot)} diseases with UniProt IDs.")

    print("[+] Mapping UniProt IDs to protein indices...")
    disease_proteins = map_uniprot_to_index(disease_uniprot, protein_index)
    print(f"[+] {len(disease_proteins)} diseases have mapped proteins in protein index.")

    print("[+] Saving JSON...")
    with open(OUTPUT_JSON, "w") as f:
        json.dump(disease_proteins, f, indent=2)
    print(f"[✓] Saved disease → protein index JSON to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()

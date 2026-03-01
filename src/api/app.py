from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.disease_to_drug import predict_drugs_for_disease

app = FastAPI(title="OD3 Drug Repurposing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiseaseRequest(BaseModel):
    disease_name: str

@app.post("/predict")
def predict(request: DiseaseRequest):
    return predict_drugs_for_disease(request.disease_name)

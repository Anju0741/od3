export async function predictDrugs(disease) {
  const response = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ disease })
  });

  if (!response.ok) {
    throw new Error("Prediction failed");
  }

  return response.json();
}

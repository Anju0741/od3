const API_URL = "http://127.0.0.1:8000";

export async function predictDrugs(diseaseName) {
  const response = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      disease_name: diseaseName,
    }),
  });

  if (!response.ok) {
    throw new Error("API request failed");
  }

  return await response.json();
}

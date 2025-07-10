import requests
import pandas as pd

API_KEY = "0457925dbd7e447f93154dae6a42bbbb"
url = "https://api.spoonacular.com/recipes/complexSearch"

params = {
    "apiKey": API_KEY,
    "diet": "vegan",
    "number": 50,
    "addRecipeInformation": True
}
#Se ha guardado en un json las recetas veganas
response = requests.get(url, params=params)
data = response.json()

recetas = data.get("results", [])
df = pd.DataFrame(recetas)
df.to_json("assets/data/recetas_veganas.json", orient="records", indent=2, force_ascii=False)
print(f"✅ Guardadas {len(df)} recetas veganas")

#Análisis exploratorio básico
import json
import os
import matplotlib.pyplot as plt


with open("assets/data/recetas_veganas.json", encoding="utf-8") as f:
    recetas = json.load(f)

print(f"Cantidad total de recetas: {len(recetas)}")
print("Claves disponibles en cada receta:", recetas[0].keys())

#Recetas del JSON en un DataFrame

with open("assets/data/recetas_veganas.json", encoding="utf-8") as f:
    recetas = json.load(f)

df = pd.DataFrame([{
    "title": r.get("title"),
    "readyInMinutes": r.get("readyInMinutes"),
    "healthScore": r.get("healthScore", 0),
    "pricePerServing": r.get("pricePerServing"),
    "likes": r.get("aggregateLikes"),
    "dishTypes": r.get("dishTypes"),
    "diets": r.get("diets")
} for r in recetas])


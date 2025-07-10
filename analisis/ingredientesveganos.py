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

#MÁS LIKES------------------------------------------------------------------------------

top_likes = df.sort_values(by="likes", ascending=False).head(10)
print(top_likes[["title", "likes"]])

#GRAFICO
top_likes = df.sort_values(by="likes", ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.barh(top_likes["title"], top_likes["likes"], color="salmon")
plt.title("Top 10 recetas veganas más populares")
plt.xlabel("Número de likes")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("assets/image/ranking_popularidad.png")#GRAFICA GUARDADA EN ASSETS/IMAGE
plt.close()


#TIEMPO DE PREPARACIÓN--------------------------------------------------------------------

top_rapidas = df.sort_values(by="readyInMinutes").reset_index(drop=True)

print("⏳ Recetas veganas más rápidas:")
for i, row in top_rapidas.head(10).iterrows():
    print(f"{i+1}. {row['title']} – {row['readyInMinutes']} min")

#GRAFICO

top_rapidas = df.sort_values(by="readyInMinutes").head(10)
plt.figure(figsize=(10, 6))
plt.barh(top_rapidas["title"], top_rapidas["readyInMinutes"], color="mediumseagreen")
plt.title("Top 10 recetas veganas más rápidas")
plt.xlabel("Minutos de preparación")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("assets/image/ranking_rapidez.png")#GRAFICA GUARDADA EN ASSETS/IMAGE
plt.close()


#Recetas con mejor puntaje saludable y rápida---------------------------------------------------------------

df["eficiencia_salud"] = df["healthScore"] / df["readyInMinutes"]
eficientes = df.sort_values(by="eficiencia_salud", ascending=False).head(10)

print("Recetas más eficientes en salud por minuto:")
for i, r in eficientes.iterrows():
    print(f"{r['title']} – {round(r['eficiencia_salud'], 2)} pts/min")

#GRAFICO
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="readyInMinutes", y="likes", hue="healthScore", palette="viridis")
plt.title("Popularidad vs Tiempo de Preparación")
plt.xlabel("Minutos")
plt.ylabel("Likes")
plt.tight_layout()
plt.savefig("assets/image/popularidad_vs_tiempo.png")#GRAFICA GUARDADA EN ASSETS/IMAGE
plt.close()

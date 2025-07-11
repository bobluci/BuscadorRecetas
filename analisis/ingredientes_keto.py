import requests
import json
import time
from collections import Counter

API_KEY = "fccd95431d254ee0b8c8b49c2a8ac365" 
headers = {"Content-Type": "application/json"}

# Paso 1: Obtener recetas cetogénicas
search_url = "https://api.spoonacular.com/recipes/complexSearch"
search_params = {
    "apiKey": API_KEY,
    "diet": "ketogenic",
    "number": 20  # para evitar usar muchos créditos
}
response = requests.get(search_url, params=search_params, headers=headers)
results = response.json().get("results", [])

# Paso 2: Por cada receta, obtener información detallada
ingredientes_por_receta = []

for receta in results:
    receta_id = receta.get("id")
    titulo = receta.get("title", "Sin nombre")
    
    if receta_id:
        info_url = f"https://api.spoonacular.com/recipes/{receta_id}/information"
        info_params = {
            "apiKey": API_KEY
        }
        r = requests.get(info_url, params=info_params, headers=headers)
        info = r.json()
        
        ingredientes = info.get("extendedIngredients", [])
        lista_ingredientes = [ing.get("original", "") for ing in ingredientes]

        ingredientes_por_receta.append({
            "titulo": titulo,
            "ingredientes": lista_ingredientes
        })
        
        print(f"✅ {titulo} – {len(lista_ingredientes)} ingredientes")
        time.sleep(1)  # Espera para no saturar la API

# Paso 3: Guardar en JSON
with open("assets/data/ingredientes_ketogenicos.json", "w", encoding="utf-8") as f:
    json.dump(ingredientes_por_receta, f, indent=2, ensure_ascii=False)

print("📁 Archivo creado correctamente con ingredientes cetogénicos.")

# Paso 4: Análisis – Ingredientes más comunes
todos_los_ingredientes = []
for receta in ingredientes_por_receta:
    todos_los_ingredientes.extend(receta["ingredientes"])

conteo = Counter(todos_los_ingredientes)
ingredientes_comunes = conteo.most_common(10)

print("\n🥇 Ingredientes más comunes en recetas cetogénicas:")
for ingrediente, cantidad in ingredientes_comunes:
    print(f"• {ingrediente} – {cantidad} veces")

import matplotlib.pyplot as plt

# Gráfico de los 10 ingredientes más comunes
ingredientes, cantidades = zip(*ingredientes_comunes)

plt.figure(figsize=(10, 6))
plt.barh(ingredientes, cantidades, color="skyblue")
plt.title("Top 10 ingredientes más comunes en recetas cetogénicas")
plt.xlabel("Cantidad de apariciones")
plt.gca().invert_yaxis()
plt.tight_layout()

# Guardar el gráfico
plt.savefig("assets/image/ingredientes_comunes_keto.png")
plt.close()

print("📊 Gráfico guardado en assets/image/ingredientes_comunes_keto.png")

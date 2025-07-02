"""
📊 Análisis de recetas con datos simulados
👤 Contribución: Fabiana Rojas

Este archivo analiza un conjunto de recetas simuladas
con el mismo formato que la API de Spoonacular.

🔍 Usa pandas para contar ingredientes más frecuentes
📈 Genera un gráfico con matplotlib que analiza los diez ingredientes mas utilizados.
🧂 Detecta la receta mas simple (menos ingredientes)
🎯 Este análisis será útil más adelante cuando se conecte la API y se obtengan datos reales.
"""

import json
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# 📥 Cargar datos del archivo
with open('recetas.json', 'r', encoding='utf-8') as archivo:
    recetas = json.load(archivo)

# 🧂 Extraer todos los ingredientes (usados + faltantes)
ingredientes = []
for receta in recetas:
    for ing in receta['usedIngredients'] + receta['missedIngredients']:
        ingredientes.append(ing['name'])

# 📊 Contar frecuencia
conteo = Counter(ingredientes)
total = sum(conteo.values())

# 🥇 Ingrediente más común con porcentaje
ingrediente_mas_comun, cantidad = conteo.most_common(1)[0]
porcentaje = (cantidad / total) * 100
print(f"🥇 Ingrediente más común: {ingrediente_mas_comun} ({cantidad} veces, {porcentaje:.2f}%)")

# 🧮 Calcular total de ingredientes por receta
for receta in recetas:
    total_ingredientes = len(receta['usedIngredients']) + len(receta['missedIngredients'])
    receta['total_ingredientes'] = total_ingredientes

# 🍽️ Receta con menos ingredientes
receta_min = min(recetas, key=lambda r: r['total_ingredientes'])
print(f"🍽️ Receta más sencilla: {receta_min['title']} ({receta_min['total_ingredientes']} ingredientes)")

# 📈 Gráfico de ingredientes más frecuentes
ingredientes_comunes = conteo.most_common(10)
nombres = [i[0] for i in ingredientes_comunes]
cantidades = [i[1] for i in ingredientes_comunes]
porcentajes = [(i / total) * 100 for i in cantidades]

plt.figure(figsize=(8, 5))
barras = plt.barh(nombres[::-1], cantidades[::-1], color='skyblue')
plt.xlabel("Cantidad de apariciones")
plt.title("Top 10 ingredientes más frecuentes")

# 🏷️ Agregar porcentajes al lado de cada barra
for barra, porcentaje in zip(barras, porcentajes[::-1]):
    ancho = barra.get_width()
    plt.text(
        ancho + 0.1,
        barra.get_y() + barra.get_height() / 2,
        f"{porcentaje:.1f}%",
        va='center'
    )

plt.tight_layout()
plt.savefig("ingredientes_frecuentes.png")
plt.show()

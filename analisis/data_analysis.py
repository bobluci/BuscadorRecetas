"""
📊 Análisis de recetas con datos reales
👤 Contribución: Fabiana Rojas

Este archivo analiza un conjunto de recetas obtenidas desde la API de Spoonacular
y guardadas previamente en formato JSON.

🔍 Usa pandas para contar ingredientes más frecuentes
📈 Genera un gráfico con matplotlib que analiza los diez ingredientes más utilizados.
🧂 Detecta la receta más simple (menos ingredientes)
📄 Exporta un resumen en formato .txt con tabla
🎯 Este análisis permite conocer patrones útiles a partir de los datos reales.
"""

import json
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import os

# 📥 Ruta del archivo JSON de entrada
ruta_json = os.path.join("..", "assets", "data", "recetas_por_ingredientes.json")

# ✅ Cargar datos desde archivo JSON
with open(ruta_json, 'r', encoding='utf-8') as archivo:
    recetas = json.load(archivo)

print(f"✅ Se cargaron {len(recetas)} recetas reales desde '{ruta_json}'.")

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

# 📁 Crear carpeta de resultados
carpeta_resultados = os.path.join(os.path.dirname(__file__), "resultados")
os.makedirs(carpeta_resultados, exist_ok=True)

# 🖼️ Guardar imagen
ruta_imagen = os.path.join(carpeta_resultados, "ingredientes_frecuentes.png")
plt.tight_layout()
plt.savefig(ruta_imagen)
# plt.show()  # Opcional

# 📝 Crear archivo TXT con tabla
ruta_txt = os.path.join(carpeta_resultados, "resumen_ingredientes.txt")
with open(ruta_txt, 'w', encoding='utf-8') as f:
    f.write("📊 Análisis de Recetas (datos reales de Spoonacular)\n\n")
    f.write(f"🥇 Ingrediente más común: {ingrediente_mas_comun} ({cantidad} veces, {porcentaje:.2f}%)\n")
    f.write(f"🍽️ Receta más sencilla: {receta_min['title']} ({receta_min['total_ingredientes']} ingredientes)\n\n")
    f.write("🔝 Top 10 ingredientes más frecuentes:\n\n")
    
    f.write("| Nº | Ingrediente        | Frecuencia | Porcentaje |\n")
    f.write("|----|---------------------|------------|------------|\n")
    
    for i, (nombre, cant) in enumerate(ingredientes_comunes, start=1):
        porc = (cant / total) * 100
        f.write(f"| {i:<2} | {nombre:<19} | {cant:<10} | {porc:>9.2f}% |\n")

print(f"\n✅ Imagen guardada en: {ruta_imagen}")
print(f"📄 Análisis en tabla guardado en: {ruta_txt}")

# Importación de librerías necesarias
import os
import json
import pandas as pd
import plotly.express as px
from collections import Counter

# === 1. Cargar datos desde archivos JSON ===
ruta_veganas = os.path.join("assets", "data", "recetas_veganas.json")
ruta_keto = os.path.join("assets", "data", "ingredientes_ketogenicos.json")

# Abrir archivo de recetas veganas
with open(ruta_veganas, encoding="utf-8") as f:
    data_veganas = json.load(f)

# Abrir archivo de ingredientes combinados
with open(ruta_keto, encoding="utf-8") as f:
    data_keto = json.load(f)

# === 2. Crear DataFrames para análisis ===

# Convertir recetas veganas a DataFrame con variables clave
df_vegan = pd.DataFrame([{
    "title": r.get("title"),
    "readyInMinutes": r.get("readyInMinutes"),
    "healthScore": r.get("healthScore", 0),  # Puntaje de salud
    "pricePerServing": r.get("pricePerServing"),
    "likes": r.get("aggregateLikes"),        # Popularidad
    "dishTypes": r.get("dishTypes"),
    "diets": r.get("diets")
} for r in data_veganas])

# Extraer ingredientes cetogénicos (usados y faltantes)
ingredientes_keto = []
for receta in data_keto:
    ingredientes_keto.extend(receta['ingredientes'])

# Contar frecuencia de ingredientes cetogénicos
conteo_keto = Counter(ingredientes_keto)
ingredientes_comunes_keto = conteo_keto.most_common(10)  # Top 10 más comunes

# Crear DataFrame de ingredientes cetogénicos para gráfico
df_ingredientes_keto = pd.DataFrame(ingredientes_comunes_keto, columns=["Ingrediente", "Frecuencia"])
df_ingredientes_keto["Porcentaje"] = (df_ingredientes_keto["Frecuencia"] / sum(conteo_keto.values())) * 100

# === 3. Crear gráficos interactivos con Plotly ===

# 🔹 Gráfico 1: Ingredientes más frecuentes (horizontal)
fig1 = px.bar(
    df_ingredientes_keto[::-1],  # Revertir para mostrar de mayor a menor
    x="Frecuencia", 
    y="Ingrediente", 
    orientation="h", 
    text=df_ingredientes_keto[::-1]["Porcentaje"].map("{:.1f}%".format),
    title="Top 10 ingredientes cetogénicos más frecuentes",
    color="Frecuencia",
    color_continuous_scale="Blues"
)
fig1.update_layout(yaxis_title="", xaxis_title="Frecuencia", coloraxis_showscale=False)

# 🔹 Gráfico 2: Recetas con más likes
fig2 = px.bar(
    df_vegan.sort_values(by="likes", ascending=False).head(10)[::-1],
    x="likes",
    y="title",
    orientation="h",
    title="Top 10 recetas veganas más populares",
    color="likes",
    color_continuous_scale="reds"
)
fig2.update_layout(yaxis_title="", xaxis_title="Likes", coloraxis_showscale=False)

# 🔹 Gráfico 3: Recetas más rápidas (tiempo de preparación)
fig3 = px.bar(
    df_vegan.sort_values(by="readyInMinutes").head(10)[::-1],
    x="readyInMinutes",
    y="title",
    orientation="h",
    title="Top 10 recetas veganas más rápidas",
    color="readyInMinutes",
    color_continuous_scale="greens"
)
fig3.update_layout(yaxis_title="", xaxis_title="Minutos", coloraxis_showscale=False)

# 🔹 Gráfico 4: Dispersión de likes vs tiempo, codificado por salud
fig4 = px.scatter(
    df_vegan,
    x="readyInMinutes",
    y="likes",
    color="healthScore",
    size="healthScore",
    hover_name="title",
    title="Popularidad vs Tiempo de Preparación (codificada por puntaje saludable)",
    color_continuous_scale="viridis"
)
fig4.update_layout(xaxis_title="Minutos", yaxis_title="Likes")

# === 4. Exportar cada gráfico como bloque HTML embebible ===

graficos_html = []
for i, fig in enumerate([fig1, fig2, fig3, fig4], start=1):
    # Convertir cada gráfico en un bloque HTML (sin encabezado <html>)
    html = fig.to_html(full_html=False, include_plotlyjs='cdn', div_id=f"grafico{i}")
    graficos_html.append(html)

# === 5. Crear HTML final que contenga los 4 gráficos ===

html_final = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard de Recetas Veganas</title>
    <link rel="stylesheet" href="../../styles/main.css">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0; padding: 2rem;
            background: #f8f8f8;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 0.2em;
        }}
        p {{
            text-align: center;
            margin-bottom: 2em;
            color: #555;
        }}
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;  /* Dos columnas */
            gap: 2rem;
        }}
        .grafico {{
            background: #fff;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 0 12px rgba(0,0,0,0.05);
        }}
        @media (max-width: 1000px) {{
            .grid {{
                grid-template-columns: 1fr;  /* Una columna en móviles */
            }}
        }}
    </style>
</head>
<body>
    <h1>📊 Dashboard Interactivo de Recetas Veganas</h1>
    <p>Explora los ingredientes más usados, recetas populares, tiempos de preparación y eficiencia saludable.</p>
    <div class="grid">
        {''.join(f'<div class="grafico">{g}</div>' for g in graficos_html)}
    </div>
</body>
</html>
"""

# === 6. Guardar el archivo HTML final en carpeta correspondiente ===

ruta_salida = os.path.join("assets", "html")
os.makedirs(ruta_salida, exist_ok=True)  # Crear carpeta si no existe

# Guardar dashboard completo como HTML
with open(os.path.join(ruta_salida, "dashboard.html"), "w", encoding="utf-8") as f:
    f.write(html_final)

print("✅ Dashboard generado exitosamente en 'assets/html/dashboard.html'")
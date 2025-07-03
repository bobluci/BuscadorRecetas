import requests
import json

# API Key de Spoonacular
API_KEY = 'TU_API_KEY'  # Reemplaza con tu propia API Key

# Ingredientes a buscar (en inglés)
ingredientes = 'lettuce,tomato,cheese'

# URL base para hacer las consultas a la API
base_url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredientes}&number=10&apiKey={API_KEY}'

# Lista para guardar todas las recetas obtenidas
todas_las_recetas = []

# Función para obtener recetas usando paginación
def obtener_recetas(pagina=1):
    url = base_url + f"&offset={pagina * 10}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return []

# Obtener recetas de varias páginas
pagina = 0
while True:
    recetas = obtener_recetas(pagina)
    if not recetas:  # Si no hay más recetas, salimos del bucle
        break
    todas_las_recetas.extend(recetas)  # Guardamos las recetas obtenidas
    pagina += 1

# Guardar las recetas en un archivo JSON
with open('recetas_por_ingredientes.json', 'w') as f:
    json.dump(todas_las_recetas, f, indent=4)

print(f"Total de recetas obtenidas: {len(todas_las_recetas)}")
print("Recetas guardadas en 'recetas_por_ingredientes.json'")

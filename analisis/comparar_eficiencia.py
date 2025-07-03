import time
import json
import requests

# Cargar datos desde el archivo JSON
start_time = time.time()
with open('recetas_por_ingredientes.json', 'r') as file:
    recetas_json = json.load(file)
json_time = time.time() - start_time

# Obtener datos directamente de la API
API_KEY = 'TU_API_KEY'  # Reemplaza con tu propia API Key
ingredientes = 'lettuce,tomato,cheese'
url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredientes}&number=10&apiKey={API_KEY}'

start_time = time.time()
response = requests.get(url)
api_time = time.time() - start_time

print(f"Tiempo usando archivo JSON: {json_time:.4f} segundos")
print(f"Tiempo usando la API: {api_time:.4f} segundos")

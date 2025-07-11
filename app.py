from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Ruta principal para servir el HTML
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

# Ruta para servir el JavaScript
@app.route('/script.js')
def script():
    return send_from_directory('', 'script.js')

# Ruta para servir los estilos
@app.route('/styles/<path:nombre>')
def estilos(nombre):
    return send_from_directory('styles', nombre)

# Ruta de búsqueda de recetas
@app.route('/buscar', methods=["GET"])
def buscar():
    ingredientes = request.args.get('ingredientes')
    api_key = os.getenv("SPOONACULAR_API_KEY")

    if not ingredientes:
        return jsonify({"error": "No se proporcionaron ingredientes"}), 400

    if not api_key:
        return jsonify({"error": "No se encontró la API key en .env"}), 500

    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredientes,
        "apiKey": api_key,
        "number": 5
    }

    response = requests.get(url, params=params)
    
    try:
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": f"Respuesta inválida de la API: {str(e)}"}), 500

# Ejecuta el servidor
if __name__ == '__main__':
    app.run(debug=True)

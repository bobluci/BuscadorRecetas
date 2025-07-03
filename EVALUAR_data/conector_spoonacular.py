import requests
import json

# Diccionario de traducciones comunes de ingredientes (español a inglés y viceversa para facilitar)
# Originalmente english_word: spanish_word
TRADUCCIONES_INGREDIENTES = {
    "chicken": "pollo", "rice": "arroz", "tomato": "tomate", "tomatoes": "tomates",
    "onion": "cebolla", "onions": "cebollas", "garlic": "ajo", "carrot": "zanahoria",
    "bell pepper": "pimiento", "okra": "okra", "canned tomatoes": "tomates enlatados",
    "can chicken broth": "caldo de pollo enlatado", "cajun seasoning": "condimento cajún",
    "hot sauce": "salsa picante", "fry onion till golden brown": "freír cebolla hasta dorar",
    "onion nos": "cebolla", "serve": "servir", "chillies nos": "chiles",
    "coriander bunch": "manojo de cilantro", "garlic pod": "cabeza de ajo",
    "ginger long 2 inch": "jengibre de 2 pulgadas",
    "then add water i and cook on flame till meat is tender": "luego añadir agua y cocinar a fuego hasta que la carne esté tierna",
    "delicious palak gosht is ready": "delicioso palak gosht está listo",
    "tikka tandoori paste": "pasta tikka tandoori", "coriander leaves": "hojas de cilantro",
    "greek yogurt": "yogur griego", "black beans": "frijoles negros",
    "chili powder": "chile en polvo", "cumin": "comino",
    "optional: of hot sauce": "opcional: salsa picante", "bell peppers": "pimientos",
    "ground turkey": "pavo molido", "basil": "albahaca", "cayenne pepper": "pimienta cayena",
    "tomato sauce": "salsa de tomate", "ground beef": "carne molida", "kale": "col rizada",
    "allspice": "pimienta de Jamaica", "cinnamon": "canela", "dried/fresh mint": "menta seca/fresca",
    "tomato paste": "pasta de tomate", "lemon juice": "jugo de limón", "dill": "eneldo",
    "chavrie goat cheese log": "queso de cabra", "grape leaves": "hojas de parra",
    "frying chicken": "pollo para freír", "pepper flakes": "escamas de pimiento",
    "red wine vinegar": "vinagre de vino tinto", "basmati rice": "arroz basmati",
    "a onion": "una cebolla", "celery finelly": "apio finamente", "rosemary": "romero",
    "parsley": "perejil", "chives": "cebollino", "milk": "leche", "egg": "huevo",
    "sugar": "azúcar", "salt": "sal", "pepper": "pimienta", "olive oil": "aceite de oliva",
    "thumb sized ginger": "jengibre (tamaño de un pulgar)",
    "chicken cube": "cubo de caldo de pollo",
    "fish sauce": "salsa de pescado",
    "green onion": "cebolla verde",
    "hardboiled quail eggs": "huevos de codorniz duros",
    "pcs lemon": "rodajas de limón",
    "potato": "papa", "potatoes": "papas", "bread": "pan", "cheese": "queso", # Añadidos comunes
    "lettuce": "lechuga", "mayonnaise": "mayonesa", "tuna": "atun"
}

# Crear un diccionario inverso para traducir de español a inglés
TRADUCCIONES_INVERSAS = {v: k for k, v in TRADUCCIONES_INGREDIENTES.items()}


def traducir_ingrediente_salida(nombre_ingrediente_original):
    """
    Traduce un nombre de ingrediente de la API (generalmente en inglés) a español.
    """
    if not nombre_ingrediente_original:
        return ""
    nombre_normalizado = nombre_ingrediente_original.lower().strip()
    return TRADUCCIONES_INGREDIENTES.get(nombre_normalizado, nombre_ingrediente_original)

def traducir_ingrediente_entrada(nombre_ingrediente_espanol):
    """
    Traduce un nombre de ingrediente de entrada de español a inglés para la API.
    """
    if not nombre_ingrediente_espanol:
        return ""
    nombre_normalizado = nombre_ingrediente_espanol.lower().strip()
    return TRADUCCIONES_INVERSAS.get(nombre_normalizado, nombre_ingrediente_espanol) # Si no se encuentra, devuelve el original (en español)

def es_ingrediente_valido(nombre):
    """
    Intenta determinar si una frase es un ingrediente o una instrucción.
    Devuelve True si parece un ingrediente, False si parece una instrucción.
    """
    if not nombre or len(nombre) < 2:
        return False
    
    nombre_lower = nombre.lower()
    
    palabras_clave_instruccion = [
        "in a ", "stir in", "add ", "cook", "heat", "serve", "sprinkle", "garnish",
        "chop", "slice", "dice", "mix", "prepare", "place", "combine", "until",
        "season with", "to taste", "optional", "amount of", "till", "put", "then add",
        "delicious", "ready", "long", "inch", "pod", "bunch", "nos" # Añadidos para filtrar más frases
    ]
    
    for kw in palabras_clave_instruccion:
        if kw in nombre_lower:
            return False
            
    if len(nombre.split()) > 5:
        return False

    return True

def obtener_y_guardar_recetas_por_ingredientes_con_enlace(api_key_spoonacular, ingredientes_busqueda_espanol, nombre_archivo="recetas_por_ingredientes.json", numero=10):
    """
    Obtiene recetas de la API de Spoonacular usando findByIngredients.
    Los ingredientes de entrada se traducen de español a inglés.
    Las recetas resultantes y sus ingredientes se traducen (salida), se filtran y se guardan en un archivo JSON.

    Args:
        api_key_spoonacular (str): Tu clave API de Spoonacular.
        ingredientes_busqueda_espanol (list): Una lista de los ingredientes a buscar, en español.
        nombre_archivo (str): El nombre del archivo JSON de salida.
        numero (int): El número de recetas a recuperar.
    """
    base_url = "https://api.spoonacular.com/recipes/findByIngredients"
    
    # --- Traducir los ingredientes de entrada de español a inglés ---
    ingredientes_ingles = [traducir_ingrediente_entrada(ing) for ing in ingredientes_busqueda_espanol]
    ingredientes_str = ",".join(ingredientes_ingles) # Unir para la URL de la API
    print(f"Ingredientes en español recibidos: {ingredientes_busqueda_espanol}")
    print(f"Ingredientes traducidos a inglés para la API: {ingredientes_ingles}")
    # ---------------------------------------------------------------

    params = {
        "apiKey": api_key_spoonacular,
        "ingredients": ingredientes_str,
        "number": numero,
        "ranking": 1, 
        "ignorePantry": True,
        "language": "es" # Pedir a Spoonacular que intente traducir los títulos
    }

    try:
        print(f"Buscando recetas en Spoonacular por ingredientes (API en inglés): '{ingredientes_str}'...")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        print("\n--- RESPUESTA DE LA API DE SPOONACULAR PARA DEPURACIÓN ---")
        api_response_data = response.json()
        print(json.dumps(api_response_data, indent=2))
        print("----------------------------------------------------------\n")

        recetas_encontradas = api_response_data 
        
        if not recetas_encontradas:
            print(f"La API de Spoonacular no devolvió ninguna receta para la búsqueda de ingredientes: '{ingredientes_str}'. El JSON estará vacío.")
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            return

        print(f"Se encontraron {len(recetas_encontradas)} recetas. Procesando, traduciendo y filtrando ingredientes...")
        
        recetas_formateadas = []
        for receta in recetas_encontradas:
            titulo_receta = receta.get("title", "")
            imagen_url = receta.get("image", "")
            receta_id = receta.get("id")

            spoonacular_url = ""
            if titulo_receta and receta_id:
                titulo_para_url = titulo_receta.replace(" ", "-").replace("/", "-").replace("'", "").lower()
                spoonacular_url = f"https://spoonacular.com/recipes/{titulo_para_url}-{receta_id}"
            
            ingredientes_usados_traducidos = []
            for item in receta.get("usedIngredients", []):
                nombre_original = item.get("name", "")
                nombre_traducido = traducir_ingrediente_salida(nombre_original) # Usar la traducción para la salida
                if es_ingrediente_valido(nombre_original):
                    ingredientes_usados_traducidos.append({"name": nombre_traducido})

            ingredientes_faltantes_traducidos = []
            for item in receta.get("missedIngredients", []):
                nombre_original = item.get("name", "")
                nombre_traducido = traducir_ingrediente_salida(nombre_original) # Usar la traducción para la salida
                if es_ingrediente_valido(nombre_original):
                    ingredientes_faltantes_traducidos.append({"name": nombre_traducido})
            
            recetas_formateadas.append({
                "id": receta_id,
                "title": titulo_receta,
                "image": imagen_url,
                "spoonacularUrl": spoonacular_url,
                "usedIngredients": ingredientes_usados_traducidos,
                "missedIngredients": ingredientes_faltantes_traducidos
            })
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(recetas_formateadas, f, ensure_ascii=False, indent=2)
        
        print(f"Recetas procesadas y guardadas exitosamente en '{nombre_archivo}'.")

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP de Spoonacular: {http_err} - Revisa tu clave API o los parámetros de la solicitud.")
    except requests.exceptions.RequestException as req_err:
        print(f"Error de conexión o solicitud: {req_err}")
    except IOError as io_err:
        print(f"Error al escribir en el archivo '{nombre_archivo}': {io_err}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    API_KEY_SPOONACULAR = "api_key_spoonacular"  # Reemplaza con tu clave API real de Spoonacular
    
    # --- Ahora defines los ingredientes de búsqueda en español ---
    INGREDIENTES_PARA_BUSCAR_ESPANOL = ["pollo", "arroz", "tomate"] 
    
    NOMBRE_ARCHIVO_SALIDA = "./assets/data/recetas_por_ingredientes.json"
    NUMERO_RECETAS_A_OBTENER = 10 

    obtener_y_guardar_recetas_por_ingredientes_con_enlace(
        api_key_spoonacular=API_KEY_SPOONACULAR,
        ingredientes_busqueda_espanol=INGREDIENTES_PARA_BUSCAR_ESPANOL, # Pasa la lista en español
        nombre_archivo=NOMBRE_ARCHIVO_SALIDA,
        numero=NUMERO_RECETAS_A_OBTENER
    )
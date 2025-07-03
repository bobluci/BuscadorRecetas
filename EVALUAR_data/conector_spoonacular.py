import requests
import json

# Diccionario de traducciones comunes de ingredientes (puedes expandirlo según necesites)
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
    "chavrie goat cheese log": "queso de cabra chavrie", "grape leaves": "hojas de parra",
    "frying chicken": "pollo para freír", "pepper flakes": "escamas de pimiento",
    "red wine vinegar": "vinagre de vino tinto", "basmati rice": "arroz basmati",
    "a onion": "una cebolla", "celery finelly": "apio finamente", "rosemary": "romero",
    "parsley": "perejil", "chives": "cebollino", "milk": "leche", "egg": "huevo",
    "sugar": "azúcar", "salt": "sal", "pepper": "pimienta", "olive oil": "aceite de oliva"
}

def traducir_ingrediente(nombre_ingrediente_original):
    """
    Traduce un nombre de ingrediente usando un diccionario local.
    Convierte a minúsculas para una mejor coincidencia.
    """
    if not nombre_ingrediente_original:
        return ""
    nombre_normalizado = nombre_ingrediente_original.lower().strip()
    return TRADUCCIONES_INGREDIENTES.get(nombre_normalizado, nombre_ingrediente_original)

# Renombrada la función para reflejar que busca por ingredientes
def obtener_y_guardar_recetas_por_ingredientes_con_enlace(api_key_spoonacular, ingredientes_busqueda, nombre_archivo="recetas_por_ingredientes.json", numero=10):
    """
    Obtiene recetas de la API de Spoonacular usando findByIngredients,
    las traduce, añade el enlace directo a Spoonacular y las guarda en un archivo JSON.

    Args:
        api_key_spoonacular (str): Tu clave API de Spoonacular.
        ingredientes_busqueda (list): Una lista de los ingredientes a buscar (ej. ["chicken", "rice"]).
        nombre_archivo (str): El nombre del archivo JSON de salida.
        numero (int): El número de recetas a recuperar.
    """
    base_url = "https://api.spoonacular.com/recipes/findByIngredients" # Vuelve a findByIngredients
    
    # Prepara los ingredientes para la URL
    ingredientes_str = ",".join(ingredientes_busqueda)

    params = {
        "apiKey": api_key_spoonacular,
        "ingredients": ingredientes_str, # Usamos 'ingredients' aquí
        "number": numero,
        "ranking": 1, # Puedes ajustar esto: 1 = maximizar uso de ingredientes, 2 = minimizar ingredientes faltantes
        "ignorePantry": True,
        "language": "es" # Pedir a Spoonacular que intente traducir los títulos
    }

    try:
        print(f"Buscando recetas en Spoonacular por ingredientes: '{ingredientes_str}' (idioma de la API: español)...")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # --- LÍNEAS PARA DEPURACIÓN ---
        print("\n--- RESPUESTA DE LA API DE SPOONACULAR PARA DEPURACIÓN ---")
        api_response_data = response.json()
        print(json.dumps(api_response_data, indent=2))
        print("----------------------------------------------------------\n")
        # ----------------------------

        # findByIngredients devuelve directamente una lista de recetas, no bajo una clave 'results'
        recetas_encontradas = api_response_data 
        
        if not recetas_encontradas:
            print(f"La API de Spoonacular no devolvió ninguna receta para la búsqueda de ingredientes: '{ingredientes_str}'. El JSON estará vacío.")
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            return

        print(f"Se encontraron {len(recetas_encontradas)} recetas. Procesando y añadiendo enlaces...")
        
        recetas_formateadas = []
        for receta in recetas_encontradas:
            titulo_receta = receta.get("title", "")
            imagen_url = receta.get("image", "")
            receta_id = receta.get("id")

            # --- Generar el enlace directo a Spoonacular ---
            spoonacular_url = ""
            if titulo_receta and receta_id:
                # Limpiar el título para la URL (reemplazar espacios con guiones)
                titulo_para_url = titulo_receta.replace(" ", "-").replace("/", "-").replace("'", "").lower()
                spoonacular_url = f"https://spoonacular.com/recipes/{titulo_para_url}-{receta_id}"
            # ----------------------------------------------
            
            # Obtener y traducir ingredientes usados
            ingredientes_usados_traducidos = []
            for item in receta.get("usedIngredients", []): # Usamos .get para evitar errores si no existe la clave
                nombre_original = item.get("name", "")
                nombre_traducido = traducir_ingrediente(nombre_original)
                ingredientes_usados_traducidos.append({"name": nombre_traducido})

            # Obtener y traducir ingredientes faltantes
            ingredientes_faltantes_traducidos = []
            for item in receta.get("missedIngredients", []): # Usamos .get para evitar errores si no existe la clave
                nombre_original = item.get("name", "")
                nombre_traducido = traducir_ingrediente(nombre_original)
                ingredientes_faltantes_traducidos.append({"name": nombre_traducido})
            
            recetas_formateadas.append({
                "id": receta_id,
                "title": titulo_receta,
                "image": imagen_url,
                "spoonacularUrl": spoonacular_url, # Incluye el enlace
                "usedIngredients": ingredientes_usados_traducidos,
                "missedIngredients": ingredientes_faltantes_traducidos
                # findByIngredients no devuelve readyInMinutes, servings directamente.
                # Esos campos estaban disponibles con complexSearch + addRecipeInformation=True
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
    # --- CONFIGURACIÓN ---
    API_KEY_SPOONACULAR = "api_key" # ¡IMPORTANTE! Reemplaza con tu clave API real de Spoonacular
    
    # Volvemos a una lista de ingredientes específicos para la búsqueda
    INGREDIENTES_PARA_BUSCAR = ["chicken", "rice"] # Lista de ingredientes en inglés
    
    NOMBRE_ARCHIVO_SALIDA = "recetas_por_ingredientes.json" # Nuevo nombre de archivo
    NUMERO_RECETAS_A_OBTENER = 10 

    obtener_y_guardar_recetas_por_ingredientes_con_enlace(
        api_key_spoonacular=API_KEY_SPOONACULAR,
        ingredientes_busqueda=INGREDIENTES_PARA_BUSCAR, # Pasa la lista de ingredientes
        nombre_archivo=NOMBRE_ARCHIVO_SALIDA,
        numero=NUMERO_RECETAS_A_OBTENER
    )
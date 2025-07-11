const API_KEY = "TU_API_KEY"; // ← Reemplaza esto con tu clave real

// Diccionario de ingredientes español → inglés
const diccionario = {
  "pollo": "chicken",
  "papa": "potato",
  "tomate": "tomato",
  "cebolla": "onion",
  "ajo": "garlic",
  "arroz": "rice",
  "leche": "milk",
  "queso": "cheese",
  "carne": "beef",
  "huevo": "egg",
  "pan": "bread",
  "manzana": "apple",
  "plátano": "banana",
  "sal": "salt",
  "pimienta": "pepper",
  "aceite de oliva": "olive oil",
  "harina": "flour",
  "azúcar": "sugar",
  "mantequilla": "butter",
  "agua": "water",
  "zanahoria": "carrot",
  "pimiento": "bell pepper",
  "limón": "lemon",
  "cilantro": "cilantro", 
  "perejil": "parsley",
  "tallarines": "spaghetti", 
  "frijoles": "beans",
  "maíz": "corn",
  "cerdo": "pork",
  "pescado": "fish",
  "camarón": "shrimp",
  "chile": "chili", 
  "yogur": "yogurt",
  "miel": "honey",
  "vinagre": "vinegar",
  "mostaza": "mustard",
  "cereal": "cereal",
  "avena": "oats",
  "chocolate": "chocolate",
  "naranja": "orange",
  "fresa": "strawberry",
  "aguacate": "avocado",
  "pepino": "cucumber",
  "calabacín": "zucchini",
  "brócoli": "broccoli",
  "coliflor": "cauliflower",
  "espinaca": "spinach",
  "champiñón": "mushroom",
  "jengibre": "ginger",
  "canela": "cinnamon",
  "comino": "cumin",
  "orégano": "oregano",
  "paprika": "paprika",
  "laurel": "bay leaf",
  "romero": "rosemary",
  "tomillo": "thyme",
  "vinagre de manzana": "apple cider vinegar",
  "salsa de soja": "soy sauce",
  "miso": "miso",
  "tofu": "tofu",
  "lentejas": "lentils",
  "garbanzos": "chickpeas"
};

// Traduce una lista de ingredientes en español
function traducir(ingredientesEsp) {
  return ingredientesEsp.map(esp => diccionario[esp.trim().toLowerCase()] || esp.trim().toLowerCase());
}

// Función principal para buscar recetas
function buscarRecetas() {
  const input = document.getElementById("ingredientes").value;
  const tipo = document.getElementById("tipo").value;
  const tiempo = document.getElementById("tiempo").value;
  const dieta = document.getElementById("dieta").value;

  const ingredientesArray = input.split(",");
  const ingredientes = traducir(ingredientesArray).join(",");

  let url = `https://api.spoonacular.com/recipes/complexSearch?includeIngredients=${ingredientes}&number=10&apiKey=${API_KEY}`;

  if (tipo) url += `&type=${tipo}`;
  if (tiempo) url += `&maxReadyTime=${tiempo}`;
  if (dieta) url += `&diet=${dieta}`;

  const contenedor = document.getElementById("resultados");
  contenedor.innerHTML = "<p>Buscando recetas...</p>";

  fetch(url)
    .then(res => res.json())
    .then(data => {
      contenedor.innerHTML = "";

      if (!data.results || data.results.length === 0) {
        contenedor.innerHTML = "<p>No se encontraron recetas con esos filtros.</p>";
        return;
      }

      data.results.forEach(receta => {
        const divReceta = document.createElement('div');
        divReceta.classList.add('receta');

        const titulo = document.createElement('h2');
        titulo.textContent = receta.title;
        divReceta.appendChild(titulo);

        const imagen = document.createElement('img');
        imagen.src = receta.image;
        imagen.alt = `Imagen de ${receta.title}`;
        divReceta.appendChild(imagen);

        const link = document.createElement('a');
        link.href = `https://spoonacular.com/recipes/${receta.title.replace(/\s+/g, '-')}-${receta.id}`;
        link.textContent = "Ver receta completa";
        link.target = "_blank";
        divReceta.appendChild(link);

        const hr = document.createElement('hr');
        divReceta.appendChild(hr);

        contenedor.appendChild(divReceta);
      });
    })
    .catch(err => {
      console.error("Error:", err);
      alert("Ocurrió un error al buscar las recetas. Verifica tu conexión o tu clave API.");
    });
}

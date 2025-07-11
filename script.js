// Traducción español → inglés
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

function traducir(ingredientesEsp) {
  return ingredientesEsp.map(esp => diccionario[esp.trim().toLowerCase()] || esp.trim().toLowerCase());
}

function buscarRecetas() {
  const input = document.getElementById("ingredientes").value;
  const ingredientesTraducidos = traducir(input.split(",")).join(",");

  const url = `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${ingredientesTraducidos}&number=5&apiKey=d0e372edd1ae494c937ae7c2d8adce32`;
  
  const contenedor = document.getElementById("resultados");
  contenedor.innerHTML = "<p>Buscando recetas...</p>";

  fetch(url)
    .then(r => r.json())
    .then(data => {
      contenedor.innerHTML = "";
      if (!data.length) {
        contenedor.innerHTML = "<p>No se encontraron recetas.</p>";
        return;
      }
      data.forEach(receta => {
        contenedor.innerHTML += `
          <h3>${receta.title}</h3>
          <img src="${receta.image}" width="280">
          <p><a target="_blank" href="https://spoonacular.com/recipes/${receta.title.replace(/\s+/g,'-')}-${receta.id}">Ver receta completa</a></p>
          <hr>`;
      });
    })
    .catch(err => {
      console.error(err);
      contenedor.innerHTML = "<p>Error al buscar recetas. Intenta más tarde.</p>";
    });
}

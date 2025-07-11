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

  const url = `http://127.0.0.1:5000/buscar?ingredientes=${ingredientesTraducidos}`;
  const contenedor = document.getElementById("resultados");

  contenedor.innerHTML = "<p>Buscando recetas...</p>";

  fetch(url)
    .then(res => res.json())
    .then(data => {
      contenedor.innerHTML = "";

      if (!data || data.length === 0) {
        contenedor.innerHTML = "<p>No se encontraron recetas.</p>";
        return;
      }

      data.forEach(receta => {
        const div = document.createElement("div");
        div.classList.add("receta");

        div.innerHTML = `
          <h2>${receta.title}</h2>
          <img src="${receta.image}" alt="${receta.title}" width="300" />
          <p><a href="https://spoonacular.com/recipes/${receta.title.replace(/\s+/g, "-")}-${receta.id}" target="_blank">Ver receta completa</a></p>
          <hr>
        `;

        contenedor.appendChild(div);
      });
    })
    .catch(err => {
      console.error(err);
      contenedor.innerHTML = "<p>Error al buscar recetas. Intenta más tarde.</p>";
    });
}

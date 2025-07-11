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
  "plátano": "banana"
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

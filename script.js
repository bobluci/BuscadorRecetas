const API_KEY = "TU_API_KEY"; // ← reemplázala localmente por tu clave real

// Esta es la función que se encarga de buscar ingredientes mediante la API
function buscarRecetas() {
  const input = document.getElementById("ingredientes").value;
  const ingredientes = input.split(",").map(i => i.trim()).join(",");

  // URL para hacer la solicitud a la API
  // ¡IMPORTANTE! Añadido el parámetro '&language=es' para solicitar resultados en español.
  const url = `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${ingredientes}&number=10&ranking=1&ignorePantry=true&apiKey=${API_KEY}&language=es`;

  // Hacemos la solicitud HTTP usando fetch para obtener los datos desde la API
  fetch(url)
    .then(res => res.json())
    .then(data => {
      const contenedor = document.getElementById("resultados");
      contenedor.innerHTML = "";

      if (data.length === 0) {
        contenedor.innerHTML = "<p>No se encontraron recetas con esos ingredientes.</p>";
        return;
      }

      // Mostrar los resultados de recetas en pantalla
      data.forEach(receta => {
        const divReceta = document.createElement('div');
        divReceta.classList.add('receta');

        // Título de la receta (debería venir en español si la API lo soporta)
        const tituloReceta = document.createElement('h2');
        tituloReceta.textContent = receta.title;
        divReceta.appendChild(tituloReceta);

        // Imagen de la receta
        const imagenReceta = document.createElement('img');
        imagenReceta.src = receta.image;
        imagenReceta.alt = `Imagen de ${receta.title}`;
        divReceta.appendChild(imagenReceta);

        // Ingredientes usados (la API no siempre los traduce al español)
        const pIngredientesUsados = document.createElement('p');
        const nombresUsados = receta.usedIngredients.map(ing => ing.name).join(', ');
        pIngredientesUsados.innerHTML = `<strong>Ingredientes que tienes (${receta.usedIngredientCount}):</strong> ${nombresUsados || 'Ninguno'}.`;
        divReceta.appendChild(pIngredientesUsados);

        // Ingredientes faltantes (la API no siempre los traduce al español)
        const pIngredientesFaltantes = document.createElement('p');
        const nombresFaltantes = receta.missedIngredients.map(ing => ing.name).join(', ');
        pIngredientesFaltantes.innerHTML = `<strong>Ingredientes que faltan (${receta.missedIngredientCount}):</strong> ${nombresFaltantes || 'Ninguno'}.`;
        divReceta.appendChild(pIngredientesFaltantes);

        // Enlace a la receta completa en Spoonacular
        const enlaceCompleto = document.createElement('a');
        enlaceCompleto.href = `https://spoonacular.com/recipes/${receta.title.replace(/\s+/g, '-')}-${receta.id}`;
        enlaceCompleto.textContent = "Ver receta completa";
        enlaceCompleto.target = "_blank";
        divReceta.appendChild(enlaceCompleto);
        
        const hr = document.createElement('hr');
        divReceta.appendChild(hr);

        contenedor.appendChild(divReceta);
      });
    })
    .catch(err => {
      console.error("Error:", err);
      alert("Ocurrió un error al buscar las recetas. Por favor, revisa tu conexión o tu clave API.");
    });
}
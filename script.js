const API_KEY = "TU_API_KEY"; // ← reemplázala localmente por tu clave real

// Esta es la función que se encarga de buscar ingredientes mediante la API
function buscarRecetas(query) {
  // Armamos la URL de la petición, incorporando el término de búsqueda (`query`) y la API key
  const url = `https://api.spoonacular.com/food/ingredients/search?query=${query}&number=10&apiKey=${API_KEY}`;

  // Hacemos la solicitud HTTP usando fetch para obtener los datos desde la API
  fetch(url)
    .then(res => res.json()) // Convertimos la respuesta en formato JSON
    .then(data => {
      // IMPORTANTE: Aquí se recibirá el arreglo de ingredientes devuelto por la API
      // IMPORTANTE: TODO: mostrar los ingredientes en pantalla, almacenarlos o procesarlos
    })
    .catch(err => console.error("Error:", err)); // Captura errores como red no disponible, clave incorrecta, etc.
}

const API_KEY = "TU_API_KEY"; // ← reemplázala localmente por tu clave real

// Esta es la función que se encarga de buscar ingredientes mediante la API
function buscarRecetas(query) {
  const input = document.getElementById("ingredientes").value; //Se obtiene el texto que el usuario escribió en el campo <input> con ID "ingredientes".
  const ingredientes = input.split(",").map(i => i.trim()).join(","); //limpieza de datos: separando con comas el texto en un array, elimina espacios extras y vuelve a unir el array limpio
//  URL para hacer la solicitud a la API
  const url = `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${ingredientes}&number=10&ranking=1&ignorePantry=true&apiKey=${API_KEY}`;

  // Hacemos la solicitud HTTP usando fetch para obtener los datos desde la API
  fetch(url)
    .then(res => res.json()) // Convertimos la respuesta en formato JSON
    .then(data => {
      const contenedor = document.getElementById("resultados"); // Obtiene el contenedor HTML donde se mostrarán los resultados de las recetas
      contenedor.innerHTML = ""; // Limpia el contenido previo del contenedor (por si ya se había hecho una búsqueda anterior)

      // Verifica si la API no devolvió ninguna receta
      if (data.length === 0) {
        contenedor.innerHTML = "<p>No se encontraron recetas con esos ingredientes.</p>"; // Muestra un mensaje indicando que no se encontraron recetas
        return; // Detiene la ejecución del resto de la función
      }

      // TODO: Mostrar los resultados de recetas en pantalla
      // Recorre el arreglo `data` (que contiene las recetas devueltas por la API)
      // Por cada receta:
      //  - Crear un <div> con clase "receta"
      //  - Mostrar el título, imagen, cantidad de ingredientes usados y faltantes
      //  - Agregar un enlace a la receta completa en Spoonacular
      // Finalmente, añadir cada <div> al contenedor con id="resultados"
    })
    .catch(err => {
      console.error("Error:", err); // Captura errores como red no disponible, clave incorrecta, etc.
      alert("Ocurrió un error al buscar las recetas.");//muestra un mensaje en consola y una alerta al usuario.
    })
}

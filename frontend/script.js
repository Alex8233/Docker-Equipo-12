async function cargarBienvenida() {
    const mensaje = document.getElementById("mensaje");
    const error = document.getElementById("error");

    try {
        const respuesta = await fetch("/api/bienvenida");

        if (!respuesta.ok) {
            throw new Error("Error al obtener la bienvenida");
        }

        const datos = await respuesta.json();

        mensaje.textContent = datos.mensaje;

    } catch (e) {
        mensaje.textContent = "";
        error.textContent = "No se pudo conectar con el backend.";
        console.error(e);
    }
}

cargarBienvenida();
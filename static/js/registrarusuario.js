document.getElementById("formRegistrar").addEventListener("submit", function(event) {
    event.preventDefault(); 
    const usuario = document.getElementById("usuario").value;
    const password = document.getElementById("password").value;
    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correo").value;
    const data = {
        usuario: usuario,
        password: password,
        nombre: nombre,
        correo: correo
    };
    fetch('/registrar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.text();
        }
    })
    .then(data => {
        console.log("Respuesta del servidor:", data);
    })
    .catch(error => {
        console.error("Error al registrar:", error);
    });
});

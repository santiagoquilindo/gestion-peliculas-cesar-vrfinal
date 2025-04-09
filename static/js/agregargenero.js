document.getElementById("formGenero").addEventListener("submit", function(event) {
    event.preventDefault(); 

    const nombreGenero = document.getElementById("nombre").value;

    const data = { nombre: nombreGenero };

    fetch('/agregargenero/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(data, "text/html");

const estado = doc.querySelector('#alert-container').getAttribute('data-estado');
const mensaje = doc.querySelector('#alert-container').getAttribute('data-mensaje');
if (estado === "True") {
    Swal.fire({
    icon: 'success',
    title: '¡Éxito!',
    text: mensaje,
    confirmButtonText: 'Aceptar'
}).then(() => {
    window.location.href = '/listargenero/';
}
);
} else 
{
Swal.fire({
    icon: 'error',
    title: '¡Error!',
    text: mensaje,
    confirmButtonText: 'Aceptar'
});
}
}).catch(error => {
    Swal.fire("Error en la solicitud",error);
    Swal.fire({
    icon: 'error',
    title: '¡Algo salió mal!',
    text: "Hubo un problema al procesar la solicitud.",
    confirmButtonText: 'Aceptar'
        });
    });
});

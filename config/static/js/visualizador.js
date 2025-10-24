const zonaId = JSON.parse(document.getElementById('zona-id').textContent);

function actualizarDisponibles() {
    fetch(`/estacionamientos/zona/${zonaId}/estado/`)
        .then(resp => resp.json())
        .then(data => {
            if (data.disponibles !== undefined) {
                document.getElementById('disp').textContent = data.disponibles;
            }
        })
        .catch(err => console.error('Error al actualizar:', err));
}

setInterval(actualizarDisponibles, 5000);

// Función para descargar el respaldo a la PC del usuario
function ejecutarBackup(dbName) {
    mostrarAlerta(`Generando respaldo de '${dbName}'... Por favor espera.`, 'info');

    // Apuntamos a la API de Flask
    window.location.href = `/api/backup/${dbName}`;
}

// Función para enviar el archivo de la PC al servidor para restaurar
function ejecutarRestore(dbName) {
    const fileInput = document.getElementById(`file-${dbName}`);
    const file = fileInput.files[0];

    if (!file) {
        mostrarAlerta(`Por favor, selecciona primero un archivo .sql para la base de datos ${dbName}.`, 'warning');
        return;
    }

    // Confirmación de seguridad (¡Paso crítico!)
    if (!confirm(`¿Estás seguro de que deseas restaurar la base de datos '${dbName}'? Esto sobrescribirá todos los datos actuales.`)) {
        return;
    }

    mostrarAlerta('Restaurando base de datos... No cierres esta ventana.', 'info');

    // Empaquetamos el archivo físico seleccionado desde la PC
    const formData = new FormData();
    formData.append('backup_file', file);

    fetch(`/api/restore/${dbName}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            mostrarAlerta(data.message, 'success');
            fileInput.value = ''; // Limpiamos el input
        } else {
            mostrarAlerta(`Error: ${data.message}`, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarAlerta('Ocurrió un error de red al intentar restaurar la base de datos.', 'danger');
    });
}

// Helper para pintar alertas Bootstrap dinámicas en pantalla
function mostrarAlerta(mensaje, tipo) {
    const container = document.getElementById('alert-container');
    container.innerHTML = `
        <div class="alert alert-${tipo} alert-dismissible fade show shadow-sm d-flex align-items-center" role="alert">
            <i class="bi ${tipo === 'success' ? 'bi-check-circle-fill' : tipo === 'danger' ? 'bi-dash-circle-fill' : 'bi-info-circle-fill'} me-2"></i>
            <div>${mensaje}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}
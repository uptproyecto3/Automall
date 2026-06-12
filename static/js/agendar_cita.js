document.addEventListener('DOMContentLoaded', function(){
    'use strict';

    // 1. Inicialización de selector de hora (Flatpickr Reloj)
    const fpHora = flatpickr("#hora_cita", {
        locale: "es",
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i:S",
        time_24hr: true,
        minuteIncrement: 30,
        minTime: "8:00",
        maxTime: "18:00"                               
    });

    // 2. Inicialización de selector de fecha (Flatpickr Calendario)
    const fpFecha = flatpickr("#fecha_cita", {
        locale: "es",
        dateFormat: "Y-m-d",
        minDate: "today",
        allowInput: false,
        altInput: true,
        altFormat: "d F, Y"
    });

    // 3. Previsualización dinámica del Vehículo Seleccionado
    const selectVehiculo = document.getElementById('select-vehiculo');
    const contenedorPreview = document.getElementById('contenedor-previsualizacion');

    if (selectVehiculo && contenedorPreview) {
        selectVehiculo.addEventListener('change', function() {
            const opcionSeleccionada = this.options[this.selectedIndex];
            
            if (opcionSeleccionada && opcionSeleccionada.value !== "") {
                const marca = opcionSeleccionada.getAttribute('data-marca');
                const modelo = opcionSeleccionada.getAttribute('data-modelo');
                const color = opcionSeleccionada.getAttribute('data-color');
                const anio = opcionSeleccionada.getAttribute('data-anio');
                const placa = opcionSeleccionada.getAttribute('data-placa');
                let imagen = opcionSeleccionada.getAttribute('data-imagen');

                // Si no tiene imagen asignada, usamos un placeholder premium SVG
                if (!imagen || imagen.trim() === "") {
                    imagen = `data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%' viewBox='0 0 400 220' style='background:%23e9ecef;'><rect width='400' height='220' fill='%23e9ecef'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='16' fill='%236c757d'>Vehículo sin fotografía</text></svg>`;
                }

                // Generar card HTML de previsualización coherente al estilo AutoMall
                contenedorPreview.innerHTML = `
                    <div class="card shadow border-0 rounded-3 overflow-hidden text-start mx-auto animate__animated animate__fadeIn" style="max-width: 350px;">
                        <img src="${imagen}" class="card-img-top" alt="${marca} ${modelo}" style="height: 180px; object-fit: cover;">
                        <div class="card-body">
                            <h5 class="card-title fw-bold text-dark mb-1">${marca} ${modelo}</h5>
                            <p class="text-muted small mb-2"><i class="bi bi-hash me-1"></i>Placa: <span class="badge bg-primary px-2">${placa}</span></p>
                            
                            <div class="row g-2 pt-2 border-top mt-2">
                                <div class="col-6 small text-secondary"><strong>Color:</strong> ${color}</div>
                                <div class="col-6 small text-secondary"><strong>Año:</strong> ${anio}</div>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                // Restaurar mensaje de ayuda inicial
                contenedorPreview.innerHTML = `
                    <div class="text-muted py-5 border border-dashed rounded-3 bg-light">
                        <i class="bi bi-image text-secondary-50" style="font-size: 3rem;"></i>
                        <h5 class="mt-3 fw-semibold">Ficha del Vehículo</h5>
                        <p class="small text-muted px-4">Seleccione un vehículo disponible de la lista para previsualizar su fotografía y especificaciones.</p>
                    </div>
                `;
            }
        });

        // Disparar el cambio si ya hay una opción seleccionada (por ejemplo al volver con errores flash)
        if (selectVehiculo.value !== "") {
            selectVehiculo.dispatchEvent(new Event('change'));
        }
    }

    // 4. Evitar doble envío de formulario
    const formulario = document.querySelector('form');
    const botonSubmit = document.getElementById('btn-agendar');

    if (formulario && botonSubmit) {
        formulario.addEventListener('submit', function(evento) {
            if (botonSubmit.disabled) {
                evento.preventDefault();
                return false;
            }
            
            // Si el formulario es válido, deshabilitamos el botón de envío
            if (formulario.checkValidity()) {
                botonSubmit.disabled = true;
                botonSubmit.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Procesando cita...';
            }
        });
    }

    // 5. Ocultar notificaciones flash automáticamente tras 5 segundos (Usando Bootstrap 5 nativo)
    setTimeout(function() {
        const alertas = document.querySelectorAll('.alert');
        alertas.forEach(function(alerta) {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alerta);
                if (bsAlert) bsAlert.close();
            } else {
                alerta.remove();
            }
        });
    }, 5000);

});
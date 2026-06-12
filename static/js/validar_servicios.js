$(document).ready(function () {
    function mostrarMensajeDebajo(inputElem, mensaje) {
        inputElem.next('.mensaje-error-simple').remove();
        var mensajeDiv = $('<div class="mensaje-error-simple text-danger small mt-1"></div>').text(mensaje);
        inputElem.after(mensajeDiv);
        inputElem.one('input change', function () {
            mensajeDiv.remove();
        });
    }

    function formatearFechaHoy() {
        const hoy = new Date();
        const year = hoy.getFullYear();
        const month = String(hoy.getMonth() + 1).padStart(2, '0');
        const day = String(hoy.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    const fechaHoy = formatearFechaHoy();

    $('#nombre_servicio').on('input blur', function () {
        const val = $(this).val().trim();
        const regex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

        if (val === '') {
            mostrarMensajeDebajo($(this), 'El nombre del servicio es obligatorio.');
        } else if (val.length < 3) {
            mostrarMensajeDebajo($(this), 'El nombre del servicio debe tener al menos 3 caracteres.');
        } else if (!regex.test(val)) {
            mostrarMensajeDebajo($(this), 'El nombre del servicio solo puede contener letras y espacios.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

  

    $('#placa').on('change blur', function () {
        if ($(this).val() === '') {
            mostrarMensajeDebajo($(this), 'Seleccione un vehículo.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

    $('#descripcion_especifica').on('input blur', function () {
        const val = $(this).val().trim();
        if (val === '') {
            mostrarMensajeDebajo($(this), 'La descripción específica es obligatoria.');
        } else if (val.length < 10) {
            mostrarMensajeDebajo($(this), 'La descripción específica debe tener al menos 10 caracteres.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

    $('form').on('submit', function (e) {
        if ($(this).attr('action') && $(this).attr('action').includes('generar_reporte_servicios')) {
            return;
        }

        $('.mensaje-error-simple').remove();
        let error = false;

        const nombre = $('#nombre_servicio').val().trim();
        const costo = $('#costo').val().trim();
        const placa = $('#placa').val();
        const descripcion = $('#descripcion_especifica').val().trim();
        const regexNombre = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;
      

        if (nombre === '') {
            mostrarMensajeDebajo($('#nombre_servicio'), 'El nombre del servicio es obligatorio.');
            $('#nombre_servicio').focus();
            error = true;
        } else if (nombre.length < 3) {
            mostrarMensajeDebajo($('#nombre_servicio'), 'El nombre del servicio debe tener al menos 3 caracteres.');
            $('#nombre_servicio').focus();
            error = true;
        } else if (!regexNombre.test(nombre)) {
            mostrarMensajeDebajo($('#nombre_servicio'), 'El nombre del servicio solo puede contener letras y espacios.');
            $('#nombre_servicio').focus();
            error = true;
        }

      

        if (placa === '') {
            mostrarMensajeDebajo($('#placa'), 'Seleccione un vehículo.');
            if (!error) $('#placa').focus();
            error = true;
        }

        if (descripcion === '') {
            mostrarMensajeDebajo($('#descripcion_especifica'), 'La descripción específica es obligatoria.');
            if (!error) $('#descripcion_especifica').focus();
            error = true;
        } else if (descripcion.length < 10) {
            mostrarMensajeDebajo($('#descripcion_especifica'), 'La descripción específica debe tener al menos 10 caracteres.');
            if (!error) $('#descripcion_especifica').focus();
            error = true;
        }

        if (error) {
            e.preventDefault();
        }
    });

    if ($('#tablaServicios').length && $.fn.DataTable) {
        if ($.fn.DataTable.isDataTable('#tablaServicios')) {
            $('#tablaServicios').DataTable().destroy();
        }

        $('#tablaServicios').DataTable({
            responsive: true,
            language: {
                search: "Buscar:",
                lengthMenu: "Mostrar _MENU_ registros",
                info: "Mostrando desde _START_ al _END_ de _TOTAL_ registros",
                paginate: {
                    first: "Primero",
                    last: "Último",
                    next: "Siguiente",
                    previous: "Anterior"
                },
                zeroRecords: "No se encontraron registros coincidentes",
                emptyTable: "No hay servicios registrados."
            }
        });
    }
});
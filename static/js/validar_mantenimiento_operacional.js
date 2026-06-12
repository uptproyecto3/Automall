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

    if ($('#fecha_salida').length) {
        $('#fecha_salida').attr('min', fechaHoy);
    }

    $('#descripcion_general').on('input blur', function () {
        const val = $(this).val().trim();
        if (val === '') {
            mostrarMensajeDebajo($(this), 'La descripción general es obligatoria.');
        } else if (val.length < 10) {
            mostrarMensajeDebajo($(this), 'La descripción general debe tener al menos 10 caracteres.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

    $('#quien_autoriza').on('input blur', function () {
        const val = $(this).val().trim();
        const regex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

        if (val === '') {
            mostrarMensajeDebajo($(this), 'El campo quién autoriza es obligatorio.');
        } else if (!regex.test(val)) {
            mostrarMensajeDebajo($(this), 'Solo se permiten letras y espacios.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

    $('#tipo').on('input blur', function () {
        const val = $(this).val().trim();
        if (val === '') {
            mostrarMensajeDebajo($(this), 'El tipo de mantenimiento es obligatorio.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

    $('#fecha_salida').on('change blur', function () {
        const val = $(this).val();
        if (val === '') {
            mostrarMensajeDebajo($(this), 'Seleccione la fecha de salida.');
        } else if (val < fechaHoy) {
            mostrarMensajeDebajo($(this), 'La fecha de salida no puede ser anterior al día de hoy.');
            $(this).val('');
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

    $('#cod_taller').on('change blur', function () {
        if ($(this).val() === '') {
            mostrarMensajeDebajo($(this), 'Seleccione un taller.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

    $('form').on('submit', function (e) {
        if ($(this).attr('action') && $(this).attr('action').includes('generar_reporte_mantenimiento')) {
            return;
        }

        $('.mensaje-error-simple').remove();
        let error = false;

        const descripcion = $('#descripcion_general').val().trim();
        const autoriza = $('#quien_autoriza').val().trim();
        const tipo = $('#tipo').val().trim();
        const fechaSalida = $('#fecha_salida').val();
        const fechaEntrega = $('#fecha_entrega').val();
        const placa = $('#placa').val();
        const taller = $('#cod_taller').val();

        const regexAutoriza = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

        if (descripcion === '') {
            mostrarMensajeDebajo($('#descripcion_general'), 'La descripción general es obligatoria.');
            $('#descripcion_general').focus();
            error = true;
        } else if (descripcion.length < 10) {
            mostrarMensajeDebajo($('#descripcion_general'), 'La descripción general debe tener al menos 10 caracteres.');
            $('#descripcion_general').focus();
            error = true;
        }

        if (autoriza === '') {
            mostrarMensajeDebajo($('#quien_autoriza'), 'El campo quién autoriza es obligatorio.');
            if (!error) $('#quien_autoriza').focus();
            error = true;
        } else if (!regexAutoriza.test(autoriza)) {
            mostrarMensajeDebajo($('#quien_autoriza'), 'Solo se permiten letras y espacios.');
            if (!error) $('#quien_autoriza').focus();
            error = true;
        }

        if (tipo === '') {
            mostrarMensajeDebajo($('#tipo'), 'El tipo de mantenimiento es obligatorio.');
            if (!error) $('#tipo').focus();
            error = true;
        }

        if (fechaSalida === '') {
            mostrarMensajeDebajo($('#fecha_salida'), 'Seleccione la fecha de salida.');
            if (!error) $('#fecha_salida').focus();
            error = true;
        } else if (fechaSalida < fechaHoy) {
            mostrarMensajeDebajo($('#fecha_salida'), 'La fecha de salida no puede ser anterior al día de hoy.');
            if (!error) $('#fecha_salida').focus();
            error = true;
        }

       

        if (fechaSalida && fechaEntrega && fechaEntrega < fechaSalida) {
            mostrarMensajeDebajo($('#fecha_entrega'), 'La fecha de entrega no puede ser menor que la fecha de salida.');
            if (!error) $('#fecha_entrega').focus();
            error = true;
        }

        if (placa === '') {
            mostrarMensajeDebajo($('#placa'), 'Seleccione un vehículo.');
            if (!error) $('#placa').focus();
            error = true;
        }

        if (taller === '') {
            mostrarMensajeDebajo($('#cod_taller'), 'Seleccione un taller.');
            if (!error) $('#cod_taller').focus();
            error = true;
        }

        if (error) {
            e.preventDefault();
        }
    });

    if ($('#tablaMantenimientoOperacional').length && $.fn.DataTable) {
        if ($.fn.DataTable.isDataTable('#tablaMantenimientoOperacional')) {
            $('#tablaMantenimientoOperacional').DataTable().destroy();
        }

        $('#tablaMantenimientoOperacional').DataTable({
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
                emptyTable: "No hay mantenimientos registrados."
            }
        });
    }
});
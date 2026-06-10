$(document).ready(function () {
    function mostrarMensajeDebajo(inputElem, mensaje) {
        inputElem.next('.mensaje-error-simple').remove();
        var mensajeDiv = $('<div class="mensaje-error-simple text-danger small mt-1"></div>').text(mensaje);
        inputElem.after(mensajeDiv);
        inputElem.one('input change', function () {
            mensajeDiv.remove();
        });
    }

    $('#nombre_taller').on('input blur', function () {
        const val = $(this).val().trim();
        const regex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

        if (val === '') {
            mostrarMensajeDebajo($(this), 'El nombre del taller es obligatorio.');
        } else if (!regex.test(val)) {
            mostrarMensajeDebajo($(this), 'El nombre solo puede contener letras y espacios.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

    $('#direccion').on('input blur', function () {
        const val = $(this).val().trim();
        if (val === '') {
            mostrarMensajeDebajo($(this), 'La dirección es obligatoria.');
        } else if (val.length < 5) {
            mostrarMensajeDebajo($(this), 'La dirección debe tener al menos 5 caracteres.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

    $('#estado').on('change blur', function () {
        if ($(this).val() === '') {
            mostrarMensajeDebajo($(this), 'Seleccione un estado.');
        } else {
            $(this).next('.mensaje-error-simple').remove();
        }
    });

    $('form').on('submit', function (e) {
        $('.mensaje-error-simple').remove();
        let error = false;

        const nombre = $('#nombre_taller').val().trim();
        const direccion = $('#direccion').val().trim();
        const estado = $('#estado').val();

        const regexNombre = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

        if (nombre === '') {
            mostrarMensajeDebajo($('#nombre_taller'), 'El nombre del taller es obligatorio.');
            $('#nombre_taller').focus();
            error = true;
        } else if (!regexNombre.test(nombre)) {
            mostrarMensajeDebajo($('#nombre_taller'), 'El nombre solo puede contener letras y espacios.');
            $('#nombre_taller').focus();
            error = true;
        }

        if (direccion === '') {
            mostrarMensajeDebajo($('#direccion'), 'La dirección es obligatoria.');
            if (!error) $('#direccion').focus();
            error = true;
        } else if (direccion.length < 5) {
            mostrarMensajeDebajo($('#direccion'), 'La dirección debe tener al menos 5 caracteres.');
            if (!error) $('#direccion').focus();
            error = true;
        }

        if (estado === '') {
            mostrarMensajeDebajo($('#estado'), 'Seleccione un estado.');
            if (!error) $('#estado').focus();
            error = true;
        }

        if (error) {
            e.preventDefault();
        }
    });

    if ($.fn.DataTable && $('#tablaTalleres').length) {
        if ($.fn.DataTable.isDataTable('#tablaTalleres')) {
            $('#tablaTalleres').DataTable().destroy();
        }

        $('#tablaTalleres').DataTable({
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
                zeroRecords: "No se encontraron registros coincidentes"
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // =========================================================
    // 1. Inicializar DataTables
    // =========================================================
    const tablaClientes = $('#tablaClientes');
    if (tablaClientes.length > 0) {
        tablaClientes.DataTable({
            dom: "<'row mb-3'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                 "<'row'<'col-sm-12'tr>>" +
                 "<'row mt-3'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            language: {
                lengthMenu: "Mostrar _MENU_ registros por p\u00e1gina",
                zeroRecords: "No se encontraron clientes coincidentes",
                info: "Mostrando p\u00e1gina _PAGE_ de _PAGES_",
                infoEmpty: "No hay registros disponibles",
                search: "Buscar Cliente:",
                paginate: { next: "Siguiente", previous: "Anterior" }
            },
            pageLength: 10,
            order: [[2, "asc"]]
        });
    }

    // =========================================================
    // 2. Precargar modal de edici\u00f3n con datos del cliente
    // =========================================================
    $(document).on('click', '.btn-editar-cliente', function () {
        var btn       = $(this);
        var cedula    = btn.attr('data-cedula');
        var textNombre = btn.attr('data-nombre');
        var apellido  = btn.attr('data-apellido');
        var telefono  = btn.attr('data-telefono');
        var direccion = btn.attr('data-direccion');
        var correo    = btn.attr('data-correo');
        var fotoUrl   = btn.attr('data-foto');

        $('#editar_cedula_display').val(cedula);
        $('#editar_nombre').val(textNombre);
        $('#editar_apellido').val(apellido);
        $('#editar_telefono').val(telefono);
        $('#editar_direccion').val(direccion);
        $('#editar_correo').val(correo);

        // Mostrar foto actual en el preview
        var previewImg = document.getElementById('preview-editar');
        if (fotoUrl && fotoUrl.trim() !== '') {
            previewImg.src = fotoUrl;
            previewImg.style.display = 'block';
        } else {
            previewImg.src = '#';
        }

        // Apuntar el form a la ruta de edici\u00f3n correcta
        $('#formEditarCliente').attr('action', '/clientes/editar/' + cedula);
    });

    // =========================================================
    // 3. Vista previa de nueva foto seleccionada en modal de edici\u00f3n
    // =========================================================
    var inputFotoEditar = document.getElementById('foto_perfil_editar');
    if (inputFotoEditar) {
        inputFotoEditar.addEventListener('change', function () {
            var previewImg = document.getElementById('preview-editar');
            if (this.files && this.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    previewImg.src = e.target.result;
                    previewImg.style.display = 'block';
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

    // =========================================================
    // 4. Modal de confirmaci\u00f3n de eliminaci\u00f3n
    // =========================================================
    $(document).on('click', '.btn-eliminar-cliente', function () {
        var cedula = $(this).attr('data-cedula');
        var nombre = $(this).attr('data-nombre');

        var textoEl = document.getElementById('textoConfirmarEliminar');
        if (textoEl) {
            textoEl.innerHTML = '\u00bfEst\u00e1 seguro de eliminar al cliente <b>' + nombre + '</b> de forma permanente? Esta acci\u00f3n es irreversible.';
        }

        $('#formEliminarCliente').attr('action', '/clientes/eliminar/' + cedula);

        var modalEl = document.getElementById('modalConfirmarEliminar');
        if (modalEl) {
            new bootstrap.Modal(modalEl).show();
        }
    });

    // =========================================================
    // 5. Auto-cierre de notificaciones flash tras 5 segundos
    // =========================================================
    setTimeout(function () {
        document.querySelectorAll('.alert').forEach(function (alerta) {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                var bsAlert = bootstrap.Alert.getOrCreateInstance(alerta);
                if (bsAlert) bsAlert.close();
            } else {
                alerta.remove();
            }
        });
    }, 5000);

});

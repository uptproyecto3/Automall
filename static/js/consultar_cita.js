document.addEventListener("DOMContentLoaded", function() {


    if (typeof $.fn.dataTable !== 'undefined') {
        $.fn.dataTable.ext.errMode = 'throw';
    }

    const inputFecha = document.getElementById("modal_fecha");
    let fpFecha = null;
    
    if (inputFecha && !inputFecha.hasAttribute("readonly")) {
        const fechaDefecto = typeof fecha !== 'undefined' ? fecha : "today";
        fpFecha = flatpickr("#modal_fecha", { 
            locale: "es",
            dateFormat: "Y-m-d", 
            minDate: "today", 
            defaultDate: fechaDefecto 
        });
    }


    const fpHora = flatpickr("#modal_hora", {
        locale: "es",
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i:S",
        time_24hr: true,
        minuteIncrement: 30,
        minTime: "8:00",
        maxTime: "18:00"
    });


    const tablaCitasElemento = $('#tablaCitas');
    if (tablaCitasElemento.length > 0) {
        tablaCitasElemento.DataTable({
            "dom": "<'row mb-3'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                   "<'row'<'col-sm-12'tr>>" +
                   "<'row mt-3'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            "language": {
                "lengthMenu": "Mostrar _MENU_ registros por página",
                "zeroRecords": "No se encontraron citas coincidentes",
                "info": "Mostrando página _PAGE_ de _PAGES_",
                "infoEmpty": "No hay registros disponibles",
                "search": "Buscar Cita:",
                "paginate": { "next": "Siguiente", "previous": "Anterior" }
            },
            "pageLength": 10,
            "order": [[0, "desc"]]
        });
    }

  
    if (tablaCitasElemento.length > 0) {
        
        tablaCitasElemento.on('click', '.btn-cancelar-cita', function(e) {
            e.preventDefault();
            const idDetectado = this.getAttribute('data-cod');

            if (idDetectado) {
                const btnAceptarModal = document.getElementById('btnAceptarConfirmacionUniversal');
                if (btnAceptarModal) {
                    btnAceptarModal.setAttribute('data-id-caja-fuerte', idDetectado);
                    btnAceptarModal.setAttribute('data-accion-tipo', 'eliminar');
                }

                const esCliente = document.getElementById('modal_estado') === null || document.getElementById('modal_estado').type === 'hidden';
                const tituloAccion = esCliente ? 'Cancelar Cita' : 'Eliminar Cita';
                const descAccion = esCliente ? 
                    `¿Está seguro de cancelar su cita <b>#${idDetectado}</b>? El cupo se liberará de inmediato.` :
                    `¿Está seguro de eliminar la cita <b>#${idDetectado}</b> de forma permanente? Esta acción es irreversible.`;

                abrirModalAlertaUniversal(
                    `<i class="bi bi-x-circle-fill text-danger fs-4 me-2"></i> ${tituloAccion}`,
                    descAccion,
                    'btn btn-danger px-4 fw-bold',
                    esCliente ? 'Sí, Cancelar Cita' : 'Sí, Eliminar'
                );

                const modalElemento = document.getElementById('modalConfirmacionUniversal');
                if (modalElemento) {
                    const myModal = new bootstrap.Modal(modalElemento);
                    myModal.show();
                }
            } else {
                alert("Error crítico: No se pudo extraer el ID de la fila.");
            }
        });

        tablaCitasElemento.on('click', '.btn-disparar-finalizar', function(e) {
            e.preventDefault();
            const btnFinalizar = $(this);
            const idDetectado = btnFinalizar.attr('data-cod');

            if (idDetectado) {
                const btnAceptarModal = document.getElementById('btnAceptarConfirmacionUniversal');
                if (btnAceptarModal) {
                    btnAceptarModal.setAttribute('data-id-caja-fuerte', idDetectado);
                    btnAceptarModal.setAttribute('data-accion-tipo', 'finalizar');
                }

                abrirModalAlertaUniversal(
                    '<i class="bi bi-check-circle-fill text-success fs-4 me-2"></i> Finalizar Cita',
                    `¿Desea marcar la cita <b>#${idDetectado}</b> como Concluida/Finalizada?`,
                    'btn btn-success px-4 fw-bold',
                    'Sí, Finalizar'
                );

                const modalElemento = document.getElementById('modalConfirmacionUniversal');
                if (modalElemento) {
                    const myModal = new bootstrap.Modal(modalElemento);
                    myModal.show();
                }
            }
        });

        $(document).on('click', '#btnAceptarConfirmacionUniversal', function(e) {
            e.preventDefault();
            const btnConfirmar = $(this);
            const idFinalCita = btnConfirmar.attr('data-id-caja-fuerte');
            const tipoAccion = btnConfirmar.attr('data-accion-tipo');

            if (idFinalCita) {
                btnConfirmar.prop('disabled', true).text('Procesando...');

                const formularioImprovisado = document.createElement('form');
                formularioImprovisado.method = 'POST';
                
                if (tipoAccion === 'eliminar') {
                    formularioImprovisado.action = `/eliminar/${idFinalCita}`;
                } else if (tipoAccion === 'finalizar') {
                    formularioImprovisado.action = `/finalizar/${idFinalCita}`;
                }

                const inputOculto = document.createElement('input');
                inputOculto.type = 'hidden';
                inputOculto.name = 'id_cita';
                inputOculto.value = idFinalCita;
                formularioImprovisado.appendChild(inputOculto);

                document.body.appendChild(formularioImprovisado);
                formularioImprovisado.submit();
            } else {
                alert("Error de sincronización: El ID de la cita no fue localizado.");
            }
        });

        tablaCitasElemento.on('click', '.btn-editar-cita', function() {
            const btn = $(this);
            const codCita = btn.attr('data-cod');
            const fechaCita = btn.attr('data-fecha');
            const horaCita = btn.attr('data-hora');
            const estadoCita = btn.attr('data-estado');

            // Inyectar en el modal
            $('#modal_cod_cita').val(codCita);
            $('#modal_estado').val(estadoCita);

            if (fechaCita) {
                if (fpFecha) {
                    fpFecha.setDate(fechaCita);
                } else {
                    $('#modal_fecha').val(fechaCita);
                }
            }
            
            if (horaCita && fpHora) {
                fpHora.setDate(horaCita);
            }

            $('#formModificarCita').attr('action', `/modificar/${codCita}`);
        });

        $(document).on('click', '.btn-ver-foto', function() {
            const urlImagen = $(this).attr('data-imagen');
            const tituloVehiculo = $(this).attr('data-titulo') || 'Foto del Vehículo';

            const elTitulo = document.getElementById('tituloFotoVehiculo');
            if (elTitulo) elTitulo.textContent = tituloVehiculo;

            const elCuerpo = document.getElementById('cuerpoFotoVehiculo');
            if (elCuerpo) {
                if (urlImagen && urlImagen.trim() !== '') {
                    elCuerpo.innerHTML = `<img src="${urlImagen}" class="img-fluid rounded shadow-sm" alt="${tituloVehiculo}" style="max-height: 400px; object-fit: contain;">`;
                } else {
                    elCuerpo.innerHTML = `
                        <div class="py-4 text-muted">
                            <i class="bi bi-image" style="font-size: 3rem;"></i>
                            <p class="mt-3 fw-semibold">Este vehículo no tiene foto registrada.</p>
                        </div>`;
                }
            }
        });
    }

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


function abrirModalAlertaUniversal(titulo, textoBody, clasesBoton, textoBoton) {
    const elTitulo = document.getElementById('tituloConfirmacionUniversal');
    const elTexto = document.getElementById('textoConfirmacionUniversal');
    const btnConfirmar = document.getElementById('btnAceptarConfirmacionUniversal');

    if (elTitulo) elTitulo.innerHTML = titulo;
    if (elTexto) elTexto.innerHTML = textoBody;
    if (btnConfirmar) {
        btnConfirmar.className = clasesBoton;
        btnConfirmar.textContent = textoBoton;
    }
}
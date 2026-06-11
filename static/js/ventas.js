/**
 * Automall del Centro - Módulo de Ventas
 * Manejo de lógica de interfaz y cálculos dinámicos (Versión Producción)
 */
document.getElementById('form-venta').addEventListener('submit', function(e) {
    e.preventDefault(); // Detener el envío tradicional

    // Validaciones previas
    const cedula = document.getElementById('id_cliente_hidden').value;
    const placa = document.getElementById('id_vehiculo_hidden').value;
    
    if (!cedula || !placa) {
        alert("Error: Debe seleccionar un cliente y un vehículo válidos.");
        return;
    }

    // Recopilar datos del formulario
    const formData = new FormData(this);
    
    // Antes de enviar, nos aseguramos de que los campos deshabilitados se incluyan
    const selectBanco = document.getElementById('cod_banco');
    const bancoHabilitadoOriginalmente = !selectBanco.disabled;
    selectBanco.disabled = false; 

    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Restaurar estado del select si es necesario
    if(!bancoHabilitadoOriginalmente) selectBanco.disabled = true;

    // Enviar por FETCH
    fetch(this.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(res => {
        if (res.exito) {
            alert("✅ " + res.mensaje);
            window.location.href = "/ventas/listado"; // O la ruta que prefieras
        } else {
            alert("❌ Error: " + res.mensaje);
        }
    })
    .catch(error => {
        console.error("Error en la petición:", error);
        alert("Hubo un error crítico al procesar la venta.");
    });
});



document.addEventListener('DOMContentLoaded', function() {
    // 1. Mostrar fecha de hoy con formato regional
    const hoy = new Date();
    const opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const fechaActualElement = document.getElementById('fecha-actual');
    
    if (fechaActualElement) {
        fechaActualElement.innerText = hoy.toLocaleDateString('es-ES', opciones);
    }

    // 2. Escuchar cambios en el monto recibido para recalcular deuda
    const inputMonto = document.getElementById('monto_recibido');
    if (inputMonto) {
        inputMonto.addEventListener('input', calcularBalances);
    }
});


/**
 * Carga y formatea los datos del vehículo seleccionado
 */
function buscarVehiculoPorPlaca() {
    const inputPlaca = document.getElementById('buscar_placa');
    // FORZAMOS MAYÚSCULAS en JS para asegurar consistencia en el envío
    const placa = inputPlaca.value.trim().toUpperCase(); 
    
    const lblMarcaModelo = document.getElementById('v_marca_modelo');
    const lblTipo = document.getElementById('v_tipo');
    const lblAnioColor = document.getElementById('v_anio_color');
    const lblEstado = document.getElementById('v_estado');
    const lblPrecio = document.getElementById('v_precio');
    const inputPrecioRaw = document.getElementById('v_precio_raw');
    const hiddenIdVehiculo = document.getElementById('id_vehiculo_hidden');
    
    const imgFoto = document.getElementById('v_foto');
    const divNoFoto = document.getElementById('v_no_foto');

    if (!placa) return;

    lblMarcaModelo.innerHTML = `<span class="text-muted italic small">Buscando...</span>`;

    fetch(`/ventas/api/vehiculo/${placa}`)
        .then(response => {
            if (!response.ok) throw new Error('Vehículo no encontrado');
            return response.json();
        })
        .then(data => {
            if (data.exito) {
                const v = data.vehiculo;
                
                // Inyectamos datos
                lblMarcaModelo.textContent = `${v.marca} ${v.modelo}`;
                lblTipo.textContent = v.tipo ? v.tipo : "No especificado";
                lblAnioColor.textContent = `${v.anio} / ${v.color}`;
                lblEstado.textContent = v.estado;
                
                inputPrecioRaw.value = v.precio;
                const precioFormateado = "$ " + v.precio.toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
                lblPrecio.textContent = precioFormateado;
                
                if (document.getElementById('resumen_total')) {
                    document.getElementById('resumen_total').textContent = precioFormateado;
                }

                // Forzamos visualización de "Sin Imagen" por requerimiento de la BD actual
                //imgFoto.classList.add('d-none');
                //divNoFoto.classList.remove('d-none');

                // Guardamos la placa como primary key en el campo oculto
                hiddenIdVehiculo.value = v.placa;

                // Clases de éxito de Bootstrap
                inputPlaca.classList.remove('is-invalid');
                inputPlaca.classList.add('is-valid');

                if (typeof alternarModalidadPago === 'function') {
                    alternarModalidadPago();
                } else if (typeof calcularBalances === 'function') {
                    calcularBalances();
                }
            }
        })
        .catch(error => {
            lblMarcaModelo.textContent = "-";
            lblTipo.textContent = "-";
            lblAnioColor.textContent = "-";
            lblEstado.textContent = "-";
            lblPrecio.textContent = "$ 0.00";
            inputPrecioRaw.value = 0;
            hiddenIdVehiculo.value = "";
            
            if (document.getElementById('resumen_total')) {
                document.getElementById('resumen_total').textContent = "$ 0.00";
            }

            //imgFoto.classList.add('d-none');
           //divNoFoto.classList.remove('d-none');

            // Clases de error de Bootstrap
            inputPlaca.classList.remove('is-valid');
            inputPlaca.classList.add('is-invalid');
            console.error("Error:", error);
        });
}

/**
 * Alterna visualmente el contenedor de crédito/reserva y fuerza los cálculos financieros.
 */
function alternarModalidadPago() {
    const tipoOperacion = document.getElementById('tipo_operacion').value;
    const wrapperCredito = document.getElementById('wrapper_credito');
    const inputMonto = document.getElementById('monto_recibido');
    const precioBase = parseFloat(document.getElementById('v_precio_raw').value) || 0;

    if (!wrapperCredito) return;

    if (tipoOperacion === 'credito') {
        // Mostramos los campos de deuda y fecha de vencimiento
        wrapperCredito.classList.remove('d-none');
        document.getElementById('fecha_vencimiento').required = true;
    } else {
        // Si es de contado, ocultamos y auto-llenamos el monto completo del auto
        wrapperCredito.classList.add('d-none');
        document.getElementById('fecha_vencimiento').required = false;
        
        if (precioBase > 0) {
            inputMonto.value = precioBase;
        }
    }
    
    calcularBalances();
}

/**
 * Bloquea de forma inteligente el selector de bancos nacionales si el método es Efectivo,
 * Zelle, Zinli o Binance.
 */
function evaluarMetodoPago() {
    const metodo = document.getElementById('cod_metodo').value;
    const wrBanco = document.getElementById('wrapper_banco');
    const wrRef = document.getElementById('wrapper_refencia');
    const inputRef = document.getElementById('refencia'); // ID corregido
    const lblRef = document.getElementById('label_refencia');

    // 1 = Efectivo (Ajusta este ID según tu base de datos)
    if (metodo === "1") { 
        wrBanco.classList.add('d-none');
        wrRef.classList.add('d-none');
        if (inputRef) {
            inputRef.removeAttribute('required');
            inputRef.value = "";
        }
    } else {
        wrBanco.classList.remove('d-none');
        wrRef.classList.remove('d-none');
        if (inputRef) inputRef.setAttribute('required', 'required');

        // Cambiar etiquetas según el método
        if (["5", "6", "7"].includes(metodo)) { // Digitales
            if (lblRef) lblRef.innerText = "TXID / Hash de Transferencia";
        } else {
            if (lblRef) lblRef.innerText = "Nro. de Referencia Bancaria";
        }
    }
}

/**
 * Ejecuta la matemática financiera en tiempo real adaptándose automáticamente 
 * si la transacción se liquida en Dólares o Bolívares usando la Tasa BCV.
 */
function calcularBalances() {
    // 1. Obtener valores base
    const precioUSD = parseFloat(document.getElementById('v_precio_raw').value) || 0;
    const tasaBCV = parseFloat(document.getElementById('tasa_bcv').value) || 1;
    
    // 2. Detectar Moneda Seleccionada
    const comboMoneda = document.getElementById('cod_moneda');
    if (!comboMoneda.options[comboMoneda.selectedIndex]) return;
    
    const textoMoneda = comboMoneda.options[comboMoneda.selectedIndex].text.toLowerCase();
    const simbolo = comboMoneda.options[comboMoneda.selectedIndex].getAttribute('data-simbolo') || '$';

    // 3. Lógica de Conversión (Multiplicar si es Bolívares)
    let precioConvertido = precioUSD;
    const infoTasa = document.getElementById('info_tasa_bcv');

    if (textoMoneda.includes("bolivar") || textoMoneda.includes("bs")) {
        precioConvertido = precioUSD * tasaBCV;
        if (infoTasa) {
            infoTasa.textContent = `Tasa: 1$ = ${tasaBCV.toFixed(2)} Bs.`;
            infoTasa.classList.remove('d-none');
        }
    } else {
        if (infoTasa) infoTasa.classList.add('d-none');
    }

    // 4. Actualizar etiquetas visuales de Total
    const resumenTotal = document.getElementById('resumen_total');
    if (resumenTotal) {
        resumenTotal.textContent = `${simbolo} ${precioConvertido.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    }

    // 5. Manejo de Monto Recibido y Saldo Pendiente
    const inputMontoRecibido = document.getElementById('monto_recibido');
    const inputSaldoPendiente = document.getElementById('saldo_pendiente');
    const tipoOperacion = document.getElementById('tipo_operacion').value;

    // Si es CONTADO, autollenamos el monto recibido con el total convertido
    if (tipoOperacion === 'contado') {
        inputMontoRecibido.value = precioConvertido.toFixed(2);
        if (inputSaldoPendiente) inputSaldoPendiente.value = "0.00";
    } else {
        // Si es CRÉDITO, calculamos la resta
        let montoRecibido = parseFloat(inputMontoRecibido.value) || 0;
        let deuda = precioConvertido - montoRecibido;
        if (inputSaldoPendiente) {
            inputSaldoPendiente.value = deuda > 0 ? deuda.toFixed(2) : "0.00";
        }
    }
}

/**
 * Función para buscar cliente (Estructura para FETCH)
 */
function buscarCliente() {
    const inputCedula = document.getElementById('buscar_cliente');
    const cedula = inputCedula.value;
    
    // Elementos visuales del contenedor unificado
    const lblNombre = document.getElementById('lbl_cliente_nombre');
    const lblTelefono = document.getElementById('lbl_cliente_telefono');
    const lblCorreo = document.getElementById('lbl_cliente_correo');
    const lblDireccion = document.getElementById('lbl_cliente_direccion');
    
    const hiddenId = document.getElementById('id_cliente_hidden');

    if (!cedula) return;

    // Efecto visual de carga en el contenedor
    lblNombre.innerHTML = `<span class="text-muted italic small">Buscando...</span>`;

    fetch(`/ventas/api/cliente/${cedula}`)
        .then(response => {
            if (!response.ok) throw new Error('No encontrado');
            return response.json();
        })
        .then(data => {
            if (data.exito) {
                // Inyectamos los datos reales del cliente en la ficha integrada
                lblNombre.textContent = data.nombre_completo;
                lblTelefono.textContent = data.telefono ? data.telefono : "No registrado";
                lblCorreo.textContent = data.correo ? data.correo : "No registrado";
                lblDireccion.textContent = data.direccion ? data.direccion : "No registrada";
                
                // Guardamos la cédula en el input oculto que va al formulario final
                hiddenId.value = data.cedula;
                
                // Feedback visual de éxito
                inputCedula.classList.remove('is-invalid');
                inputCedula.classList.add('is-valid');
            }
        })
        .catch(error => {
            // Limpiamos los campos en caso de error
            lblNombre.textContent = "-";
            lblTelefono.textContent = "-";
            lblCorreo.textContent = "-";
            lblDireccion.textContent = "-";
            hiddenId.value = "";
            
            // Feedback visual de error
            inputCedula.classList.remove('is-valid');
            inputCedula.classList.add('is-invalid');
            console.error("Error:", error);
        });
}

/**
 * Función para registro rápido de cliente (Estructura para AJAX)
 */
function guardarClienteRapido() {
    const cedula = document.getElementById('m_cedula').value;
    const nombre = document.getElementById('m_nombre').value;
    const apellido = document.getElementById('m_apellido').value;

    if (!cedula || !nombre || !apellido) return;

    // Aquí enviarás los datos a tu controlador de usuarios/clientes
    // Una vez guardado con éxito, cierras el modal:
    const modalElement = document.getElementById('modalCliente');
    const modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) modal.hide();
}

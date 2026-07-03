/**
 * Automall del Centro - Módulo de Ventas
 * Manejo de lógica de interfaz y cálculos dinámicos (Versión Producción Modificada)
 */

document.addEventListener('DOMContentLoaded', function() {
    // 1. Vincular los eventos de los botones (Se eliminaron los onclick directos del HTML)
    inicializarEventos();

    // 2. Mostrar fecha de hoy con formato regional
    const hoy = new Date();
    const opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const fechaActualElement = document.getElementById('fecha-actual');
    if (fechaActualElement) {
        fechaActualElement.innerText = hoy.toLocaleDateString('es-ES', opciones);
    }

    // 3. Escuchar cambios financieros en tiempo real
    const inputMonto = document.getElementById('monto_recibido');
    if (inputMonto) {
        inputMonto.addEventListener('input', calcularBalances);
    }

    const comboMetodo = document.getElementById('cod_metodo');
    if (comboMetodo) {
        comboMetodo.addEventListener('change', function() {
            evaluarMetodoPago();
            filtrarMonedasPorMetodo();
        });
    }

    const comboMoneda = document.getElementById('cod_moneda');
    if (comboMoneda) {
        comboMoneda.addEventListener('change', function() {
            actualizarSimboloMoneda();
            calcularBalances();
        });
    }

    const tipoOperacion = document.getElementById('tipo_operacion');
    if (tipoOperacion) {
        tipoOperacion.addEventListener('change', alternarModalidadPago);
    }

    const selectVehiculo = document.getElementById('select_vehiculo_lista');
    if (selectVehiculo) {
        selectVehiculo.addEventListener('change', function() {
            seleccionarDeLista(this);
        });
    }

    // 4. CONSULTA AUTOMÁTICA DE LA TASA BCV AL CARGAR LA PÁGINA
    fetch('/tasa/api/obtener_tasa')
        .then(response => {
            if (!response.ok) throw new Error("Error en red al buscar tasa");
            return response.json();
        })
        .then(data => {
            if (data.status === 'success' || data.status === 'warning') {
                const tasa = parseFloat(data.tasa);
                const inputTasaBcv = document.getElementById('tasa_bcv');
                
                if (inputTasaBcv) {
                    inputTasaBcv.value = tasa;
                    console.log("✅ Tasa BCV cargada automáticamente: " + tasa + " Bs.");
                    calcularBalances(); 
                }
            }
        })
        .catch(error => {
            console.error("❌ No se pudo cargar la tasa BCV automática:", error);
        });
});

/**
 * Vinculación limpia de Listeners del Dom
 */
function inicializarEventos() {
    document.getElementById('btn_buscar_cliente').addEventListener('click', buscarCliente);
    document.getElementById('btn_buscar_placa').addEventListener('click', buscarVehiculoPorPlaca);
    
    document.getElementById('btn_ir_paso_2').addEventListener('click', () => cambiarPaso(2));
    document.getElementById('btn_volver_paso_1').addEventListener('click', () => cambiarPaso(1));
    document.getElementById('btn_ir_paso_3').addEventListener('click', () => cambiarPaso(3));
    document.getElementById('btn_volver_paso_2').addEventListener('click', () => cambiarPaso(2));
}

// =========================================================
// FILTRADO DINÁMICO DE MONEDAS (PETICIÓN PUNTUAL REQUERIDA)
// =========================================================
function filtrarMonedasPorMetodo() {
    const comboMetodo = document.getElementById('cod_metodo');
    const comboMoneda = document.getElementById('cod_moneda');
    const comboDigital = document.getElementById('cod_mon_digital'); // <-- NUEVOS SELECTS
    const comboBanco = document.getElementById('cod_banco');           // <-- NUEVOS SELECTS
    
    if (!comboMetodo || !comboMoneda) return;

    // Función auxiliar para pasar a minúsculas y eliminar tildes
    const limpiarTexto = (txt) => {
        return (txt || '')
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
    };

    const textoMetodo = limpiarTexto(comboMetodo.options[comboMetodo.selectedIndex].text);
    let primeraOpcionValida = null;
    let opcionDolar = null; 

    // Contenedores de la interfaz
    const wrapperDigital = document.getElementById('wrapper_moneda_digital');
    const wrapperBanco = document.getElementById('wrapper_banco');     
    const wrapperMoneda = document.getElementById('wrapper_moneda');   

    // ==========================================
    // 1. CONTROL DE VISIBILIDAD Y DISBLED DE BLOQUES
    // ==========================================
    if (textoMetodo.includes('binance')) {
        // Binance: Muestra cripto, oculta Banco y Moneda tradicional
        if (wrapperDigital) wrapperDigital.style.display = 'block';
        if (wrapperBanco) wrapperBanco.style.display = 'none';
        if (wrapperMoneda) wrapperMoneda.style.display = 'none';

        // Habilitamos el envío de moneda digital, deshabilitamos banco
        if (comboDigital) comboDigital.disabled = false;
        if (comboBanco) comboBanco.disabled = true;
        comboMoneda.disabled = false; // Lo dejamos activo para que viaje en segundo plano
    } 
    else if (textoMetodo.includes('zinli') || textoMetodo.includes('zelle')) {
        // Zinli o Zelle: Oculta cripto, oculta Banco y muestra Moneda tradicional
        if (wrapperDigital) wrapperDigital.style.display = 'none';
        if (wrapperBanco) wrapperBanco.style.display = 'none'; 
        if (wrapperMoneda) wrapperMoneda.style.display = 'block';

        if (comboDigital) comboDigital.disabled = true;
        if (comboBanco) comboBanco.disabled = true;
        comboMoneda.disabled = false;
    } 
    else {
        // Efectivo, Transferencia, Pago Móvil, etc.
        if (wrapperDigital) wrapperDigital.style.display = 'none';
        if (wrapperBanco) wrapperBanco.style.display = 'block';
        if (wrapperMoneda) wrapperMoneda.style.display = 'block';

        if (comboDigital) comboDigital.disabled = true;
        if (comboBanco) comboBanco.disabled = false;
        comboMoneda.disabled = false;
    }

    // ==========================================
    // 2. FILTRADO INTERNO DE OPCIONES
    // ==========================================
    for (let i = 0; i < comboMoneda.options.length; i++) {
        const opcion = comboMoneda.options[i];
        const textoMoneda = limpiarTexto(opcion.text);
        const simbolo = limpiarTexto(opcion.getAttribute('data-simbolo') || '');
        
        let visible = false;

        const esDolar = textoMoneda.includes('dolar') || textoMoneda.includes('usd') || simbolo.includes('$');
        const esBolivar = textoMoneda.includes('bolivar') || textoMoneda.includes('bs');

        // Guardamos la opción de dólares apenas aparezca
        if (esDolar && !opcionDolar) {
            opcionDolar = opcion;
        }

        if (textoMetodo.includes('zinli') || textoMetodo.includes('zelle')) {
            if (esDolar) visible = true;
        } else if (textoMetodo.includes('efectivo') || textoMetodo.includes('transferencia') || textoMetodo.includes('pago movil')) {
            if (esDolar || esBolivar) visible = true;
        } else if (textoMetodo.includes('binance')) {
            // ¡SOLUCIÓN AQUÍ! Si es Binance, permitimos que el dólar quede "visible" (activo) 
            // internamente para que el navegador no lo bloquee al enviar el formulario
            if (esDolar) visible = true; 
        } else {
            visible = true; 
        }

        if (visible) {
            // Si estamos en Binance, no queremos alterar el display individual de las opciones
            if (!textoMetodo.includes('binance')) {
                opcion.style.display = 'block';
            }
            opcion.disabled = false;
            if (!primeraOpcionValida) primeraOpcionValida = opcion;
        } else {
            opcion.style.display = 'none';
            opcion.disabled = true;
        }
    }

    // ==========================================
    // 3. ASIGNACIÓN DE VALOR Y PRECIOS
    // ==========================================
    if (textoMetodo.includes('binance')) {
        if (opcionDolar) {
            comboMoneda.value = opcionDolar.value;
        }
    } else if (primeraOpcionValida) {
        comboMoneda.value = primeraOpcionValida.value;
    }

    if (typeof actualizarSimboloMoneda === 'function') actualizarSimboloMoneda();
    if (typeof calcularBalances === 'function') calcularBalances();
}
/**
 * Sincroniza el buscador manual y dispara la búsqueda principal.
 */
function seleccionarDeLista(selectElement) {
    const placaSeleccionada = selectElement.value;
    if (placaSeleccionada) {
        document.getElementById('buscar_placa').value = placaSeleccionada;
        buscarVehiculoPorPlaca();
    }
}

// =========================================================
// FUNCIONES DE BÚSQUEDA
// =========================================================

function buscarCliente() {
    const inputCedula = document.getElementById('buscar_cliente');
    const cedula = inputCedula.value;
    
    const lblNombre = document.getElementById('lbl_cliente_nombre');
    const lblTelefono = document.getElementById('lbl_cliente_telefono');
    const lblCorreo = document.getElementById('lbl_cliente_correo');
    const lblDireccion = document.getElementById('lbl_cliente_direccion');
    const hiddenId = document.getElementById('id_cliente_hidden');

    if (!cedula) return;

    lblNombre.innerHTML = `<span class="text-muted italic small">Buscando...</span>`;

    fetch(`/ventas/api/cliente/${cedula}`)
        .then(response => {
            if (!response.ok) throw new Error('No encontrado');
            return response.json();
        })
        .then(data => {
            if (data.exito) {
                lblNombre.textContent = data.nombre_completo;
                lblTelefono.textContent = data.telefono ? data.telefono : "No registrado";
                lblCorreo.textContent = data.correo ? data.correo : "No registrado";
                lblDireccion.textContent = data.direccion ? data.direccion : "No registrada";
                
                hiddenId.value = data.cedula;
                inputCedula.classList.remove('is-invalid');
                inputCedula.classList.add('is-valid');
            }
        })
        .catch(error => {
            lblNombre.textContent = "-";
            lblTelefono.textContent = "-";
            lblCorreo.textContent = "-";
            lblDireccion.textContent = "-";
            hiddenId.value = "";
            
            inputCedula.classList.remove('is-valid');
            inputCedula.classList.add('is-invalid');
        });
}

function buscarVehiculoPorPlaca() {
    const inputPlaca = document.getElementById('buscar_placa');
    const placa = inputPlaca.value.trim().toUpperCase(); 
    
    const lblMarcaModelo = document.getElementById('v_marca_modelo');
    const lblTipo = document.getElementById('v_tipo');
    const lblAnioColor = document.getElementById('v_anio_color');
    const lblEstado = document.getElementById('v_estado');
    const lblPrecio = document.getElementById('v_precio');
    const inputPrecioRaw = document.getElementById('v_precio_raw');
    const hiddenIdVehiculo = document.getElementById('id_vehiculo_hidden');

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
                
                lblMarcaModelo.textContent = `${v.marca} ${v.modelo}`;
                lblTipo.textContent = v.tipo ? v.tipo : "No especificado";
                lblAnioColor.textContent = `${v.anio} / ${v.color}`;
                lblEstado.textContent = v.estado;
                
                inputPrecioRaw.value = v.precio;
                lblPrecio.textContent = "$ " + v.precio.toLocaleString('en-US', {
                    minimumFractionDigits: 2, maximumFractionDigits: 2
                });
                
                hiddenIdVehiculo.value = v.placa;
                
                alternarModalidadPago();
            }
        })
        .catch(error => {
            console.error(error);
            resetFichaVehiculo();
            inputPlaca.classList.remove('is-valid');
            inputPlaca.classList.add('is-invalid');
        });
}

function resetFichaVehiculo() {
    document.getElementById('v_marca_modelo').innerText = "Seleccione un Vehículo";
    document.getElementById('id_vehiculo_hidden').value = "";
    document.getElementById('v_precio_raw').value = 0;
    document.getElementById('v_precio').innerText = "$ 0.00";
    document.getElementById('total_visual_usd').innerText = "$ 0.00";
    document.getElementById('total_visual_ves').innerText = "Bs. 0.00";
    document.getElementById('resumen_total').innerText = "$ 0.00";
}

function cambiarPaso(nuevoPaso) {
    if (nuevoPaso === 2 && !document.getElementById('id_cliente_hidden').value) {
        Swal.fire('Atención', 'Debe identificar un cliente primero', 'warning');
        return;
    }
    if (nuevoPaso === 3 && !document.getElementById('id_vehiculo_hidden').value) {
        Swal.fire('Atención', 'Debe seleccionar un vehículo válido', 'warning');
        return;
    }

    document.querySelectorAll('.step-pane').forEach(pane => pane.classList.add('d-none'));
    document.getElementById(`step-${nuevoPaso}`).classList.remove('d-none');
    window.scrollTo(0,0);
}

// =========================================================
// LÓGICA DE NEGOCIO Y CÁLCULOS FINANCIEROS (DUAL USD/VES)
// =========================================================

function calcularBalances() {
    const precioUSD = parseFloat(document.getElementById('v_precio_raw').value) || 0;
    const inputTasa = document.getElementById('tasa_bcv');
    const tasaBCV = inputTasa && parseFloat(inputTasa.value) > 0 ? parseFloat(inputTasa.value) : 1;
    
    // Calcular ambos montos exigibles de manera fija
    const precioVES = precioUSD * tasaBCV;

    // Actualizar campos fijos del desglose dual
    document.getElementById('total_visual_usd').innerText = `$ ${precioUSD.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    document.getElementById('total_visual_ves').innerText = `Bs. ${precioVES.toLocaleString('es-VE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

    const comboMoneda = document.getElementById('cod_moneda');
    if (!comboMoneda || !comboMoneda.options[comboMoneda.selectedIndex]) return;
    
    const textoMoneda = comboMoneda.options[comboMoneda.selectedIndex].text.toLowerCase();
    const simbolo = comboMoneda.options[comboMoneda.selectedIndex].getAttribute('data-simbolo') || '$';

    let precioConvertido = precioUSD;
    const esBolivar = textoMoneda.includes("bol") || textoMoneda.includes("bs") || simbolo.toLowerCase().includes("bs");

    if (esBolivar) {
        precioConvertido = precioVES;
    }

    // Mostrar el precio principal en el formato de moneda seleccionada
    const resumenTotal = document.getElementById('resumen_total');
    if (resumenTotal) {
        resumenTotal.textContent = `${simbolo} ${precioConvertido.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    }

    const inputMontoRecibido = document.getElementById('monto_recibido');
    const inputSaldoPendiente = document.getElementById('saldo_pendiente');
    const tipoOperacion = document.getElementById('tipo_operacion').value;

    if (tipoOperacion === 'contado') {
        if (inputMontoRecibido) inputMontoRecibido.value = precioConvertido.toFixed(2);
        if (inputSaldoPendiente) inputSaldoPendiente.value = "0.00";
        document.getElementById('deuda_usd').innerText = "USD: $0.00";
        document.getElementById('deuda_ves').innerText = "VES: Bs. 0.00";
    } else {
        // Cálculo de balance de crédito en ambas denominaciones
        let montoRecibido = parseFloat(inputMontoRecibido.value) || 0;
        let deudaEnMonedaActual = precioConvertido - montoRecibido;
        if (deudaEnMonedaActual < 0) deudaEnMonedaActual = 0;

        let saldoPendienteUSD = 0;
        let saldoPendienteVES = 0;

        if (esBolivar) {
            saldoPendienteVES = deudaEnMonedaActual;
            saldoPendienteUSD = deudaEnMonedaActual / tasaBCV;
        } else {
            saldoPendienteUSD = deudaEnMonedaActual;
            saldoPendienteVES = deudaEnMonedaActual * tasaBCV;
        }

        if (inputSaldoPendiente) inputSaldoPendiente.value = deudaEnMonedaActual.toFixed(2);
        
        document.getElementById('deuda_usd').innerText = `USD: $ ${saldoPendienteUSD.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2})}`;
        document.getElementById('deuda_ves').innerText = `VES: Bs. ${saldoPendienteVES.toLocaleString('es-VE', {minimumFractionDigits:2, maximumFractionDigits:2})}`;
    }
}

function actualizarSimboloMoneda() {
    const comboMoneda = document.getElementById('cod_moneda');
    if (!comboMoneda) return;
    const simbolo = comboMoneda.options[comboMoneda.selectedIndex].getAttribute('data-simbolo') || '$';
    
    document.getElementById('simbolo_moneda').innerText = simbolo;
}

function alternarModalidadPago() {
    const tipoOperacion = document.getElementById('tipo_operacion').value;
    const wrapperCredito = document.getElementById('wrapper_credito');
    
    if (!wrapperCredito) return;

    if (tipoOperacion === 'credito') {
        wrapperCredito.classList.remove('d-none');
        document.getElementById('fecha_vencimiento').required = true;
        document.getElementById('monto_recibido').value = ""; // Limpiar para que digiten el abono
    } else {
        wrapperCredito.classList.add('d-none');
        document.getElementById('fecha_vencimiento').required = false;
    }
    
    calcularBalances();
}

/**
 * EVALUAR MÉTODO: Corrección de ID ('wrapper_referencia') para ocultar correctamente en Efectivo
 */
function evaluarMetodoPago() {
    const comboMetodo = document.getElementById('cod_metodo');
    if (!comboMetodo) return;

    const textoMetodo = comboMetodo.options[comboMetodo.selectedIndex].text.toLowerCase();
    
    const wrBanco = document.getElementById('wrapper_banco');
    const wrRef = document.getElementById('wrapper_referencia'); // ID corregido con la "er" faltante
    const inputRef = document.getElementById('refencia'); 
    const lblRef = document.getElementById('label_referencia');

    // Validación estricta por texto para evitar fallas por IDs correlativos de BD
    if (textoMetodo.includes("efectivo")) { 
        if(wrBanco) wrBanco.classList.add('d-none');
        if(wrRef) wrRef.classList.add('d-none');
        if (inputRef) {
            inputRef.removeAttribute('required');
            inputRef.value = "";
        }
    } else {
        if(wrBanco) wrBanco.classList.remove('d-none');
        if(wrRef) wrRef.classList.remove('d-none');
        if (inputRef) inputRef.setAttribute('required', 'required');

        if (textoMetodo.includes("pago movil") || textoMetodo.includes("transferencia")) { 
            if (lblRef) lblRef.innerText = "Nro. de Referencia o Transacción Bancaria";
        } else {
            if (lblRef) lblRef.innerText = "Código de Referencia / ID de Pago";
        }
    }
}

// =========================================================
// INTERCEPCIÓN DEL FORMULARIO PRINCIPAL
// =========================================================
document.getElementById('form-venta').addEventListener('submit', function(e) {
    e.preventDefault();

    const cedula = document.getElementById('id_cliente_hidden').value;
    const placa = document.getElementById('id_vehiculo_hidden').value;
    
    if (!cedula || !placa) {
        Swal.fire('Error', 'Debe seleccionar un cliente y un vehículo válidos.', 'error');
        return;
    }

    const formData = new FormData(this);
    
    // Habilitar campos temporalmente para asegurar transmisión
    const selectBanco = document.getElementById('cod_banco');
    const bancoHabilitadoOriginalmente = !selectBanco.disabled;
    selectBanco.disabled = false; 

    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    if(!bancoHabilitadoOriginalmente) selectBanco.disabled = true;

    fetch(this.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(res => {
        if (res.exito) {
            Swal.fire('Éxito', res.mensaje, 'success').then(() => {
                window.location.href = "/ventas/lista_ventas";
            });
        } else {
            Swal.fire('Error', res.mensaje, 'error');
        }
    })
    .catch(error => {
        console.error("Error en la petición:", error);
        Swal.fire('Error Crítico', 'Hubo un problema procesando la venta.', 'error');
    });
});
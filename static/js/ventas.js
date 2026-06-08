/**
 * Automall del Centro - Módulo de Ventas
 * Manejo de lógica de interfaz y cálculos dinámicos (Versión Producción)
 */

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
        inputMonto.addEventListener('input', calcularDeuda);
    }
});

/**
 * Cambia la visibilidad de la sección de crédito según el tipo de operación
 */
function togglePagos() {
    const tipo = document.getElementById('tipo_operacion').value;
    const seccion = document.getElementById('seccion_credito');
    
    if (seccion) {
        if (tipo === 'credito') {
            seccion.classList.remove('d-none');
            calcularDeuda();
        } else {
            seccion.classList.add('d-none');
        }
    }
}

/**
 * Controla la disponibilidad del selector de banco según el método de pago
 */
function checkMetodo() {
    const metodo = document.getElementById('cod_metodo').value;
    const selectBanco = document.getElementById('cod_banco');
    
    if (selectBanco) {
        // Asumiendo que ID 2 es 'Efectivo' en tu tabla metodo_pago
        if (metodo === "2") { 
            selectBanco.value = "1"; // ID 1 para 'No aplica' en tabla banco
            selectBanco.disabled = true;
        } else {
            selectBanco.disabled = false;
        }
    }
}

/**
 * Carga y formatea los datos del vehículo seleccionado
 */
function cargarDatosVehiculo() {
    const select = document.getElementById('select_vehiculo');
    const opt = select.options[select.selectedIndex];

    if (opt && opt.value !== "") {
        document.getElementById('v_modelo').innerText = `${opt.dataset.marca} ${opt.dataset.modelo}`;
        document.getElementById('v_anio_color').innerText = `${opt.dataset.anio} / ${opt.dataset.color}`;
        
        const precio = parseFloat(opt.dataset.precio);
        document.getElementById('v_precio').innerText = "$ " + precio.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        
        calcularDeuda();
    }
}

/**
 * Calcula el saldo pendiente restando el abono al precio total
 */
function calcularDeuda() {
    const tipo = document.getElementById('tipo_operacion').value;
    const select = document.getElementById('select_vehiculo');
    const opt = select.options[select.selectedIndex];
    const montoInput = document.getElementById('monto_recibido');
    const deudaInput = document.getElementById('deuda_pendiente');

    if (tipo === 'credito' && opt && opt.value !== "" && montoInput && deudaInput) {
        const precio = parseFloat(opt.dataset.precio) || 0;
        const montoRecibido = parseFloat(montoInput.value) || 0;
        
        const deuda = precio - montoRecibido;
        deudaInput.value = (deuda > 0) ? deuda.toFixed(2) : "0.00";
    }
}

/**
 * Función para buscar cliente (Estructura para FETCH)
 */
function buscarCliente() {
    const inputCedula = document.getElementById('buscar_cliente');
    const cedula = inputCedula.value;
    const nombreCampo = document.getElementById('nombre_cliente');
    const hiddenId = document.getElementById('id_cliente_hidden');

    if (!cedula) return;

    // Cambiamos el estado visual para indicar que busca
    nombreCampo.value = "Buscando...";

    fetch(`/ventas/api/cliente/${cedula}`)
        .then(response => {
            if (!response.ok) throw new Error('No encontrado');
            return response.json();
        })
        .then(data => {
            if (data.exito) {
                // Llenamos los campos con los datos reales
                nombreCampo.value = data.nombre_completo;
                hiddenId.value = data.cedula;
                nombreCampo.classList.remove('is-invalid');
                nombreCampo.classList.add('is-valid');
            }
        })
        .catch(error => {
            nombreCampo.value = "";
            nombreCampo.placeholder = "Cliente no encontrado";
            nombreCampo.classList.add('is-invalid');
            hiddenId.value = "";
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
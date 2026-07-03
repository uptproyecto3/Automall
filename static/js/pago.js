/**
 * Automall - Gestión de Pagos/Abonos
 */

// Función para actualizar los cuadros de texto con la info de la deuda seleccionada
function actualizarInfoDeuda() {
    const select = document.getElementById('cod_cuentas');
    if (!select.value) return;

    const option = select.options[select.selectedIndex];
    
    const total = parseFloat(option.getAttribute('data-total')) || 0;
    const saldo = parseFloat(option.getAttribute('data-saldo')) || 0;
    
    document.getElementById('lbl_total').innerText = '$ ' + total.toLocaleString('en-US', {minimumFractionDigits: 2});
    document.getElementById('lbl_saldo').innerText = '$ ' + saldo.toLocaleString('en-US', {minimumFractionDigits: 2});
    document.getElementById('saldo_actual_val').value = saldo;
    
    calcularNuevoSaldo();
}

// Calcula cuánto quedará debiendo el cliente después del abono
function calcularNuevoSaldo() {
    const saldoActual = parseFloat(document.getElementById('saldo_actual_val').value) || 0;
    const montoAbono = parseFloat(document.getElementById('monto_pago').value) || 0;
    const nuevoSaldo = saldoActual - montoAbono;
    
    const lbl = document.getElementById('lbl_nuevo_saldo');
    lbl.innerText = '$ ' + (nuevoSaldo < 0 ? 0 : nuevoSaldo).toLocaleString('en-US', {minimumFractionDigits: 2});
    
    if (nuevoSaldo < 0) {
        lbl.classList.add('text-warning');
    } else {
        lbl.classList.remove('text-warning');
    }
}

// Control dinámico de visibilidad de Monedas, Bancos y Plataformas Cripto
function evaluarMetodo() {
    const comboMetodo = document.getElementById('cod_metodo');
    const comboMoneda = document.getElementById('cod_moneda');
    const comboBanco = document.getElementById('cod_banco'); 
    const comboDigital = document.getElementById('cod_mon_digital');

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
    const wrapperBanco = document.getElementById('div_banco');     
    const wrapperMoneda = document.getElementById('wrapper_moneda');   

    // ==========================================
    // 1. CONTROL DE VISIBILIDAD Y ENABLED/DISABLED
    // ==========================================
    if (textoMetodo.includes('binance')) {
        if (wrapperDigital) wrapperDigital.style.display = 'block';
        if (wrapperBanco) wrapperBanco.style.display = 'none';
        if (wrapperMoneda) wrapperMoneda.style.display = 'none';

        if (comboDigital) comboDigital.disabled = false;
        if (comboBanco) comboBanco.disabled = true;
        comboMoneda.disabled = false; // Se queda activo para enviar USD de fondo
    } 
    else if (textoMetodo.includes('zinli') || textoMetodo.includes('zelle')) {
        if (wrapperDigital) wrapperDigital.style.display = 'none';
        if (wrapperBanco) wrapperBanco.style.display = 'none'; 
        if (wrapperMoneda) wrapperMoneda.style.display = 'block';

        if (comboDigital) comboDigital.disabled = true;
        if (comboBanco) comboBanco.disabled = true;
        comboMoneda.disabled = false;
    } 
    else if (textoMetodo.includes('efectivo')) {
        if (wrapperDigital) wrapperDigital.style.display = 'none';
        if (wrapperBanco) wrapperBanco.style.display = 'none'; 
        if (wrapperMoneda) wrapperMoneda.style.display = 'block';

        if (comboDigital) comboDigital.disabled = true;
        if (comboBanco) comboBanco.disabled = true;
        comboMoneda.disabled = false;
    }
    else {
        // Transferencias, Pago Móvil, etc.
        if (wrapperDigital) wrapperDigital.style.display = 'none';
        if (wrapperBanco) wrapperBanco.style.display = 'block';
        if (wrapperMoneda) wrapperMoneda.style.display = 'block';

        if (comboDigital) comboDigital.disabled = true;
        if (comboBanco) comboBanco.disabled = false;
        comboMoneda.disabled = false;
    }

    // ==========================================
    // 2. FILTRADO INTERNO DE OPCIONES DE MONEDA
    // ==========================================
    for (let i = 0; i < comboMoneda.options.length; i++) {
        const opcion = comboMoneda.options[i];
        const textoMoneda = limpiarTexto(opcion.text);

        let visible = false;
        const esDolar = textoMoneda.includes('dolar') || textoMoneda.includes('usd');
        const esBolivar = textoMoneda.includes('bolivar') || textoMoneda.includes('bs');

        if (esDolar && !opcionDolar) {
            opcionDolar = opcion;
        }

        if (textoMetodo.includes('zinli') || textoMetodo.includes('zelle')) {
            if (esDolar) visible = true;
        } else if (textoMetodo.includes('binance')) {
            if (esDolar) visible = true; // Se mantiene activo internamente
        } else {
            if (esDolar || esBolivar) visible = true;
        }

        if (visible) {
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
    // 3. ASIGNACIÓN DE VALOR AUTOMÁTICO
    // ==========================================
    if (textoMetodo.includes('binance')) {
        if (opcionDolar) comboMoneda.value = opcionDolar.value;
    } else if (primeraOpcionValida) {
        comboMoneda.value = primeraOpcionValida.value;
    }
}

// Escuchador para el envío del formulario mediante Fetch
document.addEventListener('DOMContentLoaded', function() {
    // Ejecutar una primera validación al cargar la página por si hay valores preseleccionados
    evaluarMetodo();

    const formAbono = document.getElementById('form-abono');

    if (formAbono) {
        formAbono.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            // Agregamos manualmente el saldo actual del campo oculto
            data.saldo_actual = document.getElementById('saldo_actual_val').value;

            // Bloquear botón para evitar doble clic
            const btn = document.getElementById('btn-procesar');
            btn.disabled = true;
            btn.innerText = "Procesando...";

            fetch('/pagos/procesar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('El servidor respondió con un error (Código ' + response.status + ')');
                }
                return response.json();
            })
            .then(res => { 
                if (res.success) { 
                    Swal.fire({
                        title: '¡Operación Exitosa!',
                        text: res.message, 
                        icon: 'success',
                        confirmButtonText: 'Continuar'
                    }).then(() => {
                        window.location.href = "/pagos/listar_pagos"; 
                    });
                } else {
                    Swal.fire('Error de Validación', res.message || 'Error desconocido', 'error');
                    btn.disabled = false;
                    btn.innerText = "Registrar Pago";
                }
            })
            .catch(error => {
                console.error("Error detectado:", error);
                Swal.fire('Error Crítico', 'No se pudo comunicar con el sistema: ' + error.message, 'error');
                btn.disabled = false;
                btn.innerText = "Registrar Pago";
            });
        });
    }
});
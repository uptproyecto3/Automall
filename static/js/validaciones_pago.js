/**
 * Automall del Centro - Módulo de Validaciones para Control de Pagos
 * Vinculado estrictamente al DOM de la vista de Abonos/Cuentas por Cobrar.
 */

document.addEventListener("DOMContentLoaded", function () {
    // 1. SELECTORES EXACTOS DE TU VISTA DE PAGOS
    const formAbono = document.getElementById("form-abono");
    const selectCuenta = document.getElementById("cod_cuentas");
    const txtMontoPago = document.getElementById("monto_pago");
    const txtReferencia = document.querySelector('input[name="referencia"]'); // Captura por name al no tener ID
    const hdnSaldoActual = document.getElementById("saldo_actual_val");       // Campo oculto con el saldo real
    const selectMonedaDigital = document.getElementById("cod_mon_digital");
    
    // Contenedores dinámicos para validar visibilidad
    const divBanco = document.getElementById("div_banco");
    const wrapperMonedaDigital = document.getElementById("wrapper_moneda_digital");

    // ==========================================
    // CAPA 1: FILTROS Y MÁSCARAS EN TIEMPO REAL
    // ==========================================

    // Bloqueo MONTO: Evitar exponentes, signos negativos y limitar decimales
    if (txtMontoPago) {
        txtMontoPago.addEventListener("keydown", function (e) {
            if (["e", "E", "+", "-"].includes(e.key)) {
                e.preventDefault();
            }
        });

        txtMontoPago.addEventListener("input", function () {
            if (this.value.includes(".")) {
                const partes = this.value.split(".");
                if (partes[1].length > 2) {
                    this.value = partes[0] + "." + partes[1].slice(0, 2);
                }
            }
        });
    }

    // Bloqueo REFERENCIA: Permite números y letras (por si es un Hash TXID de criptomonedas)
    // Elimina caracteres especiales y espacios en blanco en tiempo real
    if (txtReferencia) {
        txtReferencia.addEventListener("input", function () {
            this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, "");
            if (this.value.length > 64) { // Límite estándar para un Hash largo de blockchain o banco
                this.value = this.value.slice(0, 64);
            }
        });
    }


    // ==========================================
    // CAPA 2: CONTROL DE SUBMIT Y LÓGICA DE NEGOCIO
    // ==========================================
    if (formAbono) {
        formAbono.addEventListener("submit", function (event) {
            let formValido = true;

            // --- 1. Validación de Selección de Cuenta con Deuda ---
            if (selectCuenta) {
                if (selectCuenta.value === "" || selectCuenta.selectedIndex === 0) {
                    mostrarError(selectCuenta, "Debe seleccionar un vehículo con deuda activa para procesar.");
                    formValido = false;
                } else {
                    quitarError(selectCuenta);
                }
            }

            // --- 2. Validación del Monto Líquido a Abonar ---
            if (txtMontoPago && hdnSaldoActual) {
                const montoAbonar = parseFloat(txtMontoPago.value);
                const saldoPendiente = parseFloat(hdnSaldoActual.value) || 0;

                if (isNaN(montoAbonar) || montoAbonar <= 0) {
                    mostrarError(txtMontoPago, "Ingrese un monto de pago válido y mayor a 0.00");
                    formValido = false;
                } 
                // REGLA DE ORO DE AUDITORÍA: No se puede abonar más de lo que se debe
                else if (montoAbonar > saldoPendiente) {
                    mostrarError(txtMontoPago, `El abono ($${montoAbonar.toFixed(2)}) no puede ser mayor al saldo pendiente ($${saldoPendiente.toFixed(2)}).`);
                    formValido = false;
                } else {
                    quitarError(txtMontoPago);
                }
            }

            // --- 3. Validación de Billetera Digital (Si está visible en pantalla) ---
            if (wrapperMonedaDigital && window.getComputedStyle(wrapperMonedaDigital).display !== "none") {
                if (selectMonedaDigital && (selectMonedaDigital.value === "" || selectMonedaDigital.selectedIndex === 0)) {
                    mostrarError(selectMonedaDigital, "Por favor seleccione la billetera/red digital de destino.");
                    formValido = false;
                } else if (selectMonedaDigital) {
                    quitarError(selectMonedaDigital);
                }
            }

            // --- 4. Validación de Referencia Bancaria o Transaccional ---
            // Se exige si el campo de banco o el de moneda digital están activos (transacciones no en efectivo)
            const requiereReferencia = 
                (divBanco && window.getComputedStyle(divBanco).display !== "none") || 
                (wrapperMonedaDigital && window.getComputedStyle(wrapperMonedaDigital).display !== "none");

            if (txtReferencia && requiereReferencia) {
                const refVal = txtReferencia.value.trim();
                if (refVal.length < 4) {
                    mostrarError(txtReferencia, "El número de referencia o TXID es obligatorio para este método de pago (Mín. 4 caracteres).");
                    formValido = false;
                } else {
                    quitarError(txtReferencia);
                }
            } else if (txtReferencia) {
                quitarError(txtReferencia); // Limpia errores si pasó a método efectivo
            }

            // DETENER EVENTO SI EXISTEN ERRORES
            if (!formValido) {
                event.preventDefault();
                event.stopPropagation();
                
                // Hace foco automático en el primer campo que falló para guiar al usuario
                const primerError = document.querySelector(".is-invalid");
                if (primerError) {
                    primerError.focus();
                }
            }
        });
    }

    // ==========================================
    // INYECCIÓN DINÁMICA DE FEEDBACK BOOTSTRAP
    // ==========================================

    function mostrarError(elemento, mensaje) {
        elemento.classList.remove("is-valid");
        elemento.classList.add("is-invalid");

        // Soporte para elementos solos o dentro de un .input-group de Bootstrap
        let contenedorPadre = elemento.closest(".input-group") || elemento.parentNode;
        let feedback = contenedorPadre.querySelector(".invalid-feedback");
        
        if (!feedback) {
            feedback = document.createElement("div");
            feedback.classList.add("invalid-feedback", "d-block", "mt-1", "text-start");
            contenedorPadre.appendChild(feedback);
        }
        feedback.innerText = mensaje;
    }

    function quitarError(elemento) {
        elemento.classList.remove("is-invalid");
        elemento.classList.add("is-valid");
        
        let contenedorPadre = elemento.closest(".input-group") || elemento.parentNode;
        let feedback = contenedorPadre.querySelector(".invalid-feedback");
        if (feedback) {
            feedback.remove();
        }
    }
});
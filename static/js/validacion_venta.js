/**
 * Automall del Centro - Módulo de Validaciones Integrado
 * Adaptado perfectamente a la estructura DOM de la vista de ventas.
 */

document.addEventListener("DOMContentLoaded", function () {
    // 1. SELECTORES EXACTOS DE TU VISTA HTML
    const formVenta = document.getElementById("form-venta");
    const txtCedula = document.getElementById("buscar_cliente"); // Campo de entrada de cédula
    const txtPlaca = document.getElementById("buscar_placa");     // Campo de entrada de placa
    const txtReferencia = document.getElementById("refencia");   // Mantiene el ID "refencia" de tu HTML
    const txtMonto = document.getElementById("monto_recibido");   // Campo de monto líquido
    const selectTipoVenta = document.getElementById("tipo_operacion"); // Contado o Crédito
    const txtFechaVencimiento = document.getElementById("fecha_vencimiento");

    // ==========================================
    // CAPA 1: BLOQUEO ESTRICTO EN TIEMPO REAL
    // ==========================================

    // Bloqueo CÉDULA: Al ser type="number", evitamos exponentes 'e', signos '+' o '-' y puntos
    if (txtCedula) {
        txtCedula.addEventListener("keydown", function (e) {
            if (["e", "E", "+", "-", "."].includes(e.key)) {
                e.preventDefault();
            }
        });

        txtCedula.addEventListener("input", function () {
            // Control de longitud máxima de 9 dígitos en tiempo real
            if (this.value.length > 9) {
                this.value = this.value.slice(0, 9);
            }
        });
    }

    // Bloqueo PLACA: Solo alfanumérico (A-Z, 0-9), sin caracteres especiales ni espacios
    if (txtPlaca) {
        txtPlaca.addEventListener("input", function () {
            this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, "");
            if (this.value.length > 8) {
                this.value = this.value.slice(0, 8);
            }
        });
    }

    // Bloqueo REFERENCIA: Solo dígitos numéricos, longitud estándar bancaria de máximo 12 caracteres
    if (txtReferencia) {
        txtReferencia.addEventListener("input", function () {
            this.value = this.value.replace(/[^0-9]/g, "");
            if (this.value.length > 12) {
                this.value = this.value.slice(0, 12);
            }
        });
    }

    // Bloqueo MONTO: Evitar exponentes o signos negativos
    if (txtMonto) {
        txtMonto.addEventListener("keydown", function (e) {
            if (["e", "E", "+", "-"].includes(e.key)) {
                e.preventDefault();
            }
        });
        
        txtMonto.addEventListener("input", function () {
            // Limitar a dos decimales si el usuario intenta escribir de más
            if (this.value.includes(".")) {
                const partes = this.value.split(".");
                if (partes[1].length > 2) {
                    this.value = partes[0] + "." + partes[1].slice(0, 2);
                }
            }
        });
    }


    // ==========================================
    // CAPA 2: VALIDACIÓN GENERAL ANTES DEL SUBMIT
    // ==========================================
    if (formVenta) {
        formVenta.addEventListener("submit", function (event) {
            let formValido = true;

            // --- Validación de Cédula (7 a 9 dígitos) ---
            if (txtCedula) {
                const cedulaVal = txtCedula.value.trim();
                if (cedulaVal.length < 7 || cedulaVal.length > 9) {
                    mostrarError(txtCedula, "La cédula debe contener entre 7 y 9 dígitos.");
                    formValido = false;
                } else {
                    quitarError(txtCedula);
                }
            }

            // --- Validación de Placa (Mínimo 6 caracteres si se usó el buscador) ---
            if (txtPlaca && txtPlaca.value.trim().length > 0) {
                const placaVal = txtPlaca.value.trim();
                if (placaVal.length < 6) {
                    mostrarError(txtPlaca, "La placa debe tener al menos 6 caracteres alfanuméricos.");
                    formValido = false;
                } else {
                    quitarError(txtPlaca);
                }
            }

            // --- Validación de Referencia Bancaria ---
            // 'wrapper_referencia' nos avisa si el campo está oculto (como en Efectivo)
            const wrapperRef = document.getElementById("wrapper_referencia");
            if (txtReferencia && wrapperRef && wrapperRef.style.display !== "none" && window.getComputedStyle(wrapperRef).display !== "none") {
                const refVal = txtReferencia.value.trim();
                if (refVal.length < 4) {
                    mostrarError(txtReferencia, "La referencia es obligatoria para este método (Mínimo 4 números).");
                    formValido = false;
                } else {
                    quitarError(txtReferencia);
                }
            } else if (txtReferencia) {
                quitarError(txtReferencia); // Si está oculto, limpiamos estados de error anteriores
            }

            // --- Validación de Monto Líquido ---
            if (txtMonto) {
                const montoVal = parseFloat(txtMonto.value);
                if (isNaN(montoVal) || montoVal <= 0) {
                    mostrarError(txtMonto, "Debe ingresar un monto numérico válido y mayor a 0.00");
                    formValido = false;
                } else {
                    quitarError(txtMonto);
                }
            }

            // --- Validación Especial: Plan de Crédito ---
            if (selectTipoVenta && selectTipoVenta.value === "credito" && txtFechaVencimiento) {
                const fechaSeleccionada = new Date(txtFechaVencimiento.value);
                const fechaHoy = new Date();
                // Resetear horas para comparar solo días
                fechaHoy.setHours(0,0,0,0);
                fechaSeleccionada.setHours(24,0,0,0); 

                if (!txtFechaVencimiento.value) {
                    mostrarError(txtFechaVencimiento, "Para ventas a crédito, la fecha de vencimiento es obligatoria.");
                    formValido = false;
                } else if (fechaSeleccionada <= fechaHoy) {
                    mostrarError(txtFechaVencimiento, "La fecha de vencimiento debe ser posterior al día de hoy.");
                    formValido = false;
                } else {
                    quitarError(txtFechaVencimiento);
                }
            }

            // FRENAR EL ENVÍO SI HAY ERRORES
            if (!formValido) {
                event.preventDefault();
                event.stopPropagation();
                
                // Enfocar el primer campo con error para mejorar la experiencia de usuario
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

        // Manejo del contenedor del mensaje de error (.invalid-feedback)
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
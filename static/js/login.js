document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formLogin');
    const contenedorErrores = document.getElementById('js-error-container');
    const botonEnviar = formulario ? formulario.querySelector('button[type="submit"]') : null;
    let intervaloCuentaRegresiva;

    // Función para activar visualmente el bloqueo en el navegador
    function activarBloqueoVisual(segundosFaltantes) {
        if (botonEnviar) botonEnviar.disabled = true; // Deshabilitamos el botón
        
        clearInterval(intervaloCuentaRegresiva);
        
        intervaloCuentaRegresiva = setInterval(() => {
            if (segundosFaltantes <= 0) {
                clearInterval(intervaloCuentaRegresiva);
                if (botonEnviar) botonEnviar.disabled = false;
                contenedorErrores.innerHTML = ''; // Limpiamos el mensaje
                return;
            }

            const minutos = Math.floor(segundosFaltantes / 60);
            const segundos = segundosFaltantes % 60;
            
            contenedorErrores.innerHTML = `
                <div class="alert alert-danger d-flex align-items-center py-2 border-0 shadow-sm mb-3" role="alert">
                    <i class="bi bi-clock-history me-2"></i>
                    <div class="small">Demasiados intentos. Formulario bloqueado. Reintente en: <b>${minutos}m ${segundos}s</b></div>
                </div>
            `;
            segundosFaltantes--;
        }, 1000);
    }

    // Al cargar la página, le preguntamos al backend si existe un bloqueo activo
    async function verificarBloqueoServidor() {
        try {
            const respuesta = await fetch('/api/chequear-bloqueo');
            const datos = await respuesta.json();
            
            if (datos.bloqueado) {
                activarBloqueoVisual(datos.segundos);
            }
        } catch (error) {
            console.error("Error al verificar estado de bloqueo:", error);
        }
    }

    // Ejecutar la verificación inicial
    verificarBloqueoServidor();

    if (formulario) {
        formulario.addEventListener('submit', function(e) {
            const correo = formulario.querySelector('input[name="email"]').value.trim();
            const password = formulario.querySelector('input[name="password"]').value.trim();
            let errores = [];
            
            // Si el botón está deshabilitado por el intervalo, no permitimos hacer nada
            if (botonEnviar && botonEnviar.disabled) {
                e.preventDefault();
                return;
            }

            // Validaciones básicas de formato anteriores
            if (!correo || !password) {
                errores.push("Todos los campos son estrictamente obligatorios.");
            }
            
            const regexCorreo = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (correo && !regexCorreo.test(correo)) {
                errores.push("El correo electrónico ingresado no tiene un formato válido.");
            }
            
            if (errores.length > 0) {
                e.preventDefault();
                contenedorErrores.innerHTML = '';
                errores.forEach(function(error) {
                    contenedorErrores.innerHTML += `
                        <div class="alert alert-danger d-flex align-items-center py-2 border-0 shadow-sm mb-3" role="alert">
                            <i class="bi bi-shield-slash-fill me-2"></i>
                            <div class="small">${error}</div>
                        </div>
                    `;
                });
            }
        });
    }
});
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("formLogin");
    const emailInput = document.getElementById("emailInput");
    const passwordInput = document.getElementById("passwordInput");
    const btnSubmit = document.getElementById("btnSubmit");
    const errorContainer = document.getElementById("js-error-container");
    const passwordHelp = document.getElementById("passwordHelp");

    // Expresión regular para correos estándar (evita caracteres raros o maliciosos)
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Función principal para validar el estado de los campos y el botón
    function validarFormulario() {
        const emailValue = emailInput.value.trim();
        const passwordValue = passwordInput.value;
        let errores = [];

        // 1. Validar formato de correo
        const correoValido = emailRegex.test(emailValue) && emailValue.length <= 35; 
        if (emailValue !== "" && !correoValido) {
            errores.push("El formato del correo no es válido o contiene caracteres no permitidos.");
        }

        // 2. Validar que la contraseña sea exactamente de 8 caracteres
        const passwordValida = passwordValue.length === 8;

        // Actualizar visualmente el texto de ayuda de la contraseña
        if (passwordValue.length > 0 && !passwordValida) {
            passwordHelp.textContent = `Llevas ${passwordValue.length} de 8 caracteres de forma obligatoria.`;
            passwordHelp.className = "form-text small text-danger mt-1";
        } else if (passwordValida) {
            passwordHelp.textContent = "¡Tamaño de contraseña correcto!";
            passwordHelp.className = "form-text small text-success mt-1";
        } else {
            passwordHelp.textContent = "Debe tener exactamente 8 caracteres.";
            passwordHelp.className = "form-text small text-muted mt-1";
        }

        // 3. Renderizar errores dinámicos en pantalla si los hay
        if (errores.length > 0) {
            errorContainer.innerHTML = `
                <div class="alert alert-warning py-2 border-0 shadow-sm mb-4 small d-flex align-items-center">
                    <i class="bi bi-exclamation-circle-fill me-2"></i>
                    <div>${errores[0]}</div>
                </div>
            `;
        } else {
            errorContainer.innerHTML = "";
        }

        // 4. Activar o apagar el botón de submit
        if (correoValido && passwordValida) {
            btnSubmit.removeAttribute("disabled");
        } else {
            btnSubmit.setAttribute("disabled", "true");
        }
    }

    // Restringir caracteres extraños en el input del correo mientras se escribe
    emailInput.addEventListener("input", function () {
        // Remueve cualquier caracter que no deba ir en un correo básico
        this.value = this.value.replace(/[^a-zA-Z0-9@._%+-]/g, "");
        validarFormulario();
    });

    // Controlar el tamaño estricto de la contraseña mientras escribe
    passwordInput.addEventListener("input", function () {
        // Si digita más de 8, lo corta inmediatamente en tiempo de ejecución
        if (this.value.length > 8) {
            this.value = this.value.slice(0, 8);
        }
        validarFormulario();
    });
});
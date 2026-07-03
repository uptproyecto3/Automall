document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("formLogin");
    const emailInput = document.getElementById("emailInput");
    const passwordInput = document.getElementById("passwordInput");
    const btnSubmit = document.getElementById("btnSubmit");
    const errorContainer = document.getElementById("js-error-container");
    const passwordHelp = document.getElementById("passwordHelp");

    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    function validarFormulario() {
        const emailValue = emailInput.value.trim();
        const passwordValue = passwordInput.value;
        let errores = [];

        // 1. Validar formato de correo
        const correoValido = emailRegex.test(emailValue) && emailValue.length <= 35; 
        if (emailValue !== "" && !correoValido) {
            errores.push("El formato del correo no es válido.");
        }

        // 2. Validar contraseña: Mínimo 8, máximo 20
        const passwordValida = passwordValue.length >= 8 && passwordValue.length <= 20;

        if (passwordValue.length > 0 && passwordValue.length < 8) {
            passwordHelp.textContent = `Te faltan ${8 - passwordValue.length} caracteres para el mínimo.`;
            passwordHelp.className = "form-text small text-danger mt-1";
        } else if (passwordValue.length > 20) {
            passwordHelp.textContent = "Has superado el límite de 20 caracteres.";
            passwordHelp.className = "form-text small text-danger mt-1";
        } else if (passwordValida) {
            passwordHelp.textContent = "¡Formato de contraseña correcto!";
            passwordHelp.className = "form-text small text-success mt-1";
        } else {
            passwordHelp.textContent = "Debe tener entre 8 y 20 caracteres.";
            passwordHelp.className = "form-text small text-muted mt-1";
        }

        if (errores.length > 0) {
            errorContainer.innerHTML = `
                <div class="alert alert-warning py-2 border-0 shadow-sm mb-4 small d-flex align-items-center">
                    <i class="bi bi-exclamation-circle-fill me-2"></i>
                    <div>${errores[0]}</div>
                </div>`;
        } else {
            errorContainer.innerHTML = "";
        }

        // Activar botón solo si ambos campos son perfectos
        btnSubmit.disabled = !(correoValido && passwordValida);
    }

    emailInput.addEventListener("input", function () {
        this.value = this.value.replace(/[^a-zA-Z0-9@._%+-]/g, "");
        validarFormulario();
    });

    passwordInput.addEventListener("input", function () {
        // Limitar físicamente la escritura a 20 caracteres
        if (this.value.length > 20) {
            this.value = this.value.slice(0, 20);
        }
        validarFormulario();
    });

    // 3. ENVIAR FORMULARIO CON FETCH API
    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // Evitamos que la página se recargue

        // Estado de carga en el botón
        btnSubmit.disabled = true;
        const originalBtnText = btnSubmit.innerHTML;
        btnSubmit.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Verificando...`;

        const data = {
            email: emailInput.value.trim(),
            password: passwordInput.value
        };

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.status === 'success') {
                // Redirigir al inicio si fue exitoso
                window.location.href = result.redirect;
            } else {
                // Mostrar error desde el servidor
                errorContainer.innerHTML = `
                    <div class="alert alert-danger py-2 border-0 shadow-sm mb-4 small d-flex align-items-center">
                        <i class="bi bi-x-circle-fill me-2"></i>
                        <div>${result.message}</div>
                    </div>`;
                btnSubmit.disabled = false;
                btnSubmit.innerHTML = originalBtnText;
            }
        } catch (error) {
            errorContainer.innerHTML = `
                <div class="alert alert-danger py-2 border-0 shadow-sm mb-4 small d-flex align-items-center">
                    <i class="bi bi-wifi-off me-2"></i>
                    <div>Error de conexión con el servidor.</div>
                </div>`;
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = originalBtnText;
        }
    });
});
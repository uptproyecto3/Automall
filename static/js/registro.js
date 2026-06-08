/**
 * AutoMall - Módulo de Usuarios
 * Validaciones en tiempo real para el formulario de registro
 */

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-registro");

    // --- 1. FILTROS DE ESCRITURA EN TIEMPO REAL ---

    // Cédula y Teléfono: Solo permiten números enteros
    const filtrarNumeros = (e) => {
        e.target.value = e.target.value.replace(/\D/g, "");
    };
    document.getElementById("cedula").addEventListener("input", filtrarNumeros);
    document.getElementById("telefono").addEventListener("input", filtrarNumeros);

    // Nombre y Apellido: Solo permiten letras de la A a la Z (incluyendo acentos y eñes)
    const filtrarLetras = (e) => {
        e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]/g, "");
    };
    document.getElementById("nombre").addEventListener("input", filtrarLetras);
    document.getElementById("apellido").addEventListener("input", filtrarLetras);

    // Correo Electrónico: Remueve espacios en blanco inmediatos al escribir
    document.getElementById("email").addEventListener("input", (e) => {
        e.target.value = e.target.value.replace(/\s/g, "");
    });


    // --- 2. CONTROLADOR AUXILIAR VISUAL DE BOOTSTRAP ---
    function aplicarEstiloValidacion(input, esValido) {
        if (esValido) {
            input.classList.remove("is-invalid");
            input.classList.add("is-valid");
            return true;
        } else {
            input.classList.remove("is-valid");
            input.classList.add("is-invalid");
            return false;
        }
    }

    // --- 3. PROCESAMIENTO GENERAL AL ENVIAR FORMULARIO ---
    form.addEventListener("submit", function (event) {
        let esFormularioValido = true;

        // Validar Cédula (Entre 6 y 8 dígitos puros)
        const inputCedula = document.getElementById("cedula");
        if (!aplicarEstiloValidacion(inputCedula, /^\d{6,8}$/.test(inputCedula.value.trim()))) {
            esFormularioValido = false;
        }

        // Validar Nombre (No vacío y máximo 50 letras)
        const inputNombre = document.getElementById("nombre");
        if (!aplicarEstiloValidacion(inputNombre, inputNombre.value.trim().length > 0 && inputNombre.value.trim().length <= 50)) {
            esFormularioValido = false;
        }

        // Validar Apellido (No vacío y máximo 50 letras)
        const inputApellido = document.getElementById("apellido");
        if (!aplicarEstiloValidacion(inputApellido, inputApellido.value.trim().length > 0 && inputApellido.value.trim().length <= 50)) {
            esFormularioValido = false;
        }

        // Validar Correo Electrónico (Estructura de expresión regular clásica)
        const inputEmail = document.getElementById("email");
        const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!aplicarEstiloValidacion(inputEmail, regexEmail.test(inputEmail.value.trim()))) {
            esFormularioValido = false;
        }

        // Validar Teléfono (Exactamente 11 dígitos numéricos, ej: 04125556677)
        const inputTelefono = document.getElementById("telefono");
        if (!aplicarEstiloValidacion(inputTelefono, /^\d{11}$/.test(inputTelefono.value.trim()))) {
            esFormularioValido = false;
        }

        // Validar Dirección (Obligatoria y acotada a un máximo de 150 caracteres)
        const inputDireccion = document.getElementById("direccion");
        if (!aplicarEstiloValidacion(inputDireccion, inputDireccion.value.trim().length > 0 && inputDireccion.value.trim().length <= 150)) {
            esFormularioValido = false;
        }

        // Validar Contraseña (Mínimo de 8 caracteres exigidos)
        const inputPassword = document.getElementById("password");
        if (!aplicarEstiloValidacion(inputPassword, inputPassword.value.length >= 8)) {
            esFormularioValido = false;
        }

        // Validar archivo de imagen (Solo si el usuario seleccionó un documento)
        const inputFoto = document.getElementById("foto_perfil");
        const fotoErrorTexto = document.getElementById("foto-error-msg");
        
        if (inputFoto.files.length > 0) {
            const imagen = inputFoto.files[0];
            const formatosValidos = /(\.jpg|\.jpeg|\.png|\.webp)$/i;
            const tamañoMaximoBytes = 3 * 1024 * 1024; // 3 Megabytes

            if (!formatosValidos.exec(imagen.name) || imagen.size > tamañoMaximoBytes) {
                fotoErrorTexto.innerText = "Error: La imagen debe ser JPG, PNG o WEBP y pesar menos de 3MB.";
                fotoErrorTexto.className = "form-text mt-2 text-danger fw-bold";
                esFormularioValido = false;
            } else {
                fotoErrorTexto.innerText = "Imagen cargada correctamente.";
                fotoErrorTexto.className = "form-text mt-2 text-success fw-bold";
            }
        }

        // Si se detectó alguna violación de las reglas, detenemos el envío inmediato
        if (!esFormularioValido) {
            event.preventDefault();
            event.stopPropagation();

            // Desplazamiento sutil hacia el primer input con problemas de validación
            const primerCampoInvalido = document.querySelector(".is-invalid");
            if (primerCampoInvalido) {
                primerCampoInvalido.scrollIntoView({ behavior: "smooth", block: "center" });
            }
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');

    // 1. Validaciones visuales en tiempo real
    inputs.forEach(input => {
        ['input', 'blur'].forEach(evt => {
            input.addEventListener(evt, () => validarCampo(input));
        });
    });

    function validarCampo(input) {
        let esValido = true;
        const valor = input.value.trim();

        // VALIDACIÓN BÁSICA: Vacío
        if (valor === "") {
            esValido = false;
        }

        // --- VALIDACIONES CON LÍMITES ESPECÍFICOS ---

        // 1. COLOR: Solo letras y espacios (NADA de números) y límite de 20 caracteres
        if (input.name === 'color') {
            const regexSoloLetras = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
            if (!regexSoloLetras.test(valor) || valor.length > 20) {
                esValido = false;
            }
        }

        // 2. PLACA: Letras, números y guiones. Entre 3 y 10 caracteres.
        if (input.name === 'placa') {
            const regexPlaca = /^[A-Z0-9-]{3,10}$/i;
            if (!regexPlaca.test(valor)) esValido = false;
        }

        // 3. AÑO: Entre 1900 y el año actual + 1
        if (input.name === 'anio') {
            const anioActual = new Date().getFullYear();
            const anioIngresado = parseInt(valor);
            if (anioIngresado < 1886 || anioIngresado > anioActual + 1) {
                esValido = false;
            }
        }

        // 4. KILOMETRAJE: Máximo 1,000,000 km (Límite lógico)
        if (input.name === 'kilometraje') {
            const km = parseFloat(valor);
            if (km < 0 || km > 1000000) esValido = false;
        }

        // 5. PRECIO: Máximo 1,000,000 (O el límite que prefieras)
        if (input.name === 'precio') {
            const precio = parseFloat(valor);
            if (precio <= 0 || precio > 5000000) esValido = false;
        }

        // 6. TEXTOS (Tipo, Descripción): Límite de caracteres
        if (input.name === 'tipo' && valor.length > 30) esValido = false;
        if (input.name === 'descripcion_catalogo' && valor.length > 500) esValido = false;

        // --- APLICAR COLORES DE BOOTSTRAP ---
        if (esValido) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
        }
        return esValido;
    }

    // 2. Manejo del Envío (Fetch API)
    form.addEventListener('submit', async function (e) {
        e.preventDefault(); 

        let formValido = true;
        inputs.forEach(input => {
            if (!validarCampo(input)) formValido = false;
        });

        if (!formValido) {
            Swal.fire({
                icon: 'warning',
                title: 'Datos inválidos',
                text: 'Por favor, revise los campos en rojo. Asegúrese de que el color no tenga números y los rangos sean correctos.',
                confirmButtonColor: '#3085d6'
            });
            return;
        }

        Swal.fire({
            title: 'Guardando...',
            allowOutsideClick: false,
            didOpen: () => { Swal.showLoading(); }
        });

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: '¡Registrado!',
                    text: result.message,
                    timer: 2000,
                    showConfirmButton: false
                }).then(() => {
                    window.location.href = "/vehiculos-lista"; 
                });
            } else {
                // Aquí aparecerá el error si la placa está duplicada (desde el backend)
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: result.message,
                    confirmButtonColor: '#d33'
                });
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error fatal',
                text: 'No se pudo conectar con el servidor.',
            });
        }
    });
});
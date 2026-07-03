
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    const formulario = document.querySelector('.needs-validation');

    if (formulario) {
        formulario.addEventListener('submit', function (event) {
            if (!formulario.checkValidity()) {
                event.preventDefault();  
                event.stopPropagation();  
            }

            formulario.classList.add('was-validated');
        }, false);
    }


    const toastElements = [].slice.call(document.querySelectorAll('.toast'));
    
    toastElements.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, { 
            delay: 5000,
            autohide: true 
        });
    });
});
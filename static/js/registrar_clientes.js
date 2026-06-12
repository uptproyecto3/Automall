/**
 * AutoMall - Módulo de Clientes
 * Validación Frontend (Bootstrap) y Control de Toasts Flotantes
 */

document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // 1. CONTROL DE VALIDACIÓN VISUAL (CSS VERDE / ROJO)
    // Buscamos el formulario que tiene la clase 'needs-validation'
    const formulario = document.querySelector('.needs-validation');

    if (formulario) {
        formulario.addEventListener('submit', function (event) {
            // Si el formulario no es válido según los atributos (required, type="email", etc.)
            if (!formulario.checkValidity()) {
                event.preventDefault();    // Frenamos el envío al servidor
                event.stopPropagation();   // Detenemos la propagación del evento
            }

            // Agregamos la clase de Bootstrap que activa el CSS de validación instantánea
            formulario.classList.add('was-validated');
        }, false);
    }

    // 2. CONTROL DE ALERTAS FLOTANTES DEL SERVIDOR (TOASTS BACKEND)
    // Buscamos todos los Toasts que hayan emergido desde Flask
    const toastElements = [].slice.call(document.querySelectorAll('.toast'));
    
    // Los inicializamos configurando un autocierre automático a los 5 segundos (5000ms)
    toastElements.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, { 
            delay: 5000,
            autohide: true 
        });
    });
});

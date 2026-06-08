document.addEventListener('DOMContentLoaded', function() {
    
    const botonesEditar = document.querySelectorAll('.btn-editar-marca');
    const modalElement = document.getElementById('modalEditarMarca');
    const modalEditar = new bootstrap.Modal(modalElement);
    const formEditar = document.getElementById('formEditarMarca');

    botonesEditar.forEach(boton => {
        boton.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const nombre = this.getAttribute('data-nombre');
            const estado = this.getAttribute('data-estado');

            // Cargar datos en los inputs del modal
            document.getElementById('edit_nombre_marca').value = nombre;
            document.getElementById('edit_estado_marca').value = estado;

            // Ajustar la URL del formulario
            formEditar.action = `/marcas/editar/${id}`;

            modalEditar.show();
        });
    });

    const formulariosEliminar = document.querySelectorAll('.form-eliminar');
    formulariosEliminar.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('¿Estás seguro de que deseas eliminar esta marca?')) {
                e.preventDefault();
            }
        });
    });
});
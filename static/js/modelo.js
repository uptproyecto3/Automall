document.addEventListener('DOMContentLoaded', function() {
    
    // Lógica para abrir el Modal de Edición y cargar los datos
    const botonesEditar = document.querySelectorAll('.btn-editar');
    const modalEditar = new bootstrap.Modal(document.getElementById('modalEditar'));
    const formEditar = document.getElementById('formEditar');

    botonesEditar.forEach(boton => {
        boton.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const nombre = this.getAttribute('data-nombre');
            const marcaId = this.getAttribute('data-marca');
            const estado = this.getAttribute('data-estado');

            document.getElementById('edit_nombre_modelo').value = nombre;
            document.getElementById('edit_cod_marca').value = marcaId;
            document.getElementById('edit_estado').value = estado;

            formEditar.action = `/modelos/editar/${id}`;
            modalEditar.show();
        });
    });

    const formulariosEliminar = document.querySelectorAll('.form-eliminar');
    formulariosEliminar.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('¿Estás seguro de que deseas eliminar este modelo? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
});
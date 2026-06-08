from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.marca import Marca
from utils.permisos import requiere_permiso

marca_bp = Blueprint('marca', __name__)


@marca_bp.route('/vehiculos/marca_registro', methods=['GET', 'POST'])
@requiere_permiso('Vehiculos', 'p_crear')
def registro_marca():
    if request.method == 'POST':
        nombre = request.form['nombre_marca']
        estado = request.form['estado']
        Marca.guardar(nombre, estado)
        flash("Marca registrada con éxito")
        return redirect(url_for('marca.registro_marca')) # Recargamos la misma página
            
    marcas = Marca.obtener_todas()
    return render_template('vehiculos/marca_registro.html', marcas=marcas)

@marca_bp.route('/marcas/editar/<int:id>', methods=['POST'])
@requiere_permiso('Vehiculos', 'p_actualizar')
def editar_marca(id):
    nombre = request.form['nombre_marca']
    estado = request.form['estado']
    Marca.actualizar(id, nombre, estado)
    flash("Marca actualizada correctamente", "success")
    return redirect(url_for('marcas.registro_marca'))

@marca_bp.route('/marcas/eliminar/<int:id>', methods=['POST'])
@requiere_permiso('Vehiculos', 'p_eliminar')
def eliminar_marca(id):
    try:
        Marca.eliminar(id)
        flash("Marca eliminada correctamente", "warning")
    except Exception as e:
        flash("No se puede eliminar la marca porque tiene modelos asociados", "danger")
    return redirect(url_for('marcas.registro_marca'))
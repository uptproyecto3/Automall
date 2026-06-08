from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.modelo import Modelo
from models.marca import Marca
from utils.permisos import requiere_permiso

modelo_bp = Blueprint('modelos', __name__)

@modelo_bp.route('/modelos/registro', methods=['GET', 'POST'])
@requiere_permiso('Vehiculos', 'p_crear')
def registro_modelo():
    if request.method == 'POST':
        nombre = request.form['nombre_modelo']
        estado = request.form['estado']
        cod_marca = request.form['cod_marca'] 
        Modelo.guardar(nombre, estado, cod_marca)
        flash("Modelo registrado con éxito")
        return redirect(url_for('modelos.registro_modelo'))
            
    modelos = Modelo.obtener_todas()
    marcas = Marca.obtener_todas() 
    return render_template('vehiculos/modelo_registro.html', modelos=modelos, marcas=marcas)

@modelo_bp.route('/modelos/editar/<int:id>', methods=['POST'])
@requiere_permiso('Vehiculos', 'p_actualizar') 
def editar_modelo(id):
    nombre = request.form['nombre_modelo']
    estado = request.form['estado']
    cod_marca = request.form['cod_marca']
    Modelo.actualizar(id, nombre, estado, cod_marca)
    flash("Modelo actualizado correctamente", "success")
    return redirect(url_for('modelos.registro_modelo'))

@modelo_bp.route('/modelos/eliminar/<int:id>', methods=['POST'])
@requiere_permiso('Vehiculos', 'p_eliminar')
def eliminar_modelo(id):
    Modelo.eliminar(id)
    flash("Modelo eliminado correctamente", "warning")
    return redirect(url_for('modelos.registro_modelo'))
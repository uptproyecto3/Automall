from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.modelo import Modelo
from utils.permisos import requiere_permiso

modelo_bp = Blueprint('modelos', __name__)

@modelo_bp.route('/modelos/registro', methods=['GET', 'POST'])
@requiere_permiso('Vehiculos', 'p_crear')
def registro_modelo():
    if request.method == 'POST':
        nombre = request.form['nombre_modelo']
        estado = request.form['estado']
        Modelo.guardar(nombre, estado)
        flash("Modelo registrado con éxito")
        return redirect(url_for('modelos.registro_modelo')) # Recargamos la misma página
            
    # OBTENEMOS LOS MODELOS TAMBIÉN AQUÍ:
    modelos = Modelo.obtener_todas()
    return render_template('vehiculos/modelo_registro.html', modelos=modelos)
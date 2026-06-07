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
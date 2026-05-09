import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.vehiculo import Vehiculo
from werkzeug.utils import secure_filename
from utils.permisos import requiere_permiso

vehiculos_bp = Blueprint('vehiculos', __name__)

@vehiculos_bp.route('/registro_vehiculo', methods=['GET', 'POST'])
@requiere_permiso('Vehiculos', 'p_crear')
def registro():
    if request.method == 'POST':
        file = request.files['imagen']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads', filename))
        
        Vehiculo.guardar(
            request.form['placa'], request.form['color'], request.form['anio'],
            request.form['tipo'], 'Disponible', request.form['marca'],
            request.form['modelo'], request.form['cedula'], filename
        )
        flash("¡Vehículo registrado!")
        return redirect(request.url)
        
    return render_template('vehiculos/registro.html')


@vehiculos_bp.route('/lista')
@requiere_permiso('Usuarios', 'p_leer')
def lista():
    vehiculos = Vehiculo.obtener_todos()
    
    page = request.args.get('page', 1, type=int)
    per_page = 6
    total = len(vehiculos)
    start = (page - 1) * per_page
    end = start + per_page
    
    vehiculos_paginados = vehiculos[start:end]
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)
    
    return render_template('vehiculos/lista.html', 
                           vehiculos=vehiculos_paginados, 
                           page=page, 
                           total_pages=total_pages)

@vehiculos_bp.route('/eliminar/<int:id>')
@requiere_permiso('Vehículos', 'p_eliminar') # <--- Si no tiene p_eliminar=1 en la BD, no entra
def eliminar(id):
    # Esta línea nunca se ejecutará si el usuario no tiene permiso
    Vehiculo.eliminar(id) 
    flash("Vehículo eliminado")
    return redirect(url_for('vehiculos.lista'))
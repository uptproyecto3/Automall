from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.propietario import Propietario
from utils.permisos import requiere_permiso

propietario_bp = Blueprint('propietarios', __name__)

# RUTA 1: VISTA DE REGISTRO
@propietario_bp.route('/propietarios/registro', methods=['GET', 'POST'])
@requiere_permiso('Propietario', 'p_crear')
def registro():
    if request.method == 'POST':
        Propietario.guardar(
            request.form['cedula'], request.form['razon_social'],
            request.form['telefono'], request.form['direccion'],
            request.form['tipo'], request.form['estado']
        )
        flash("Propietario registrado con éxito")
        return redirect(url_for('propietarios.lista')) # Al guardar, vamos a la lista

    return render_template('usuarios/propietario_registro.html')

# RUTA 2: VISTA DE LISTADO
@propietario_bp.route('/propietarios/lista')
@requiere_permiso('Propietario', 'p_leer')
def lista():
    propietarios = Propietario.obtener_todos()
    return render_template('usuarios/propietario_lista.html', propietarios=propietarios)

# RUTA PARA ELIMINAR
@propietario_bp.route('/propietarios/eliminar/<int:cedula>')
def eliminar(cedula):
    Propietario.eliminar(cedula)
    flash("Propietario eliminado")
    return redirect(url_for('propietarios.lista'))
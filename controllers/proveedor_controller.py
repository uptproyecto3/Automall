from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.proveedor import Proveedor
from utils.permisos import requiere_permiso

proveedor_bp = Blueprint('proveedores', __name__)

# RUTA 1: VISTA DE REGISTRO
@proveedor_bp.route('/proveedores/registro', methods=['GET', 'POST'])
@requiere_permiso('Vehiculos', 'p_crear')
def registro():
    if request.method == 'POST':
        Proveedor.guardar(
            request.form['cedula'], request.form['razon_social'],
            request.form['telefono'], request.form['direccion'],
            request.form['tipo'], request.form['estado']
        )
        flash("Proveedor registrado con éxito")
        return redirect(url_for('proveedores.lista')) # Al guardar, vamos a la lista
            
    return render_template('usuarios/proveedor_registro.html')

# RUTA 2: VISTA DE LISTADO
@proveedor_bp.route('/proveedores/lista')
@requiere_permiso('Vehiculos', 'p_leer')
def lista():
    proveedores = Proveedor.obtener_todos()
    return render_template('usuarios/proveedor_lista.html', proveedores=proveedores)

# RUTA PARA ELIMINAR
@proveedor_bp.route('/proveedores/eliminar/<int:cedula>')
def eliminar(cedula):
    Proveedor.eliminar(cedula)
    flash("Proveedor eliminado")
    return redirect(url_for('proveedores.lista'))
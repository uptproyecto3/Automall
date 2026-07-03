from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.insumo import Insumo
from utils.decorators import login_required
from utils.permisos import requiere_permiso
from models.bitacora import Bitacora

insumo_bp = Blueprint('insumos', __name__, url_prefix='/insumos')


@insumo_bp.route('/')
@login_required
@requiere_permiso('Insumos', 'p_leer')
def listar():
    insumos = Insumo.obtener_todos()
    return render_template('insumos/index.html', insumos=insumos)


@insumo_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@requiere_permiso('Insumos', 'p_crear')
def nuevo():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        stock = int(request.form.get('stock', 0))
        
        if not nombre:
            flash("El nombre del insumo es obligatorio", "danger")
            return render_template('insumos/nuevo.html')
        
        Insumo.crear(nombre, descripcion, stock)
        Bitacora.registrar(
            session['cedula_usuario'],
            f"Creó nuevo insumo: {nombre}",
            "Insumos"
        )
        flash("Insumo creado correctamente", "success")
        return redirect(url_for('insumos.listar'))
    
    return render_template('insumos/nuevo.html')


@insumo_bp.route('/editar/<int:cod_insumo>', methods=['POST'])
@login_required
@requiere_permiso('Insumos', 'p_actualizar')
def editar(cod_insumo):
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    stock = int(request.form.get('stock', 0))
    
    Insumo.actualizar(cod_insumo, nombre, descripcion, stock)
    Bitacora.registrar(
        session['cedula_usuario'],
        f"Actualizó insumo: {nombre}",
        "Insumos"
    )
    flash("Insumo actualizado correctamente", "success")
    return redirect(url_for('insumos.listar'))


@insumo_bp.route('/eliminar/<int:cod_insumo>')
@login_required
@requiere_permiso('Insumos', 'p_eliminar')
def eliminar(cod_insumo):
    insumo = Insumo.obtener_por_id(cod_insumo)
    if insumo:
        Insumo.eliminar(cod_insumo)
        Bitacora.registrar(
            session['cedula_usuario'],
            f"Eliminó insumo: {insumo['nombre_insumo']}",
            "Insumos"
        )
        flash("Insumo eliminado correctamente", "success")
    return redirect(url_for('insumos.listar'))
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.compra import Compra
from models.insumo import Insumo
from models.vehiculo import Vehiculo
from utils.decorators import login_required
from utils.permisos import requiere_permiso
from models.bitacora import Bitacora
from models.db import obtener_conexion

compra_bp = Blueprint('compras', __name__, url_prefix='/compras')


@compra_bp.route('/')
@login_required
@requiere_permiso('Compras', 'p_leer')
def listar():
    """Lista todas las compras"""
    compras = Compra.obtener_todos()
    return render_template('compras/index.html', compras=compras)


@compra_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@requiere_permiso('Compras', 'p_crear')
def nueva_compra():
    """Crear una nueva compra (cabecera)"""
    if request.method == 'POST':
        cod_compras = Compra.crear()
        flash(f"Compra #{cod_compras} creada. Agregue los detalles.", "success")
        return redirect(url_for('compras.agregar_detalle', cod_compras=cod_compras))
    
    return render_template('compras/nueva.html')


@compra_bp.route('/compra/<int:cod_compras>/detalle', methods=['GET', 'POST'])
@login_required
@requiere_permiso('Compras', 'p_actualizar')
def agregar_detalle(cod_compras):
    """Agregar detalles a una compra existente"""
    compra = Compra.obtener_por_id(cod_compras)
    insumos = Insumo.obtener_todos()
    vehiculos = Vehiculo.obtener_vehiculos_activos()
    
    if request.method == 'POST':
        cod_insumo = request.form.get('cod_insumo')
        producto = request.form.get('producto')
        cantidad = int(request.form.get('cantidad'))
        costo_unitario = float(request.form.get('costo_unitario'))
        placa = request.form.get('placa')
        
        # Validar que el campo producto no esté vacío
        if not producto:
            flash("El nombre del producto es obligatorio", "danger")
            return redirect(url_for('compras.agregar_detalle', cod_compras=cod_compras))
        
        Compra.agregar_detalle(cod_compras, cod_insumo if cod_insumo else None, 
                               producto, cantidad, costo_unitario, placa)
        
        Bitacora.registrar(
            session['cedula_usuario'],
            f"Agregó detalle a compra #{cod_compras}: {producto} x{cantidad}",
            "Compras"
        )
        
        flash("Detalle agregado correctamente", "success")
        return redirect(url_for('compras.agregar_detalle', cod_compras=cod_compras))
    
    return render_template('compras/detalle.html', compra=compra, insumos=insumos, vehiculos=vehiculos)


@compra_bp.route('/compra/<int:cod_compras>/finalizar')
@login_required
@requiere_permiso('Compras', 'p_actualizar')
def finalizar_compra(cod_compras):
    """Finalizar una compra (cambiar estado a Completada)"""
    Compra.finalizar_compra(cod_compras)
    Bitacora.registrar(
        session['cedula_usuario'],
        f"Finalizó compra #{cod_compras}",
        "Compras"
    )
    flash("Compra finalizada correctamente", "success")
    return redirect(url_for('compras.listar'))


@compra_bp.route('/compra/<int:cod_compras>/eliminar')
@login_required
@requiere_permiso('Compras', 'p_eliminar')
def eliminar_compra(cod_compras):
    """Eliminar una compra completa"""
    Compra.eliminar_compra(cod_compras)
    Bitacora.registrar(
        session['cedula_usuario'],
        f"Eliminó compra #{cod_compras}",
        "Compras"
    )
    flash("Compra eliminada", "success")
    return redirect(url_for('compras.listar'))


@compra_bp.route('/detalle/<int:cod_det_compra>/eliminar/<int:cod_compras>')
@login_required
@requiere_permiso('Compras', 'p_eliminar')
def eliminar_detalle(cod_det_compra, cod_compras):
    """Eliminar un detalle específico de una compra"""
    # Obtener información del detalle antes de eliminar
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT cod_insumo, cantidad FROM det_compra WHERE cod_det_compra = %s", (cod_det_compra,))
    detalle = cursor.fetchone()
    cursor.close()
    conexion.close()
    
    if detalle:
        Compra.eliminar_detalle(cod_det_compra, cod_compras, detalle['cod_insumo'], detalle['cantidad'])
        Bitacora.registrar(
            session['cedula_usuario'],
            f"Eliminó detalle de compra #{cod_compras}",
            "Compras"
        )
        flash("Detalle eliminado", "success")
    
    return redirect(url_for('compras.agregar_detalle', cod_compras=cod_compras))
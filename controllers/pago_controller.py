from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.pagos import Pagos
from models.ventas import Ventas
from utils.decorators import login_required
from utils.permisos import requiere_permiso

pagos_bp = Blueprint('pagos', __name__)

    # =========================================================================
    # METODOS DE LISTADO DE PAGOS PARA CLIENTE
    # =========================================================================

@pagos_bp.route('/pagos/listar_pagos')
@login_required
@requiere_permiso('Pagos', 'p_leer')
def listar_pagos():
    cedula_usuario = session.get('cedula_usuario')
    pagos = Pagos.obtener_todos(cedula_usuario)
    return render_template('pagos/lista_pagos.html', pagos=pagos)

    # =========================================================================
    # METODOS DE LISTADO DE PAGOS PARA ADMINISTRADOR
    # =========================================================================

@pagos_bp.route('/pagos/listar_admin')
@login_required  
@requiere_permiso('Pagosadmin', 'p_leer')
def listar_pagos_admin():
    pagos = Pagos.obtener_todos_admin()
    return render_template('pagos/lista_admin.html', pagos=pagos)

    # =========================================================================
    # METODOS DE PARA VISTA DE REGISTRO DE PAGOS
    # =========================================================================

@pagos_bp.route('/pagos/registrar_pago')
@login_required
def registrar_pago():
    cedula = session.get('cedula_usuario')
    deudas = Pagos.obtener_deudas_pendientes(cedula)
    metodos = Ventas.obtener_metodos_pago() 
    monedas = Ventas.obtener_monedas()
    monedas_digitales = Ventas.obtener_moneda_digital()
    bancos = Ventas.obtener_bancos()
    
    return render_template('pagos/registrar.html', deudas=deudas, metodos=metodos, monedas=monedas, monedas_digitales=monedas_digitales, bancos=bancos)

    # =========================================================================
    # METÓDOS DE PROCESAMIENTO DE PAGOS
    # =========================================================================

@pagos_bp.route('/pagos/procesar', methods=['POST'])
@login_required
@requiere_permiso('Pagos', 'p_crear')
def procesar_pago():
    data = request.get_json()
    
    # --- ENCAPSULAMIENTO APLICADO ---
    # Instanciamos el objeto con los datos recibidos del JSON
    pago_objeto = Pagos(data)
    resultado = pago_objeto.procesar_abono()
    
    if resultado["status"]:
        return jsonify({"success": True, "message": "Abono procesado con éxito"})
    return jsonify({"success": False, "message": resultado["error"]})

    # =========================================================================
    # ELIMINAR PAGO (MÉTODO MODIFICADO PARA ELIMINACIÓN LÓGICA)
    # =========================================================================

@pagos_bp.route('/pagos/eliminar/<int:id>')
@login_required
@requiere_permiso('Pagos', 'p_eliminar')
def eliminar_pago(id):
    # Llama al método modificado que ahora hace el UPDATE dinámico
    if Pagos.eliminar(id):
        flash("Pago anulado exitosamente. El saldo pendiente ha sido restaurado.", "success")
    else:
        flash("No se pudo procesar la anulación del pago.", "danger")
    
    return redirect(request.referrer or url_for('pagos.listar_pagos'))
    
    
    # =========================================================================
    # EDITAR PAGO (MÉTODO NUEVO)
    # =========================================================================


@pagos_bp.route('/pagos/editar', methods=['POST'])
@login_required
@requiere_permiso('Pagos', 'p_actualizar')
def editar_pago():
    data = request.form.to_dict()
    
    # --- ENCAPSULAMIENTO APLICADO ---
    # Instanciamos el objeto con los datos del formulario mutado
    pago_objeto = Pagos(data)
    
    if pago_objeto.actualizar():
        flash("Pago actualizado correctamente.", "success")
    else:
        flash("Error al actualizar el pago.", "danger")
        
    return redirect(request.referrer or url_for('pagos.listar_pagos'))
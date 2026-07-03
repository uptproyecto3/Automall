from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask import jsonify
from models.ventas import Ventas
from models.user import Usuario
from models.vehiculo import Vehiculo
from utils.decorators import login_required
from utils.permisos import requiere_permiso

ventas_bp = Blueprint('ventas', __name__)

# --- RUTA 1: PARA VER EL FORMULARIO ---
@ventas_bp.route('/ventas/registrar_venta', methods=['GET'])
@login_required
def vista_registro():
    bancos = Ventas.obtener_bancos()
    metodos_pago = Ventas.obtener_metodos_pago()
    monedas = Ventas.obtener_monedas()
    monedas_digitales = Ventas.obtener_moneda_digital()
    vehiculos = Vehiculo.obtener_vehiculos_disponibles()

    return render_template('ventas/registrar_venta.html', bancos=bancos, metodos_pago=metodos_pago, monedas=monedas, monedas_digitales=monedas_digitales, vehiculos=vehiculos)

@ventas_bp.route('/ventas/api/cliente/<int:cedula>', methods=['GET'])
@login_required
def api_buscar_cliente(cedula):
    # El modelo ahora se encarga de buscar y estructurar todo el diccionario
    respuesta = Usuario.buscar_cliente_por_cedula(cedula)
    
    if respuesta:
        return jsonify(respuesta)
    else:
        return jsonify({
            'exito': False, 
            'mensaje': 'Cliente no encontrado o no tiene rol de cliente'
        }), 404
    
@ventas_bp.route('/ventas/api/vehiculo/<string:placa>', methods=['GET'])
@login_required
def api_buscar_vehiculo(placa):
    # El modelo ahora se encarga de buscar, limpiar y formatear el vehículo
    respuesta = Vehiculo.buscar_por_placa(placa)
    
    if respuesta:
        return jsonify(respuesta)
    else:
        return jsonify({
            'exito': False,
            'mensaje': 'Vehículo no encontrado o no disponible para la venta'
        }), 404
    

# --- RUTA 2: PARA PROCESAR EL GUARDADO ---
@ventas_bp.route('/ventas/registrar_venta', methods=['POST'])
@login_required
@requiere_permiso('Ventas', 'p_crear')
def registrar_venta():
    data = request.get_json()
    
    if not data:
        return jsonify({"exito": False, "mensaje": "No se recibieron datos"})

    nueva_venta = Ventas(data)

    resultado = nueva_venta.registrar()

    if resultado["status"]:
        return jsonify({"exito": True, "mensaje": "Venta y pagos registrados exitosamente"})
    else:
        return jsonify({"exito": False, "mensaje": resultado["error"]})
    
@ventas_bp.route('/ventas/lista_ventas')
@login_required
@requiere_permiso('Ventas', 'p_leer')
def listado_ventas():
    ventas = Ventas.obtener_todas()
    return render_template('ventas/lista_ventas.html', ventas=ventas)

@ventas_bp.route('/ventas/eliminar/<int:id>')
@login_required
@requiere_permiso('Ventas', 'p_eliminar')
def eliminar_venta(id):
    if Ventas.eliminar(id):
        flash("Venta eliminada y vehículo liberado con éxito.", "success")
    else:
        flash("Error al eliminar la venta.", "danger")
    return redirect(url_for('ventas.listado_ventas'))

@ventas_bp.route('/ventas/editar', methods=['POST'])
@login_required
@requiere_permiso('Ventas', 'p_actualizar')
def editar_venta():
    data = request.form.to_dict()
    if Ventas.actualizar(data):
        flash("Venta actualizada correctamente.", "success")
    else:
        flash("Error al actualizar la venta.", "danger")
    return redirect(url_for('ventas.listado_ventas'))
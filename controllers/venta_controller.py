from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask import jsonify
from models.ventas import Ventas
from models.user import Usuario
from models.vehiculo import Vehiculo
from utils.decorators import login_required

ventas_bp = Blueprint('ventas', __name__)

# --- RUTA 1: PARA VER EL FORMULARIO ---
@ventas_bp.route('/ventas/registrar_venta', methods=['GET'])
@login_required
def vista_registro():
    bancos = Ventas.obtener_bancos()
    metodos_pago = Ventas.obtener_metodos_pago()
    monedas = Ventas.obtener_monedas()
    monedas_digitales = Ventas.obtener_moneda_digital()

    return render_template('ventas/registrar_venta.html', bancos=bancos, metodos_pago=metodos_pago, monedas=monedas, monedas_digitales=monedas_digitales)

@ventas_bp.route('/ventas/api/cliente/<int:cedula>', methods=['GET'])
@login_required
def api_buscar_cliente(cedula):
    cliente = Usuario.buscar_cliente_por_cedula(cedula)
    
    if cliente:
        return jsonify({
            'exito': True,
            'nombre_completo': f"{cliente['nombre']} {cliente['apellido']}",
            'cedula': cliente['cedula_usuario'],
            'telefono': cliente['telefono'],
            'direccion': cliente['direccion'],
            'correo': cliente['correo']
        })
    else:
        return jsonify({
            'exito': False, 
            'mensaje': 'Cliente no encontrado o no tiene rol de cliente'
        }), 404
    
@ventas_bp.route('/ventas/api/vehiculo/<string:placa>', methods=['GET'])
@login_required
def api_buscar_vehiculo(placa):
    vehiculo = Vehiculo.buscar_por_placa(placa)
    
    if vehiculo:
        return jsonify({
            'exito': True,
            'vehiculo': {
                'placa': vehiculo['placa'],
                'marca': vehiculo['marca'],
                'modelo': vehiculo['modelo'],
                'tipo': vehiculo['tipo'],
                'anio': vehiculo['anio'],
                'color': vehiculo['color'],
                'precio': float(vehiculo['precio']),
                'estado': vehiculo['estado']
            }
        })
    else:
        return jsonify({
            'exito': False,
            'mensaje': 'Vehículo no encontrado o no disponible para la venta'
        }), 404
    

# --- RUTA 2: PARA PROCESAR EL GUARDADO ---
@ventas_bp.route('/ventas/registrar_venta', methods=['POST'])
@login_required
def registrar_venta():
    # Recibimos los datos en formato JSON desde el fetch
    data = request.get_json()
    
    if not data:
        return jsonify({"exito": False, "mensaje": "No se recibieron datos"})

    # Creamos la instancia del modelo pasando el diccionario completo
    nueva_venta = Ventas(data)

    # Ejecutamos el método registrar que contiene la transacción
    resultado = nueva_venta.registrar()

    if resultado["status"]:
        return jsonify({"exito": True, "mensaje": "Venta y pagos registrados exitosamente"})
    else:
        return jsonify({"exito": False, "mensaje": resultado["error"]})
    
@ventas_bp.route('/ventas/lista_ventas')
@login_required
def listado_ventas():
    # Obtenemos los datos desde el modelo
    ventas = Ventas.obtener_todas()
    return render_template('ventas/lista_ventas.html', ventas=ventas)
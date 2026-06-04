from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask import jsonify
from models.ventas import Ventas
from models.user import Usuario
from utils.decorators import login_required

ventas_bp = Blueprint('ventas', __name__)

# --- RUTA 1: PARA VER EL FORMULARIO ---
@ventas_bp.route('/ventas/registrar_venta', methods=['GET'])
@login_required
def vista_registro():
    # Aquí es donde le dices a Flask que muestre tu HTML
    # Asegúrate de que la ruta del archivo sea correcta según tu carpeta templates
    return render_template('ventas/registrar_venta.html')

@ventas_bp.route('/nueva_venta')
def nueva_venta():
    lista_vehiculos = Ventas.obtener_vehiculos_disponibles()
    return render_template('ventas/registrar_venta.html', vehiculos=lista_vehiculos)


@ventas_bp.route('/ventas/api/cliente/<int:cedula>', methods=['GET'])
@login_required
def api_buscar_cliente(cedula):
    cliente = Usuario.buscar_cliente_por_cedula(cedula)
    
    if cliente:
        # Retornamos los datos en formato JSON
        return jsonify({
            'exito': True,
            'nombre_completo': f"{cliente['nombre']} {cliente['apellido']}",
            'cedula': cliente['cedula_usuario']
        })
    else:
        return jsonify({
            'exito': False, 
            'mensaje': 'Cliente no encontrado o no tiene rol de cliente'
        }), 404

# --- RUTA 2: PARA PROCESAR EL GUARDADO ---
@ventas_bp.route('/ventas/registrar_venta', methods=['POST'])
@login_required
def registrar_venta():
    # 1. Capturamos datos del formulario
    cedula_cliente = request.form.get('id_cliente_hidden')
    placa = request.form.get('id_vehiculo')
    tipo_operacion = request.form.get('tipo_operacion')
    
    poder = True if request.form.get('tiene_poder') else False
    traspaso = True if request.form.get('traspaso_listo') else False
    
    monto_recibido = request.form.get('monto_recibido', 0)
    fecha_vencimiento = request.form.get('fecha_vencimiento') if tipo_operacion == 'credito' else None

    # 2. Validaciones básicas
    if not cedula_cliente or not placa:
        flash("Error: Debe seleccionar un cliente y un vehículo", "ventas")
        return redirect(url_for('ventas.vista_registro'))

    # 3. Crear instancia del modelo y guardar
    nueva_venta = Ventas(
        cedula_cliente, 
        placa, 
        tipo_operacion, 
        poder, 
        traspaso, 
        monto_recibido, 
        fecha_vencimiento
    )

    if nueva_venta.registrar():
        flash("¡Venta registrada exitosamente!", "ventas")
        return redirect(url_for('ventas.vista_registro'))
    else:
        flash("Hubo un error crítico en la base de datos.", "ventas")
        return redirect(url_for('ventas.vista_registro'))
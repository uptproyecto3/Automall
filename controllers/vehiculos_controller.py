import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.vehiculo import Vehiculo
from models.marca import Marca        # Importar tus otros modelos
from models.modelo import Modelo      # Importar tus otros modelos
from models.proveedor import Proveedor # Importar tus otros modelos
from werkzeug.utils import secure_filename
from utils.permisos import requiere_permiso

vehiculos_bp = Blueprint('vehiculos', __name__)

@vehiculos_bp.route('/vehiculos/registro', methods=['GET', 'POST'])
@requiere_permiso('Vehiculos', 'p_crear')
def registro():
    if request.method == 'POST':
        # 1. Manejo de la Imagen
        file = request.files['imagen']
        filename = secure_filename(file.filename)
        upload_path = os.path.join('static/uploads')
        if not os.path.exists(upload_path): os.makedirs(upload_path)
        file.save(os.path.join(upload_path, filename))
        
        # 2. Recolectar datos de DOCUMENTACIÓN
        doc_fields = [
            'original_totalPropiedad', 'experticia_transito', 'certificado_origen',
            'carnet_circulacion', 'reserva_dominio', 'garantia_vehiculo',
            'certificado_garantia', 'manual_vehiculoGarantia', 'finiquito',
            'resguardo', 'seguro', 'factura_compra'
        ]
        d_data = {field: (1 if request.form.get(field) else 0) for field in doc_fields}
        d_data['fecha_ingreso'] = request.form.get('fecha_ingreso')
        d_data['otro_documento'] = request.form.get('otro_documento')

        # 3. Recolectar datos del VEHÍCULO
        v_data = {
            'placa': request.form['placa'],
            'color': request.form['color'],
            'anio': request.form['anio'],
            'kilometraje': request.form['kilometraje'],
            'tipo': request.form['tipo'],
            'marca': request.form['marca'],   # Este será el ID del select
            'modelo': request.form['modelo'], # Este será el ID del select
            'cedula': request.form['cedula']  # Este será el ID del select
        }
        
        if Vehiculo.guardar_con_documentos(v_data, d_data, filename):
            flash("¡Vehículo registrado con éxito!")
            return redirect(url_for('vehiculos.lista'))
        else:
            flash("Error al registrar el vehículo.")

    # --- PARTE GET: Cargar datos para los Selects ---
    marcas = Marca.obtener_todas()
    modelos = Modelo.obtener_todas()
    proveedores = Proveedor.obtener_todos()
    
    return render_template('vehiculos/registro.html', 
                           marcas=marcas, 
                           modelos=modelos, 
                           proveedores=proveedores)

@vehiculos_bp.route('/lista')
@requiere_permiso('Usuarios', 'p_leer')
def lista():
    vehiculos = Vehiculo.obtener_todos()
    return render_template('vehiculos/lista.html', vehiculos=vehiculos)
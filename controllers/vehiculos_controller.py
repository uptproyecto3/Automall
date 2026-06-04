import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.vehiculo import Vehiculo
from models.marca import Marca        
from models.modelo import Modelo      
from models.proveedor import Proveedor 
from werkzeug.utils import secure_filename
from utils.permisos import requiere_permiso

vehiculos_bp = Blueprint('vehiculos', __name__)

@vehiculos_bp.route('/vehiculos/registro', methods=['GET', 'POST'])
@requiere_permiso('Vehiculos', 'p_crear')
def registro():
    if request.method == 'POST':
        try:
            # Manejo de Imagen
            file = request.files['imagen']
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static/uploads')
            if not os.path.exists(upload_path): os.makedirs(upload_path)
            file.save(os.path.join(upload_path, filename))
            
            # Recolectar Documentación
            doc_fields = [
                'original_totalPropiedad', 'experticia_transito', 'certificado_origen',
                'carnet_circulacion', 'reserva_dominio', 'garantia_vehiculo',
                'certificado_garantia', 'manual_vehiculoGarantia', 'finiquito',
                'resguardo', 'seguro', 'factura_compra'
            ]
            d_data = {field: (1 if request.form.get(field) else 0) for field in doc_fields}
            d_data['fecha_ingreso'] = request.form.get('fecha_ingreso')
            d_data['otro_documento'] = request.form.get('otro_documento')

            # Recolectar Datos Vehículo
            v_data = {
                'placa': request.form['placa'],
                'color': request.form['color'],
                'anio': request.form['anio'],
                'kilometraje': request.form['kilometraje'],
                'tipo': request.form['tipo'],
                'estado': request.form['estado'],
                'marca': request.form['marca'],
                'modelo': request.form['modelo'],
                'cedula': request.form['cedula']
            }
            
            if Vehiculo.guardar_con_documentos(v_data, d_data, filename):
                flash("¡Vehículo registrado con éxito!", "success")
                return redirect(url_for('vehiculos.lista'))
            else:
                flash("Error al registrar en la base de datos. Revisa la consola.", "danger")
        except Exception as e:
            print(f"Error en controlador: {e}")
            flash("Error de sistema al procesar el formulario.", "danger")

    marcas = Marca.obtener_todas()
    modelos = Modelo.obtener_todas()
    proveedores = Proveedor.obtener_todos()
    return render_template('vehiculos/registro.html', marcas=marcas, modelos=modelos, proveedores=proveedores)

@vehiculos_bp.route('/vehiculos/lista')
@requiere_permiso('Vehiculos', 'p_leer')
def lista():
    vehiculos = Vehiculo.obtener_todos()
    return render_template('vehiculos/lista.html', vehiculos=vehiculos)
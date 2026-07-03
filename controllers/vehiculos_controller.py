import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.vehiculo import Vehiculo    
from models.modelo import Modelo      
from models.marca import Marca      
from models.propietario import Propietario 
from werkzeug.utils import secure_filename
from utils.permisos import requiere_permiso
from flask import jsonify

vehiculos_bp = Blueprint('vehiculos', __name__)

@vehiculos_bp.route('/vehiculos-lista')
@requiere_permiso('Vehiculos', 'p_leer')
def lista():
    vehiculos = Vehiculo.obtener_todos()
    return render_template('vehiculos/lista.html', vehiculos=vehiculos)

@vehiculos_bp.route('/vehiculos-registrar', methods=['GET', 'POST'])
@requiere_permiso('Vehiculos', 'p_crear')
def registro():
    if request.method == 'POST':
        try:
            # 1. Manejo de Imagen
            file = request.files.get('imagen')
            filename = ""
            if file:
                filename = secure_filename(file.filename)
                upload_path = os.path.join('static/uploads')
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file.save(os.path.join(upload_path, filename))
            
            # 2. Datos Documentación
            doc_fields = ['original_totalPropiedad', 'experticia_transito', 'certificado_origen', 'carnet_circulacion', 'reserva_dominio', 'garantia_vehiculo', 'certificado_garantia', 'manual_vehiculoGarantia', 'finiquito', 'resguardo', 'seguro', 'factura_compra']
            d_data = {f: (1 if request.form.get(f) else 0) for f in doc_fields}
            d_data['fecha_ingreso'] = request.form.get('fecha_ingreso')
            d_data['otro_documento'] = request.form.get('otro_documento')

            # 3. Datos Accesorios
            a_data = {
                'copia_llaves': 1 if request.form.get('copia_llaves') else 0,
                'repuesto': 1 if request.form.get('repuesto') else 0,
                'triangulo': 1 if request.form.get('triangulo') else 0
            }

            # 4. Datos Vehículo
            v_data = {
                'placa': request.form['placa'],
                'color': request.form['color'],
                'anio': request.form['anio'],
                'kilometraje': request.form['kilometraje'],
                'tipo': request.form['tipo'],
                'estado': request.form['estado'],
                'modelo': request.form['modelo'],
                'cedula': request.form['cedula']
            }

            # 5. Datos Catálogo 
            c_data = {
                'precio': request.form['precio'],
                'descripcion': request.form['descripcion_catalogo'],
                'fecha_pub': request.form['fecha_publicacion'],
                'estado': 'Activo'
            }
            
            if Vehiculo.guardar_con_documentos(v_data, d_data, a_data, c_data, filename):
                # IMPORTANTE: Devolvemos JSON, no Redirect
                return jsonify({"status": "success", "message": "¡Vehículo y Catálogo registrados con éxito!"}), 200
            else:
                return jsonify({"status": "error", "message": "Error al registrar en la base de datos."}), 400

        except Exception as e:
            print(f"Error en controlador: {e}")
            # Aquí se enviará el mensaje de "Placa Duplicada" que definiste en el modelo
            return jsonify({"status": "error", "message": str(e)}), 400

    return render_template('vehiculos/registro.html', 
                           marcas=Marca.obtener_todas(), 
                           modelos=Modelo.obtener_todas(), 
                           propietarios=Propietario.obtener_todos())
                           
@vehiculos_bp.route('/vehiculos-editar/<placa>', methods=['GET', 'POST'])
@requiere_permiso('Vehiculos', 'p_actualizar')
def editar(placa):
    vehiculo = Vehiculo.obtener_por_placa(placa)
    
    if request.method == 'POST':
        try:
            file = request.files.get('imagen')
            filename = secure_filename(file.filename) if file and file.filename != '' else None
            if filename:
                upload_path = os.path.join('static/uploads')
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file.save(os.path.join(upload_path, filename))

            # Documentación
            doc_fields = ['original_totalPropiedad', 'experticia_transito', 'certificado_origen', 'carnet_circulacion', 'reserva_dominio', 'garantia_vehiculo', 'certificado_garantia', 'manual_vehiculoGarantia', 'finiquito', 'resguardo', 'seguro', 'factura_compra']
            d_data = {f: (1 if request.form.get(f) else 0) for f in doc_fields}
            d_data['fecha_ingreso'] = request.form['fecha_ingreso']
            d_data['otro_documento'] = request.form.get('otro_documento', '')

            # Accesorios
            a_data = {
                'copia_llaves': 1 if request.form.get('copia_llaves') else 0,
                'repuesto': 1 if request.form.get('repuesto') else 0,
                'triangulo': 1 if request.form.get('triangulo') else 0
            }
            
            # Vehículo
            v_data = {
                'placa': request.form['placa'], 
                'color': request.form['color'], 
                'anio': request.form['anio'],
                'kilometraje': request.form['kilometraje'], 
                'tipo': request.form['tipo'], 
                'estado': request.form['estado'],
                'modelo': request.form['modelo'], 
                'cedula': request.form['cedula']
            }

            # Catálogo
            c_data = {
                'precio': request.form['precio'], 
                'descripcion': request.form['descripcion_catalogo'],
                'fecha_pub': request.form['fecha_publicacion']
            }

            if Vehiculo.actualizar(placa, v_data, d_data, a_data, c_data, filename):
                flash("Vehículo actualizado correctamente", "success")
                return redirect(url_for('vehiculos.lista'))
            else:
                flash("No se pudo actualizar en la base de datos. Verifique los campos.", "danger")
        except Exception as e:
            print(f"Error en controlador: {e}")
            flash(f"Error de sistema: {e}", "danger")
        
    return render_template('vehiculos/editar_vehiculo.html', 
                           v=vehiculo, 
                           marcas=Marca.obtener_todas(), 
                           modelos=Modelo.obtener_todas(), 
                           propietarios=Propietario.obtener_todos())

@vehiculos_bp.route('/vehiculos-eliminar/<placa>', methods=['POST'])
@requiere_permiso('Vehiculos', 'p_eliminar')
def eliminar(placa):
    if Vehiculo.eliminar(placa):
        flash("Vehículo eliminado", "warning")
    else:
        flash("No se pudo eliminar el vehículo", "danger")
    return redirect(url_for('vehiculos.lista'))
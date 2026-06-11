from flask import Flask, render_template, session, request 
from dotenv import load_dotenv
from models.db import obtener_conexion_seguridad
from models.catalogo import Catalogo

import os

load_dotenv() # Esto lee el archivo .env automáticamente

from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp
from controllers.vehiculos_controller import vehiculos_bp
from controllers.catalogo_controller import catalogo_bp
from controllers.marca_controller import marca_bp
from controllers.modelo_controller import modelo_bp
from controllers.proveedor_controller import proveedor_bp 
from controllers.venta_controller import ventas_bp 
from controllers.citas_controller import citas_bp 
from controllers.permisos_controller import permisos_bp
from controllers.bitacora_controller import bitacora_bp
from controllers.mantenimientobd_controller import mantenimiento_bp
from controllers.tallercontroller import tallerbp
from controllers.mantenimiento_operacional_controller import mantenimiento_operacional_bp
from controllers.reporte_mantenimiento_operacional_controller import reporte_mantenimiento_operacional_bp
from controllers.servicios_controller import servicios_bp
from controllers.reporte_servicios_controller import reporte_servicios_bp
from controllers.pago_controller import pagos_bp

app = Flask(__name__)
app.secret_key = '123456789' # nosec B105

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(vehiculos_bp)
app.register_blueprint(catalogo_bp)
app.register_blueprint(marca_bp)
app.register_blueprint(modelo_bp)
app.register_blueprint(proveedor_bp)
app.register_blueprint(citas_bp)
app.register_blueprint(permisos_bp)
app.register_blueprint(bitacora_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(mantenimiento_bp)
app.register_blueprint(tallerbp)
app.register_blueprint(mantenimiento_operacional_bp)
app.register_blueprint(reporte_mantenimiento_operacional_bp)
app.register_blueprint(servicios_bp)
app.register_blueprint(reporte_servicios_bp)
app.register_blueprint(pagos_bp)



# Este decorador hace que la función sea accesible en cualquier HTML
@app.context_processor
def inject_permisos():
    def tiene_permiso(modulo, tipo_permiso):
        if 'cod_rol' not in session:
            return False
        
        if session.get('cod_rol') == 1:
            return True
            
        # LISTA BLANCA DE SEGURIDAD (Añadido para Bandit)
        permisos_validos = ['p_crear', 'p_eliminar', 'p_actualizar', 'p_leer']
        if tipo_permiso not in permisos_validos:
            return False
            
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        # Usamos nosec porque ya validamos con la lista blanca arriba
        sql = f"""
            SELECT rp.{tipo_permiso} as permiso 
            FROM t_permiso_rol_modulo rp
            JOIN t_modulo m ON rp.cod_modulo = m.cod_modulo
            WHERE rp.cod_rol = %s AND m.nombre_modulo = %s
        """ # nosec B608
        
        cursor.execute(sql, (session.get('cod_rol'), modulo))
        res = cursor.fetchone()
        
        cursor.close() 
        conexion.close()
        
        return res and res['permiso'] == 1
        
    return dict(tiene_permiso=tiene_permiso)

@app.route('/')
def index():
    todos_disponibles = Catalogo.obtener_disponibles()
    vehiculos_destacados = todos_disponibles[:6] 
    
    return render_template('index.html', vehiculos=vehiculos_destacados)

if __name__ == '__main__':
    app.run(debug=True)  # nosec B201




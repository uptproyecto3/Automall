from flask import Flask, render_template, session
from dotenv import load_dotenv
from models.db import obtener_conexion_seguridad

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

from controllers.marca_controller import marca_bp
from controllers.modelo_controller import modelo_bp
from controllers.proveedor_controller import proveedor_bp  
from controllers.permisos_controller import permisos_bp
from controllers.bitacora_controller import bitacora_bp
from controllers.mantenimientobd_controller import mantenimiento_bp
from controllers.venta_controller import ventas_bp


app = Flask(__name__)
app.secret_key = '123456789' # Necesario para las sesiones

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(vehiculos_bp)
app.register_blueprint(catalogo_bp, url_prefix='/vehiculos')
app.register_blueprint(marca_bp)
app.register_blueprint(modelo_bp)
app.register_blueprint(proveedor_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(citas_bp)

app.register_blueprint(marca_bp)
app.register_blueprint(modelo_bp)
app.register_blueprint(proveedor_bp)
app.register_blueprint(permisos_bp)
app.register_blueprint(bitacora_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(mantenimiento_bp)


# Este decorador hace que la función sea accesible en cualquier HTML
@app.context_processor
def inject_permisos():
    def tiene_permiso(modulo, tipo_permiso):
        if 'cod_rol' not in session:
            return False
        
        # Super Usuario (ID 1) siempre tiene todo
        if session.get('cod_rol') == 1:
            return True
            
        # Si por error el HTML envía un permiso vacío, evitamos el choque de SQL
        if not tipo_permiso or tipo_permiso.strip() == "":
            return False
            
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        sql = f"""
            SELECT rp.{tipo_permiso} as permiso 
            FROM t_permiso_rol_modulo rp
            JOIN t_modulo m ON rp.cod_modulo = m.cod_modulo
            WHERE rp.cod_rol = %s AND m.nombre_modulo = %s
        """
        
        cursor.execute(sql, (session.get('cod_rol'), modulo))
        res = cursor.fetchone()
        
        cursor.close()  # Cerramos el cursor
        conexion.close()
        
        return res and res['permiso'] == 1
        
    return dict(tiene_permiso=tiene_permiso)

# Ruta principal (Landing page)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # debug=True permite que el servidor se recargue solo al guardar cambios
    app.run(debug=True)




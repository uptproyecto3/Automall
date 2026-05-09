from flask import Flask, render_template, session
from models.db import obtener_conexion

from controllers.auth_controller import auth_bp
from controllers.vehiculos_controller import vehiculos_bp
from controllers.permisos_controller import permisos_bp

app = Flask(__name__)
app.secret_key = '123456789' # Necesario para las sesiones

app.register_blueprint(auth_bp)
app.register_blueprint(vehiculos_bp)
app.register_blueprint(permisos_bp)

# Este decorador hace que la función sea accesible en cualquier HTML
@app.context_processor
def inject_permisos():
    def tiene_permiso(modulo, tipo_permiso):
        # Si no hay sesión, no tiene permisos
        if 'id_rol' not in session:
            return False
        
        # Super Usuario (ID 1) siempre tiene todo
        if session.get('id_rol') == 1:
            return True
            
        # Consultar BD para verificar permiso
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = f"""SELECT {tipo_permiso} as permiso 
                  FROM rol_permisos rp
                  JOIN modulo m ON rp.id_modulo = m.id_modulo
                  WHERE rp.id_rol = %s AND m.nombre_modulo = %s"""
        cursor.execute(sql, (session.get('id_rol'), modulo))
        res = cursor.fetchone()
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




from functools import wraps
from flask import session, flash, redirect, url_for
from models.db import obtener_conexion_seguridad

# Decorador para permisos específicos (Ej: eliminar, crear)
def requiere_permiso(modulo, tipo_permiso):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            id_rol = session.get('id_rol')
            if not id_rol: return redirect(url_for('auth.login'))
            
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor(dictionary=True)
            # Consultamos si el rol tiene permiso en el módulo dado
            sql = """SELECT rp.{} as tiene_permiso 
                     FROM t_permiso_rol_modulo rp 
                     JOIN t_modulo m ON rp.id_modulo = m.id_modulo 
                     WHERE rp.id_rol = %s AND m.nombre_modulo = %s""".format(tipo_permiso)
            cursor.execute(sql, (id_rol, modulo))
            res = cursor.fetchone()
            conexion.close()
            
            if res and res['tiene_permiso'] == 1:
                return f(*args, **kwargs)
            else:
                flash("Acceso denegado: No tienes permisos para esta acción.")
                return redirect(url_for('index'))
        return wrapper
    return decorador

# Decorador específico para Super Usuario (ID 1)
def requiere_superusuario(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Asumiendo que el ID del 'Super Usuario' en tu BD es 1
        if session.get('id_rol') == 1:
            return f(*args, **kwargs)
        else:
            flash("Acceso restringido solo para Super Usuarios.")
            return redirect(url_for('index'))
    return wrapper
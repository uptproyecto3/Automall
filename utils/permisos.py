from functools import wraps
from flask import session, flash, redirect, url_for
from models.db import obtener_conexion_seguridad

# Decorador para permisos específicos (Ej: eliminar, crear)
def requiere_permiso(modulo, tipo_permiso):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cod_rol = session.get('cod_rol')
            if not cod_rol: 
                return redirect(url_for('auth.login'))
            
            # --- MEJORA DE SEGURIDAD PARA BANDIT ---
            # Definimos qué columnas son permitidas en la base de datos
            permisos_validos = ['p_crear', 'p_eliminar', 'p_actualizar', 'p_leer'] # Ajusta según tus nombres reales de columnas
            
            if tipo_permiso not in permisos_validos:
                flash("Error de seguridad: Permiso no reconocido.")
                return redirect(url_for('index'))
            # ---------------------------------------

            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor(dictionary=True)
            
            # Al usar la lista blanca arriba, este f-string ya es seguro.
            # Usamos # nosec para que Bandit sepa que lo hemos revisado manualmente.
            sql = f"""
                SELECT rp.{tipo_permiso} as tiene_permiso 
                FROM t_permiso_rol_modulo rp 
                JOIN t_modulo m ON rp.cod_modulo = m.cod_modulo 
                WHERE rp.cod_rol = %s AND m.nombre_modulo = %s
            """ # nosec B608
            
            cursor.execute(sql, (cod_rol, modulo))
            res = cursor.fetchone()
            
            cursor.close()
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
        if session.get('cod_rol') == 1:
            return f(*args, **kwargs)
        else:
            flash("Acceso restringido solo para Super Usuarios.")
            return redirect(url_for('index'))
    return wrapper
from functools import wraps
from flask import session, flash, redirect, url_for
from models.permiso import Permiso 

# Decorador para permisos específicos de funciones (CRUD)
def requiere_permiso(modulo, tipo_permiso):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cod_rol = session.get('cod_rol')
            if not cod_rol: 
                return redirect(url_for('auth.login'))
            
            # Lista blanca preventiva en el middleware
            permisos_validos = ['p_crear', 'p_eliminar', 'p_actualizar', 'p_leer']
            if tipo_permiso not in permisos_validos:
                flash("Error de seguridad: Acción o permiso no reconocido.")
                return redirect(url_for('index'))

            # Invocamos la verificación relacional
            tiene_acceso = Permiso.verificar_acceso(cod_rol, modulo, tipo_permiso)
            
            if tiene_acceso:
                return f(*args, **kwargs)
            else:
                flash("Acceso denegado: No tienes permisos para esta acción.")
                return redirect(url_for('index'))
        return wrapper
    return decorador


# Decorador exclusivo para Super Usuario
def requiere_superusuario(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('cod_rol') == 1:
            return f(*args, **kwargs)
        else:
            flash("Acceso restringido solo para Super Usuarios.")
            return redirect(url_for('index'))
    return wrapper
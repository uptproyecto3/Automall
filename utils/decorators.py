from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_nombre' not in session:
            flash("Debes iniciar sesión para ver esta página.")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
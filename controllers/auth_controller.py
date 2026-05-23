from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
from models.auth import Auth 
from models.bitacora import Bitacora
from utils.validaciones import ValidadorAuth

auth_bp = Blueprint('auth', __name__) 

# --- RUTAS DE AUTENTICACIÓN ---

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        password = request.form['password']
        usuario = Auth.verificar_credenciales(correo, password)
        
        if usuario:
            # Aquí es donde ocurre la magia
            session['cedula_usuario'] = usuario['cedula_usuario']
            session['usuario_nombre'] = usuario['nombre']
            session['cod_rol'] = usuario['cod_rol']  # <--- ESTO ES LO QUE FALTABA
            
            flash(f"Bienvenido, {usuario['nombre']}")
            return redirect(url_for('index'))
        else:
            flash("Correo o contraseña incorrectos.")
            
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        correo = request.form['email']
        # Buscamos si el usuario tiene pregunta registrada
        datos = Auth.obtener_pregunta(correo)
        
        if datos and datos['pregunta_seguridad']:
            # Guardamos el correo en sesión temporalmente para el siguiente paso
            session['recuperar_correo'] = correo
            return render_template('auth/verificar_pregunta.html', pregunta=datos['pregunta_seguridad'])
        else:
            flash("El correo no existe o no tiene preguntas de seguridad configuradas.")
            
    return render_template('auth/olvido_password.html')

@auth_bp.route('/verificar_respuesta', methods=['POST'])
def verificar_respuesta():
    correo = session.get('recuperar_correo')
    respuesta = request.form['respuesta']
    
    if Auth.validar_respuesta(correo, respuesta):
        # Si es correcto, permitimos ir a la vista de nueva contraseña
        return render_template('auth/cambiar_password.html')
    else:
        flash("Respuesta de seguridad incorrecta.")
        # Si falla, lo mandamos al inicio del proceso por seguridad
        return redirect(url_for('auth.recuperar'))

@auth_bp.route('/cambiar_password', methods=['POST'])
def cambiar_password():
    correo = session.get('recuperar_correo')
    nueva_pass = request.form['nueva_password']
    
    if correo and nueva_pass:
        Auth.actualizar_password(correo, nueva_pass)
        session.pop('recuperar_correo', None) # Limpiamos la sesión
        flash("Contraseña actualizada con éxito. Ya puedes iniciar sesión.")
        return redirect(url_for('auth.login'))
    
    return redirect(url_for('auth.login'))
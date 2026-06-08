from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.auth import Auth 

auth_bp = Blueprint('auth', __name__) 

# --- RUTAS DE AUTENTICACIÓN ---

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('email')
        password = request.form.get('password')
        
        # El modelo devuelve un dict con 'error' si la validación falla
        usuario = Auth.verificar_credenciales(correo, password)
        
        # 1. Validar si el modelo devolvió un error de validación (de utils)
        if isinstance(usuario, dict) and 'error' in usuario:
            flash(usuario['error'], "warning")
            return render_template('auth/login.html')

        # 2. Si las credenciales son correctas (devolvió los datos del usuario)
        if usuario:
            session['cedula_usuario'] = usuario['cedula_usuario']
            session['usuario_nombre'] = usuario['nombre']
            session['cod_rol'] = usuario['cod_rol']
            
            flash(f"Bienvenido, {usuario['nombre']}", "success")
            return redirect(url_for('index'))
        else:
            # 3. Si no hay usuario y no hubo error de formato, las credenciales no existen
            flash("Correo o contraseña incorrectos.", "danger")
            
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        correo = request.form.get('email')
        
        # Buscamos si el usuario tiene pregunta registrada
        datos = Auth.obtener_pregunta(correo)
        
        # Validar error de formato de correo devuelto por el modelo
        if isinstance(datos, dict) and 'error' in datos:
            flash(datos['error'], "warning")
            return render_template('auth/olvido_password.html')
        
        if datos and datos.get('pregunta_seguridad'):
            session['recuperar_correo'] = correo
            return render_template('auth/verificar_pregunta.html', pregunta=datos['pregunta_seguridad'])
        else:
            flash("El correo no existe o no tiene una pregunta de seguridad configurada.", "warning")
            
    return render_template('auth/olvido_password.html')

@auth_bp.route('/verificar_respuesta', methods=['POST'])
def verificar_respuesta():
    correo = session.get('recuperar_correo')
    respuesta = request.form.get('respuesta')
    
    if not correo:
        flash("Sesión de recuperación expirada.", "danger")
        return redirect(url_for('auth.recuperar'))

    # El modelo valida si la respuesta es vacía o si el formato del correo es inválido
    usuario = Auth.validar_respuesta(correo, respuesta)
    
    if usuario:
        # Si devuelve el usuario, la respuesta es correcta
        return render_template('auth/cambiar_password.html')
    else:
        flash("La respuesta de seguridad es incorrecta o no puede estar vacía.", "danger")
        return redirect(url_for('auth.recuperar'))

@auth_bp.route('/cambiar_password', methods=['POST'])
def cambiar_password():
    correo = session.get('recuperar_correo')
    nueva_pass = request.form.get('nueva_password')
    confirmar_pass = request.form.get('confirmar_password')
    
    if not correo:
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('auth.login'))

    # 1. Validación básica de coincidencia en el controlador
    if nueva_pass != confirmar_pass:
        flash("Las contraseñas no coinciden.", "warning")
        return render_template('auth/cambiar_password.html')

    # 2. Llamamos al modelo para validar la fuerza de la contraseña y actualizar
    resultado = Auth.actualizar_password(correo, nueva_pass)
    
    if resultado['status']:
        session.pop('recuperar_correo', None) # Limpieza de sesión
        flash(resultado['mensaje'], "success")
        return redirect(url_for('auth.login'))
    else:
        # Aquí se mostrarán los errores de ValidacionUsuario (ej: "debe tener 8 caracteres")
        flash(resultado['mensaje'], "danger")
        return render_template('auth/cambiar_password.html')
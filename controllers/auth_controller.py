from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
from models.auth import Auth
from models.bitacora import Bitacora
from utils.validaciones import ValidadorAuth

auth_bp = Blueprint('auth', __name__) 

# --- RUTAS DE AUTENTICACIÓN ---

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # --- VERIFICACIÓN DE BLOQUEO (Primera línea de defensa) ---
    if 'bloqueo_hasta' in session:
        hora_desbloqueo = datetime.fromisoformat(session['bloqueo_hasta'])
        
        if datetime.now() < hora_desbloqueo:
            tiempo_restante = hora_desbloqueo - datetime.now()
            minutos_restantes = int(tiempo_restante.total_seconds() // 60)
            segundos_restantes = int(tiempo_restante.total_seconds() % 60)
            
            flash(f"Cuenta temporalmente bloqueada. Intenta de nuevo en {minutos_restantes}m {segundos_restantes}s.", "danger")
            return render_template('auth/login.html')
        else:
            session.pop('bloqueo_hasta', None)
            session.pop('login_intentos', None)

    if request.method == 'POST':
        errores, correo_limpio = ValidadorAuth.validar_login(
            request.form.get('email'), 
            request.form.get('password')
        )
        
        if errores:
            for error in errores:
                flash(error, "danger")
            return render_template('auth/login.html')

        # Verificar credenciales en la BD
        usuario = Auth.verificar_credenciales(correo_limpio, request.form.get('password'))
        
        if usuario:
            # LOGIN EXITOSO: Limpiamos rastros de intentos fallidos
            session.pop('login_intentos', None)
            session.pop('bloqueo_hasta', None)
            
            # Guardamos datos en sesión
            session['usuario_nombre'] = usuario['nombre']
            session['id_rol'] = usuario['id_rol']
            
            # NOTA: Si vuelve a dar KeyError aquí, revisa tu modelo Auth y verifica si 
            # en el SELECT de SQL la columna se llama 'cedula' o 'cedula_usuario'.
            # Usamos .get() con un fallback por seguridad para evitar que la app se caiga.
            cedula_real = usuario.get('cedula_usuario') or usuario.get('cedula')
            session['cedula_usuario'] = cedula_real

            Bitacora.registrar(session['cedula_usuario'], "Inició sesión en el sistema", "Autenticación")
            flash(f"Bienvenido, {usuario['nombre']}")
            return redirect(url_for('index'))
        
        else:
            # --- CONTROL DE INTENTOS FALLIDOS ---
            intentos = session.get('login_intentos', 0) + 1
            session['login_intentos'] = intentos
            
            if intentos >= 3:
                hora_bloqueo = datetime.now() + timedelta(minutes=5)
                session['bloqueo_hasta'] = hora_bloqueo.isoformat()
                
                # CORRECCIÓN INTEGRIDAD: Como no hay sesión activa, mandamos el correo 
                # del infractor o un indicador genérico a la bitácora en vez de session['cedula_usuario']
                #usuario_infractor = correo_limpio if correo_limpio else "Desconocido"
                #Bitacora.registrar(usuario_infractor, f"Intrusión detectada: Bloqueo de IP/Cuenta por 3 intentos fallidos", "Seguridad")
                
                flash("Has superado el límite de intentos. Formulario bloqueado por 5 minutos.", "danger")
            else:
                intentos_restantes = 3 - intentos
                flash(f"Correo o contraseña incorrectos. Te quedan {intentos_restantes} intentos.", "danger")
                
    return render_template('auth/login.html')

@auth_bp.route('/api/chequear-bloqueo')
def chequear_bloqueo():
    if 'bloqueo_hasta' in session:
        hora_desbloqueo = datetime.fromisoformat(session['bloqueo_hasta'])
        if datetime.now() < hora_desbloqueo:
            tiempo_restante = hora_desbloqueo - datetime.now()
            return {
                "bloqueado": True, 
                "segundos": int(tiempo_restante.total_seconds())
            }
        else:
            session.pop('bloqueo_hasta', None)
            session.pop('login_intentos', None)
            
    return {"bloqueado": False, "segundos": 0}


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
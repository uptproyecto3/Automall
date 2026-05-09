from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import Usuario
from utils.decorators import login_required
from utils.permisos import requiere_permiso

auth_bp = Blueprint('auth', __name__) 

# --- RUTAS DE AUTENTICACIÓN ---

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        password = request.form['password']
        usuario = Usuario.verificar_credenciales(correo, password)
        
        if usuario:
            # Aquí es donde ocurre la magia
            session['usuario_nombre'] = usuario['nombre']
            session['id_rol'] = usuario['id_rol']  # <--- ESTO ES LO QUE FALTABA
            
            flash(f"Bienvenido, {usuario['nombre']}")
            return redirect(url_for('index'))
        else:
            flash("Correo o contraseña incorrectos.")
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
    
        nuevo_usuario = Usuario(
            request.form['cedula'],
            request.form['nombre'],
            request.form['apellido'],
            request.form['telefono'],
            request.form['direccion'],
            request.form['email'],
            request.form['password']
        )
        nuevo_usuario.guardar()
        
        flash("¡Registro exitoso! Ya puedes iniciar sesión.")
        return redirect(url_for('auth.login'))
        
    return render_template('auth/registro.html')

# --- RUTAS DE GESTIÓN (CRUD) ---

@auth_bp.route('/usuarios')
@login_required
def listar():
    usuarios = Usuario.obtener_todos()
    return render_template('usuarios/index.html', usuarios=usuarios)

@auth_bp.route('/usuarios/eliminar/<int:id>')
@login_required
@requiere_permiso('Usuarios', 'p_eliminar') # <--- Si no tiene p_eliminar=1 en la BD, no entra
def eliminar(id):
    Usuario.eliminar(id)
    return redirect(url_for('auth.listar'))

@auth_bp.route('/usuarios/editar/<int:id>', methods=['POST'])
@login_required
@requiere_permiso('Usuarios', 'p_actualizar')
def editar(id):
    # Aquí procesamos los datos que vienen del modal
    Usuario.actualizar(
        id,
        request.form['cedula'],
        request.form['nombre'],
        request.form['apellido'],
        request.form['telefono'],
        request.form['direccion'],
        request.form['email']
    )
    flash("Usuario actualizado correctamente.")
    return redirect(url_for('auth.listar'))
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import Usuario
from utils.decorators import login_required
from utils.permisos import requiere_permiso
from models.bitacora import Bitacora

user_bp = Blueprint('user', __name__) 

# --- RUTAS DE USUARIOS ---

@user_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
    
        nuevo_usuario = Usuario(
            request.form['cedula_usuario'],
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
        
    return render_template('usuarios/registro.html')

# --- RUTAS DE GESTIÓN (CRUD) ---

@user_bp.route('/usuarios')
@login_required
@requiere_permiso('Usuarios', 'p_leer')
def listar():
    usuarios = Usuario.obtener_todos()
    return render_template('usuarios/index.html', usuarios=usuarios)

@user_bp.route('/usuarios/eliminar/<int:id>')
@login_required
@requiere_permiso('Usuarios', 'p_eliminar') # <--- Si no tiene p_eliminar=1 en la BD, no entra
def eliminar(id):
    Usuario.eliminar(id)
    Bitacora.registrar(session['cedula_usuario'], f"Eliminó el Usuario ID: {id}", "Usuarios")
    return redirect(url_for('user.listar'))

@user_bp.route('/usuarios/editar/<int:id>', methods=['POST'])
@login_required
@requiere_permiso('Usuarios', 'p_actualizar')
def editar(id):
    # Ya no extraemos ni enviamos la cédula para no alterar sus relaciones en cascada
    Usuario.actualizar(
        id,
        request.form['nombre'],
        request.form['apellido'],
        request.form['telefono'],
        request.form['direccion'],
        request.form['email']
    )
    
    flash("Usuario actualizado correctamente.")
    Bitacora.registrar(session['cedula_usuario'], f"Actualizo al Usuario ID: {id}", "Usuarios")
    return redirect(url_for('user.listar'))
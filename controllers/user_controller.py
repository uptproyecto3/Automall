import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import Usuario # El modelo se llama user.py
from utils.decorators import login_required
from utils.permisos import requiere_permiso
from models.bitacora import Bitacora 

user_bp = Blueprint('user', __name__) 

# --- RUTAS DE USUARIOS ---

@user_bp.route('/perfil')
@login_required
def perfil():
    cedula_usuario = session.get('cedula_usuario')
    usuario_info = Usuario.obtener_por_cedula(cedula_usuario)
    
    if not usuario_info:
        flash("No se pudo cargar la información del perfil.", "danger")
        return redirect(url_for('index'))
        
    return render_template('usuarios/perfil.html', usuario=usuario_info)

@user_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # 1. Recoger datos del formulario
        cedula = request.form.get('cedula')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        correo = request.form.get('email')
        password = request.form.get('password')
        
        # 2. Manejar la foto (Nombre temporal por si no suben nada)
        foto = request.files.get('foto_perfil')
        nombre_foto = "default.png"

        # 3. Creamos la instancia del usuario
        nuevo_usuario = Usuario(
            cedula, nombre, apellido, telefono, direccion, correo, password, nombre_foto
        )

        # 4. Intentamos guardar (El modelo ejecuta todas las validaciones de utils)
        resultado = nuevo_usuario.guardar()

        if resultado['status']:
            # Si el registro fue exitoso en la BD, procedemos a guardar la foto física
            if foto and foto.filename != '':
                extension = os.path.splitext(foto.filename)[1]
                nombre_foto = secure_filename(f"{cedula}{extension}")
                ruta_guardado = os.path.join('static', 'uploads', 'perfiles', nombre_foto)
                foto.save(ruta_guardado)
                
                # Opcional: Actualizar el nombre de la foto en la BD si cambió del default
                # (Aunque en el constructor ya se pasó el nombre, aquí podrías hacer un update rápido si fuera necesario)

            flash(resultado['mensaje'], "success")
            return redirect(url_for('auth.login'))
        else:
            # Si hubo error de validación (cédula repetida, clave débil, etc.)
            flash(resultado['mensaje'], "danger")
            return render_template('usuarios/registro.html')
        
    return render_template('usuarios/registro.html')

# --- RUTAS DE GESTIÓN (CRUD) ---

@user_bp.route('/usuarios')
@login_required
@requiere_permiso('Usuarios', 'p_leer')
def listar():
    usuarios = Usuario.obtener_todos()
    return render_template('usuarios/index.html', usuarios=usuarios)

@user_bp.route('/usuarios/eliminar/<int:cedula_usuario>')
@login_required
@requiere_permiso('Usuarios', 'p_eliminar')
def eliminar(cedula_usuario):
    exito = Usuario.eliminar(cedula_usuario)
    if exito:
        Bitacora.registrar(session['cedula_usuario'], f"Eliminó lógicamente al Usuario: {cedula_usuario}", "Usuarios")
        flash("Usuario eliminado correctamente.", "success")
    else:
        flash("Error al intentar eliminar el usuario.", "danger")
    return redirect(url_for('user.listar'))

@user_bp.route('/usuarios/editar/<int:cedula_usuario>', methods=['POST'])
@login_required
@requiere_permiso('Usuarios', 'p_actualizar')
def editar(cedula_usuario):
    # Llamamos al método actualizar que ahora devuelve un diccionario de estatus
    resultado = Usuario.actualizar(
        cedula_usuario,
        request.form.get('nombre'),
        request.form.get('apellido'),
        request.form.get('telefono'),
        request.form.get('direccion'),
        request.form.get('email')
    )
    
    if resultado['status']:
        flash(resultado['mensaje'], "success")
        #Este es el llamado a la bitacora
        Bitacora.registrar(session['cedula_usuario'], f"Actualizó al Usuario ID: {cedula_usuario}", "Usuarios") 
    else:
        # Aquí se mostrarán los errores de validación de formato o correo duplicado
        flash(resultado['mensaje'], "danger")
        
    return redirect(url_for('user.listar'))
import os
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from models.clientes import ClienteModel
from utils.decorators import login_required
from utils.validaciones import ValidacionUsuario

# Directorio donde se guardan las fotos de perfil
CARPETA_PERFILES = os.path.join('static', 'uploads', 'perfiles')

clientes_bp = Blueprint('clientes', __name__)


def _guardar_foto_perfil(archivo, cedula):
    """
    Guarda la foto de perfil en CARPETA_PERFILES con nombre único (cedula_timestamp.ext).
    Retorna la ruta relativa a /static/ para usar con url_for, o None si no hay archivo.
    """
    if not archivo or archivo.filename == '':
        return None

    extension = archivo.filename.rsplit('.', 1)[-1].lower()
    nombre_unico = f"{cedula}_{int(time.time())}.{extension}"
    nombre_seguro = secure_filename(nombre_unico)
    ruta_destino = os.path.join(CARPETA_PERFILES, nombre_seguro)

    os.makedirs(CARPETA_PERFILES, exist_ok=True)
    archivo.save(ruta_destino)
    return f"uploads/perfiles/{nombre_seguro}"


# ==========================================================================================
# LISTA DE CLIENTES (Solo Super Usuario)
# ==========================================================================================
@clientes_bp.route('/clientes')
@login_required
def listar_clientes():
    if session.get('cod_rol') != 1:
        flash("⛔ Acceso denegado: Solo el administrador puede gestionar clientes.", "danger")
        return redirect(url_for('index'))

    clientes = ClienteModel.obtener_clientes()
    return render_template('usuarios/clientes.html', clientes=clientes)


# ==========================================================================================
# REGISTRAR NUEVO CLIENTE (Público — accesible sin sesión)
# ==========================================================================================
@clientes_bp.route('/registrar_clientes', methods=['GET', 'POST'])
def registrar_clientes():
    if request.method == 'POST':
        cedula    = request.form.get('cedula', '').strip()
        nombre    = request.form.get('nombre', '').strip()
        apellido  = request.form.get('apellido', '').strip()
        telefono  = request.form.get('telefono', '').strip()
        direccion = request.form.get('direccion', '').strip()
        correo    = request.form.get('email', '').strip()
        password  = request.form.get('password', '')
        archivo_foto = request.files.get('foto_perfil')

        # Validar foto si se proporcionó
        err_foto = ValidacionUsuario.validar_foto_perfil(archivo_foto)
        if err_foto:
            flash(f"⚠️ {err_foto}", "danger")
            return render_template('usuarios/registrar_clientes.html', datos=request.form)

        # Guardar foto o usar imagen por defecto
        nombre_foto = _guardar_foto_perfil(archivo_foto, cedula) or "uploads/perfiles/default.png"

        nuevo_cliente = ClienteModel(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            correo=correo,
            password=password,
            foto=nombre_foto,
            cod_rol=4
        )

        resultado = nuevo_cliente.registrar_cliente_db()

        if resultado['status']:
            flash(f"✨ {resultado['mensaje']}", "success")
            # Admin regresa a la gestión; cliente público va al login
            if session.get('cod_rol') == 1:
                return redirect(url_for('clientes.listar_clientes'))
            return redirect(url_for('auth.login'))
        else:
            flash(f"⚠️ {resultado['mensaje']}", "danger")
            return render_template('usuarios/registrar_clientes.html', datos=request.form)

    return render_template('usuarios/registrar_clientes.html')


# ==========================================================================================
# EDITAR CLIENTE (Solo Super Usuario)
# ==========================================================================================
@clientes_bp.route('/clientes/editar/<cedula>', methods=['POST'])
@login_required
def editar_cliente(cedula):
    if session.get('cod_rol') != 1:
        flash("⛔ Acceso denegado.", "danger")
        return redirect(url_for('index'))

    datos_form = {
        'nombre':    request.form.get('nombre', '').strip(),
        'apellido':  request.form.get('apellido', '').strip(),
        'telefono':  request.form.get('telefono', '').strip(),
        'direccion': request.form.get('direccion', '').strip(),
        'correo':    request.form.get('correo', '').strip(),
    }

    # Validar campos editables
    es_valido, errores = ValidacionUsuario.validar_modificacion_cliente(datos_form)
    if not es_valido:
        for _, mensaje in errores.items():
            flash(f"⚠️ {mensaje}", "danger")
        return redirect(url_for('clientes.listar_clientes'))

    # Manejar foto nueva (opcional)
    archivo_foto = request.files.get('foto_perfil')
    err_foto = ValidacionUsuario.validar_foto_perfil(archivo_foto)
    if err_foto:
        flash(f"⚠️ {err_foto}", "danger")
        return redirect(url_for('clientes.listar_clientes'))

    nueva_foto = _guardar_foto_perfil(archivo_foto, cedula)
    if nueva_foto is None:
        # Conservar foto existente
        cliente_actual = ClienteModel.obtener_por_cedula(cedula)
        nueva_foto = cliente_actual['foto'] if cliente_actual else "uploads/perfiles/default.png"

    datos_form['cedula'] = cedula
    datos_form['foto'] = nueva_foto

    if ClienteModel.actualizar_cliente(datos_form):
        flash("✨ Datos del cliente actualizados con éxito.", "success")
    else:
        flash("⚠️ No se pudieron guardar los cambios.", "danger")

    return redirect(url_for('clientes.listar_clientes'))


# ==========================================================================================
# ELIMINAR CLIENTE (Solo Super Usuario)
# ==========================================================================================
@clientes_bp.route('/clientes/eliminar/<cedula>', methods=['POST'])
@login_required
def eliminar_cliente(cedula):
    if session.get('cod_rol') != 1:
        flash("⛔ Acceso denegado.", "danger")
        return redirect(url_for('index'))

    resultado = ClienteModel.eliminar_cliente(cedula)
    if resultado['status']:
        flash(resultado['mensaje'], "success")
    else:
        flash(f"⚠️ {resultado['mensaje']}", "danger")

    return redirect(url_for('clientes.listar_clientes'))
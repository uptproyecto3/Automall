from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.vendedor import Vendedor
from utils.decorators import login_required
from utils.permisos import requiere_permiso
from models.bitacora import Bitacora

vendedor_bp = Blueprint('vendedor', __name__, url_prefix='/vendedores')

@vendedor_bp.route('/')
@login_required
@requiere_permiso('Vendedor', 'p_leer')
def listar():
    vendedores = Vendedor.obtener_todos()
    return render_template('vendedor/index.html', vendedores=vendedores)

@vendedor_bp.route('/registrar', methods=['GET', 'POST'])
@login_required
@requiere_permiso('Vendedor', 'p_crear')
def registrar():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        correo = request.form.get('email')
        password = request.form.get('password')

        if not all([cedula, nombre, apellido, telefono, direccion, correo, password]):
            flash("Todos los campos son obligatorios", "danger")
            return render_template('vendedor/registrar.html')

        nuevo_vendedor = Vendedor(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            correo=correo,
            password=password
        )

        resultado = nuevo_vendedor.guardar()

        if resultado['status']:
            Bitacora.registrar(
                session['cedula_usuario'],
                f"Registró nuevo vendedor: {cedula} - {nombre} {apellido}",
                "Vendedores"
            )
            flash(resultado['mensaje'], "success")
            return redirect(url_for('vendedor.listar'))
        else:
            flash(resultado['mensaje'], "danger")

    return render_template('vendedor/registrar.html')

#Ver detalle del vendedor
@vendedor_bp.route('/ver/<cedula>')
@login_required
@requiere_permiso('Vendedor', 'p_leer')
def ver(cedula):
    vendedor = Vendedor.obtener_por_cedula(cedula)
    if not vendedor:
        flash("Vendedor no encontrado", "danger")
        return redirect(url_for('vendedor.listar'))
    return render_template('vendedor/detalle.html', vendedor=vendedor)

# Editar vendedor
@vendedor_bp.route('/editar/<cedula>', methods=['POST'])
@login_required
@requiere_permiso('Vendedor', 'p_actualizar')
def editar(cedula):
    resultado = Vendedor.actualizar(
        cedula,
        request.form.get('nombre'),
        request.form.get('apellido'),
        request.form.get('telefono'),
        request.form.get('direccion'),
        request.form.get('email')
    )

    if resultado['status']:
        Bitacora.registrar(
            session['cedula_usuario'],
            f"Actualizó vendedor: {cedula}",
            "Vendedores"
        )
        flash(resultado['mensaje'], "success")
    else:
        flash(resultado['mensaje'], "danger")

    return redirect(url_for('vendedor.listar'))

#Cambiar estado
@vendedor_bp.route('/cambiar_estado/<cedula>')
@login_required
@requiere_permiso('Vendedor', 'p_eliminar')
def cambiar_estado(cedula):
    vendedor = Vendedor.obtener_por_cedula(cedula)
    if vendedor:
        nuevo_estado = 0 if vendedor.get('estado') == 1 else 1
        Vendedor.cambiar_estado(cedula, nuevo_estado)
        estado_texto = "activado" if nuevo_estado == 1 else "desactivado"
        Bitacora.registrar(
            session['cedula_usuario'],
            f"{estado_texto.capitalize()} al vendedor: {cedula}",
            "Vendedores"
        )
        flash(f"Vendedor {estado_texto} correctamente", "success")
    return redirect(url_for('vendedor.listar'))
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.servicios import Servicios
from utils.permisos import requiere_permiso


servicios_bp = Blueprint('servicios', __name__)


@servicios_bp.route('/servicios')
@requiere_permiso('servicios', 'p_leer')
def listar_servicios():
    servicios = Servicios.obtener_servicios()
    vehiculos = Servicios.obtener_vehiculos()
    return render_template(
        'servicios/index.html',
        servicios=servicios,
        vehiculos=vehiculos
    )


@servicios_bp.route('/servicios/nuevo', methods=['GET', 'POST'])
@requiere_permiso('servicios', 'p_crear')
def crear_servicio():
    vehiculos = Servicios.obtener_vehiculos_disponibles()

    if request.method == 'POST':
        nombre_servicio = request.form.get('nombre_servicio', '').strip()
        costo = request.form.get('costo', '').strip()
        descripcion_especifica = request.form.get('descripcion_especifica', '').strip()
        placa = request.form.get('placa', '').strip()

        if not all([nombre_servicio, costo, descripcion_especifica, placa]):
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('servicios.crear_servicio'))

        try:
            Servicios.guardar(nombre_servicio, costo, descripcion_especifica, placa)
            flash('Servicio registrado correctamente.', 'success')
            return redirect(url_for('servicios.listar_servicios'))
        except Exception as e:
            flash(f'Error al registrar servicio: {e}', 'danger')
            return redirect(url_for('servicios.crear_servicio'))

    return render_template('servicios/form.html', vehiculos=vehiculos)


@servicios_bp.route('/servicios/editar/<int:cod_servicios>', methods=['GET', 'POST'])
@requiere_permiso('servicios', 'p_actualizar')
def editar_servicio(cod_servicios):
    servicio = Servicios.obtener_servicio_por_codigo(cod_servicios)
    vehiculos = Servicios.obtener_vehiculos_disponibles()

    if request.method == 'POST':
        nombre_servicio = request.form.get('nombre_servicio', '').strip()
        costo = request.form.get('costo', '').strip()
        descripcion_especifica = request.form.get('descripcion_especifica', '').strip()
        placa = request.form.get('placa', '').strip()

        if not all([nombre_servicio, costo, descripcion_especifica, placa]):
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('servicios.editar_servicio', cod_servicios=cod_servicios))

        try:
            Servicios.actualizar(cod_servicios, nombre_servicio, costo, descripcion_especifica, placa)
            flash('Servicio actualizado correctamente.', 'success')
            return redirect(url_for('servicios.listar_servicios'))
        except Exception as e:
            flash(f'Error al actualizar servicio: {e}', 'danger')
            return redirect(url_for('servicios.editar_servicio', cod_servicios=cod_servicios))

    return render_template(
        'servicios/form.html',
        vehiculos=vehiculos,
        servicio=servicio
    )


@servicios_bp.route('/servicios/inactivar/<int:cod_servicios>', methods=['POST'])
@requiere_permiso('servicios', 'p_eliminar')
def inactivar_servicio(cod_servicios):
    try:
        Servicios.inactivar(cod_servicios)
        flash('Servicio inactivado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al inactivar servicio: {e}', 'danger')
    return redirect(url_for('servicios.listar_servicios'))


@servicios_bp.route('/servicios/finalizar/<int:cod_servicios>/<string:placa>', methods=['POST'])
@requiere_permiso('servicios', 'p_actualizar')
def finalizar_servicio(cod_servicios, placa):
    try:
        Servicios.finalizar(cod_servicios, placa)
        flash('Servicio finalizado y vehículo reactivado.', 'success')
    except Exception as e:
        flash(f'Error al finalizar servicio: {e}', 'danger')
    return redirect(url_for('servicios.listar_servicios'))
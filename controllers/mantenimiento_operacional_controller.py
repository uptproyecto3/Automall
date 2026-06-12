from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.mantenimiento_operacional import MantenimientoOperacional
from utils.permisos import requiere_permiso


mantenimiento_operacional_bp = Blueprint('mantenimiento_operacional', __name__)



@mantenimiento_operacional_bp.route('/mantenimiento-operacional')
@requiere_permiso('mantenimiento_operacional', 'p_leer')
def listar_mantenimiento():
    mantenimientos = MantenimientoOperacional.obtener_mantenimientos()
    talleres = MantenimientoOperacional.obtener_talleres()
    
   
    vehiculos = MantenimientoOperacional.obtener_vehiculos_disponibles()
    
    return render_template(
        'mantenimiento_operacional/index.html',
        mantenimientos=mantenimientos,
        talleres=talleres,
        vehiculos=vehiculos 
    )



@mantenimiento_operacional_bp.route('/mantenimiento-operacional/crear', methods=['GET', 'POST'])
@requiere_permiso('mantenimiento_operacional', 'p_crear')
def crear_mantenimiento():
    talleres = MantenimientoOperacional.obtener_talleres()
    vehiculos = MantenimientoOperacional.obtener_vehiculos_disponibles()

    if request.method == 'POST':
        descripcion_general = request.form.get('descripcion_general', '').strip()
        quien_autoriza = request.form.get('quien_autoriza', '').strip()
        tipo = request.form.get('tipo', '').strip()
        fecha_salida = request.form.get('fecha_salida', '').strip()
        fecha_entrega = request.form.get('fecha_entrega', '').strip()  # Campo opcional
        placa = request.form.get('placa', '').strip()
        cod_taller = request.form.get('cod_taller', '').strip()

        try:
            if not descripcion_general or not quien_autoriza or not tipo or not fecha_salida or not placa or not cod_taller:
                flash('Completa todos los campos obligatorios.', 'warning')
                return render_template(
                    'mantenimiento_operacional/form.html',
                    talleres=talleres,
                    vehiculos=vehiculos,
                    mantenimiento=None
                )

            MantenimientoOperacional.guardar(
                descripcion_general,
                quien_autoriza,
                tipo,
                fecha_salida,
                fecha_entrega if fecha_entrega else None,
                placa,
                cod_taller
            )

            flash('Mantenimiento registrado correctamente.', 'success')
            return redirect(url_for('mantenimiento_operacional.listar_mantenimiento'))

        except Exception:
            flash('Ocurrió un error al guardar el mantenimiento.', 'danger')
            return render_template(
                'mantenimiento_operacional/form.html',
                talleres=talleres,
                vehiculos=vehiculos,
                mantenimiento=None
            )

    return render_template(
        'mantenimiento_operacional/form.html',
        talleres=talleres,
        vehiculos=vehiculos,
        mantenimiento=None
    )



@mantenimiento_operacional_bp.route('/mantenimiento-operacional/editar/<int:cod_mantenimiento>', methods=['GET', 'POST'])
@requiere_permiso('mantenimiento_operacional', 'p_actualizar')
def editar_mantenimiento(cod_mantenimiento):
    talleres = MantenimientoOperacional.obtener_talleres()
    vehiculos = MantenimientoOperacional.obtener_vehiculos_disponibles()
    mantenimientos = MantenimientoOperacional.obtener_mantenimientos()

    mantenimiento = None
    for m in mantenimientos:
        if m['cod_mantenimiento'] == cod_mantenimiento:
            mantenimiento = m
            break

    if not mantenimiento:
        flash('Mantenimiento no encontrado.', 'warning')
        return redirect(url_for('mantenimiento_operacional.listar_mantenimiento'))

    if request.method == 'POST':
        descripcion_general = request.form.get('descripcion_general', '').strip()
        quien_autoriza = request.form.get('quien_autoriza', '').strip()
        tipo = request.form.get('tipo', '').strip()
        fecha_salida = request.form.get('fecha_salida', '').strip()
        fecha_entrega = request.form.get('fecha_entrega', '').strip()  # Campo opcional
        placa = request.form.get('placa', '').strip()
        cod_taller = request.form.get('cod_taller', '').strip()

        try:
            if not descripcion_general or not quien_autoriza or not tipo or not fecha_salida or not placa or not cod_taller:
                flash('Completa todos los campos obligatorios.', 'warning')
                return render_template(
                    'mantenimiento_operacional/form.html',
                    talleres=talleres,
                    vehiculos=vehiculos,
                    mantenimiento=mantenimiento
                )

            MantenimientoOperacional.actualizar(
                cod_mantenimiento,
                descripcion_general,
                quien_autoriza,
                tipo,
                fecha_salida,
                fecha_entrega if fecha_entrega else None,
                placa,
                cod_taller
            )

            flash('Mantenimiento actualizado correctamente.', 'success')
            return redirect(url_for('mantenimiento_operacional.listar_mantenimiento'))

        except Exception:
            flash('Ocurrió un error al actualizar el mantenimiento.', 'danger')
            return render_template(
                'mantenimiento_operacional/form.html',
                talleres=talleres,
                vehiculos=vehiculos,
                mantenimiento=mantenimiento
            )

    return render_template(
        'mantenimiento_operacional/form.html',
        talleres=talleres,
        vehiculos=vehiculos,
        mantenimiento=mantenimiento
    )



@mantenimiento_operacional_bp.route('/mantenimiento-operacional/inactivar/<int:cod_mantenimiento>', methods=['POST'])
@requiere_permiso('mantenimiento_operacional', 'p_actualizar')
def inactivar_mantenimiento(cod_mantenimiento):
    try:
        MantenimientoOperacional.inactivar(cod_mantenimiento)
        flash('Mantenimiento inactivado correctamente.', 'success')
    except Exception:
        flash('Ocurrió un error al inactivar el mantenimiento.', 'danger')

    return redirect(url_for('mantenimiento_operacional.listar_mantenimiento'))



@mantenimiento_operacional_bp.route('/mantenimiento-operacional/finalizar/<int:cod_mantenimiento>/<placa>', methods=['POST'])
@requiere_permiso('mantenimiento_operacional', 'p_actualizar')
def finalizar_mantenimiento(cod_mantenimiento, placa):
    try:
        MantenimientoOperacional.finalizar(cod_mantenimiento, placa)
        flash('Mantenimiento finalizado correctamente.', 'success')
    except Exception:
        flash('Ocurrió un error al finalizar el mantenimiento.', 'danger')

    return redirect(url_for('mantenimiento_operacional.listar_mantenimiento'))
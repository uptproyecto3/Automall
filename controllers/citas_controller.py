from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.citas import citasModel
from utils.decorators import login_required
from utils.validaciones_citas import (
    validar_registro_cita, 
    validar_cambios_superusuario, 
    validar_cambios_hora_cliente
)

citas_bp = Blueprint('citas', __name__)

@citas_bp.route('/consultar')
@login_required
def consultar():
    cod_rol = session.get('cod_rol')
    cedula_usuario = session.get('cedula_usuario')

    if cod_rol == 1:
        # Super Usuario: Ve las citas de todos los usuarios
        lista_citas = citasModel.obtener_citas_transito()
    elif cod_rol == 4:
        # Cliente: Solo ve sus propias citas
        lista_citas = citasModel.obtener_por_cliente(cedula_usuario)
    else:
        flash("No tienes permisos para acceder a esta sección.", "danger")
        return redirect(url_for('index'))
       
    return render_template('citas/consultar.html', citas=lista_citas)


#AGENDAR NUEVA CITA------------------------------------------------------------------------
@citas_bp.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    cedula_usuario = session.get('cedula_usuario')
    cod_rol = session.get('cod_rol')

    # Solo Super Usuario y Cliente pueden agendar citas
    if cod_rol not in [1, 4]:
        flash("No tienes permisos para agendar citas.", "danger")
        return redirect(url_for('citas.consultar'))
    
    if request.method == 'POST':
        fecha = request.form.get('fecha_cita')
        hora = request.form.get('hora_cita')
        cod_catalogo = request.form.get('cod_catalogo')
        
        datos_formulario = {
            'fecha': fecha,
            'hora': hora,
            'cod_catalogo': cod_catalogo
        }

        #Contar citas en el horario seleccionado para control de base de datos
        total_concurrentes = citasModel.contar_citas_en_horario(fecha, hora)

        #Llamar a las utilidades de validación
        es_valido, errores = validar_registro_cita(datos_formulario, total_concurrentes)

        if not es_valido:
            for campo, mensaje in errores.items():
                flash(f"⚠️ {mensaje}", "danger")
            vehiculos_catalogo = citasModel.obtener_todos()
            return render_template('citas/agendar.html', vehiculos=vehiculos_catalogo, datos=request.form)

        try:
            citasModel.registrar_citas(fecha, hora, cod_catalogo, cedula_usuario)
            flash("✨ ¡Cita agendada con éxito!", "success")
            return redirect(url_for('citas.consultar'))
        except Exception as e:
            flash(f"❌ Error al agendar la cita: {str(e)}", "danger")
            vehiculos_catalogo = citasModel.obtener_todos()
            return render_template('citas/agendar.html', vehiculos=vehiculos_catalogo, datos=request.form)
        
    vehiculos_catalogo = citasModel.obtener_todos()
    return render_template('citas/agendar.html', vehiculos=vehiculos_catalogo)

# ELIMINAR CITA-----------------------------------------------------------------
@citas_bp.route('/eliminar/<int:cod_cita>', methods=['POST'])
@login_required
def eliminar_cita(cod_cita):
    cod_rol = session.get('cod_rol')
    cedula_usuario = session.get('cedula_usuario')

    # Si es Cliente (4), intentará cancelar usando su cédula (solo citas pendientes suyas)
    if cod_rol == 4:
        resultado = citasModel.eliminar_cita_db(cod_cita, cedula_usuario=cedula_usuario)
        if resultado['status']:
            flash(resultado['mensaje'], "success")
        else:
            flash(resultado['mensaje'], "danger")
    # Si es Super Usuario (1), tiene el borrado físico sin restricciones
    elif cod_rol == 1:
        resultado = citasModel.eliminar_cita_db(cod_cita)
        if resultado['status']:
            flash("✨ Cita eliminada del sistema con éxito.", "warning")
        else:
            flash(resultado['mensaje'], "danger")
    else:
        flash("No tienes permisos para realizar esta acción.", "danger")

    return redirect(url_for('citas.consultar'))

# Modificar Cita----------------------------------------------------------------------------
@citas_bp.route('/modificar/<int:cod_cita>', methods=['POST'])
@login_required
def modificar(cod_cita):
    cod_rol = session.get('cod_rol')
    cedula_usuario = session.get('cedula_usuario')

    cita_original = citasModel.obtener_cita_por_id(cod_cita)
    if not cita_original:
        flash("⚠️ No se pudo localizar la cita seleccionada.", "danger")
        return redirect(url_for('citas.consultar'))

    if cod_rol == 4:
        citas_cliente = citasModel.obtener_por_cliente(cedula_usuario)
        pertenece = any(int(c['cod_citas']) == int(cod_cita) for c in citas_cliente)
        if not pertenece:
            flash("Acceso denegado: No tienes autorización sobre esta cita.", "danger")
            return redirect(url_for('citas.consultar'))

        # El cliente solo puede modificar la hora. Mantenemos fecha y estado originales.
        nueva_hora = request.form.get('hora')
        fecha_cita = str(cita_original['fecha'])
        estado_cita = str(cita_original['estado'])

        # Contar citas simultáneas en la misma fecha y la nueva hora (excluyendo esta cita)
        total_concurrentes = citasModel.contar_citas_en_horario(fecha_cita, nueva_hora, cod_cita_excluir=cod_cita)

        es_valido, errores = validar_cambios_hora_cliente(
            nueva_hora, fecha_cita, estado_cita, total_concurrentes
        )

        if not es_valido:
            for campo, mensaje in errores.items():
                flash(f"⚠️ {mensaje}", "danger")
            return redirect(url_for('citas.consultar'))

        datos_formulario = {
            'cod_citas': cod_cita,
            'fecha': fecha_cita,
            'hora': nueva_hora,
            'estado': estado_cita
        }

    elif cod_rol == 1:
        # SUPER USUARIO: Puede modificar fecha, hora y estado
        fecha_req = request.form.get('fecha') or str(cita_original['fecha'])
        hora_req = request.form.get('hora') or str(cita_original['hora'])
        estado_req = request.form.get('estado') or str(cita_original['estado'])

        datos_formulario = {
            'cod_citas': cod_cita,
            'fecha': fecha_req,
            'hora': hora_req,
            'estado': estado_req
        }

        # Contar citas simultáneas en la nueva fecha y hora (excluyendo esta cita)
        total_concurrentes = citasModel.contar_citas_en_horario(fecha_req, hora_req, cod_cita_excluir=cod_cita)

        es_valido, errores = validar_cambios_superusuario(datos_formulario, total_concurrentes)

        if not es_valido:
            for campo, mensaje in errores.items():
                flash(f"⚠️ {mensaje}", "danger")
            return redirect(url_for('citas.consultar'))
    else:
        flash("No tienes permisos para modificar citas.", "danger")
        return redirect(url_for('citas.consultar'))

    try:
        citasModel.actualizar_cita(datos_formulario)
        flash("✨ La cita ha sido reprogramada y actualizada con éxito.", "success")
    except Exception as e:
        flash(f"❌ Error al guardar modificaciones: {str(e)}", "danger")
        
    return redirect(url_for('citas.consultar'))


# FINALIZAR CITA----------------------------------------------------------------------------
@citas_bp.route('/finalizar/<int:cod_citas>', methods=['POST'])
@login_required
def finalizar_cita(cod_citas):
    cod_rol = session.get('cod_rol')

    # Solo el Super Usuario puede finalizar citas
    if cod_rol != 1:
        flash("Acceso denegado: Solo el Super Usuario puede finalizar citas.", "danger")
        return redirect(url_for('citas.consultar'))

    citasModel.finalizar_cita_db(cod_citas)
    flash("✨ ¡La cita ha sido marcada como Finalizada!", "success")
    return redirect(url_for('citas.consultar'))
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.taller import Taller
from utils.permisos import requiere_permiso, requiere_superusuario

tallerbp = Blueprint('tallerbp', __name__)

@tallerbp.route('/taller')
@requiere_permiso('Taller', 'p_leer')
def listar_talleres():
    talleres = Taller.obtener_todos()
    return render_template('taller/index.html', talleres=talleres)

@tallerbp.route('/taller/nuevo', methods=['GET', 'POST'])
@requiere_permiso('Taller', 'p_crear')
def crear_taller():
    if request.method == 'POST':
        nombre_taller = request.form.get('nombre_taller', '').strip()
        direccion = request.form.get('direccion', '').strip()
        estado = request.form.get('estado', '1')

        if not nombre_taller or not direccion:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('tallerbp.crear_taller'))

        Taller.guardar(nombre_taller, direccion, estado)
        flash('Taller registrado correctamente.', 'success')
        return redirect(url_for('tallerbp.listar_talleres'))

    return render_template('taller/form.html', taller=None)

@tallerbp.route('/taller/editar/<int:cod_taller>', methods=['GET', 'POST'])
@requiere_permiso('Taller', 'p_actualizar')
def editar_taller(cod_taller):
    taller = Taller.obtener_por_id(cod_taller)

    if not taller:
        flash('El taller no existe.', 'danger')
        return redirect(url_for('tallerbp.listar_talleres'))

    if request.method == 'POST':
        nombre_taller = request.form.get('nombre_taller', '').strip()
        direccion = request.form.get('direccion', '').strip()
        estado = request.form.get('estado', '1')

        if not nombre_taller or not direccion:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('tallerbp.editar_taller', cod_taller=cod_taller))

        Taller.actualizar(cod_taller, nombre_taller, direccion, estado)
        flash('Taller actualizado correctamente.', 'success')
        return redirect(url_for('tallerbp.listar_talleres'))

    return render_template('taller/form.html', taller=taller)

@tallerbp.route('/taller/eliminar/<int:cod_taller>', methods=['POST'])
@requiere_permiso('Taller', 'p_eliminar')
def eliminar_taller(cod_taller):
    Taller.eliminar(cod_taller)
    flash('Taller desactivado correctamente.', 'success')
    return redirect(url_for('tallerbp.listar_talleres'))
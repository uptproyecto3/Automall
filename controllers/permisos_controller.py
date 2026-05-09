from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.permiso import Permiso
from utils.permisos import requiere_superusuario # Importamos el decorador
permisos_bp = Blueprint('permisos', __name__)



@permisos_bp.route('/gestionar', methods=['GET', 'POST'])
@requiere_superusuario  # <--- AQUÍ ESTÁ EL BLOQUEO REAL
def gestionar():
    # 1. Si enviamos el formulario de actualizar
    if request.method == 'POST':
        id_rol_actual = request.form.get('id_rol_actual')
        ids = request.form.getlist('id_permiso')
        
        for id_p in ids:
            p_crear = 1 if request.form.get(f'crear_{id_p}') else 0
            p_leer = 1 if request.form.get(f'leer_{id_p}') else 0
            p_actualizar = 1 if request.form.get(f'actualizar_{id_p}') else 0
            p_eliminar = 1 if request.form.get(f'eliminar_{id_p}') else 0
            Permiso.actualizar(id_p, p_crear, p_leer, p_actualizar, p_eliminar)
            
        flash("Permisos actualizados para este rol")
        return redirect(url_for('permisos.gestionar', id_rol=id_rol_actual))

    # 2. Si entramos por GET (Cargar datos)
    roles = Permiso.obtener_roles()
    id_rol_seleccionado = request.args.get('id_rol', type=int)
    permisos = []
    
    if id_rol_seleccionado:
        permisos = Permiso.obtener_por_rol(id_rol_seleccionado)
        
    return render_template('permisos/gestionar.html', 
                           roles=roles, 
                           permisos=permisos, 
                           id_rol_seleccionado=id_rol_seleccionado)
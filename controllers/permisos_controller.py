from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.permiso import Permiso
from utils.permisos import requiere_superusuario 

permisos_bp = Blueprint('permisos', __name__) 

@permisos_bp.route('/gestionar', methods=['GET', 'POST'])
@requiere_superusuario  
def gestionar():
    # 1. Si enviamos el formulario para guardar cambios
    if request.method == 'POST':
        id_rol_actual = request.form.get('id_rol_actual')
        # Captura todos los valores de los checkboxes marcados en el HTML
        permisos_marcados = request.form.getlist('permisos_activos') 
        
        resultado = Permiso.sincronizar_permisos(id_rol_actual, permisos_marcados)
        
        if resultado["status"]:
            flash("Matriz de permisos actualizada con éxito para este rol.")
        else:
            flash(f"Error al procesar la actualización: {resultado['error']}")
            
        return redirect(url_for('permisos.gestionar', cod_rol=id_rol_actual))

    # 2. Si entramos por GET (Cargar vista de administración)
    roles = Permiso.obtener_roles()
    id_rol_seleccionado = request.args.get('cod_rol', type=int)
    matriz_permisos = []
    
    if id_rol_seleccionado:
        # Obtenemos la lista plana relacional
        matriz_permisos = Permiso.obtener_matriz_permisos(id_rol_seleccionado)
        
    return render_template('permisos/gestionar.html', 
                           roles=roles, 
                           permisos=matriz_permisos, 
                           id_rol_seleccionado=id_rol_seleccionado)
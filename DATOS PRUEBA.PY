#BLOQUEO DE PERMISOS A NIVEL DE BACKEND

@requiere_permiso('Usuarios', 'p_crear') # <--- Si no tiene p_eliminar=1 en la BD, no entra
@requiere_permiso('Usuarios', 'p_leer')
@requiere_permiso('Usuarios', 'p_actualizar')
@requiere_permiso('Usuarios', 'p_eliminar')

#EJEMPLO 

@auth_bp.route('/usuarios/eliminar/<int:id>')
@requiere_permiso('Usuarios'#ESTE ES EL MODULO A ACCEDER, 
                  'p_eliminar'#ESTE EL PERMISO) #SE COLOCAN JUSTO AQUI ESTA LINEA DE CODIGO PARA EVITAR QUE HAGA LA ACCION REQUERIDA
def eliminar(id):
    Usuario.eliminar(id)
    return redirect(url_for('auth.listar'))


    #A NIVEL DE FRONT END SE UTILIZA ASI
    #SE ENCIERRA EL BOTON A ELIMINAR DENTRO DE EL CONDICIONAL PARA QUE NO LE MUESTRE EL BOTON SI NO PUEDE ACCEDER
    {% if tiene_permiso('Usuarios', 'p_leer') %}#ESTE CONDICIONAL DE ACA LE DICE SI PUEDE VERLO O NO
        <a class="nav-link" href="{{ url_for('auth.listar') }}">Usuarios</a>#SE USA LEER QUE ES EL PRINCIPAL PARA LISTAR TODO
                    
    {% endif %}


    
    #PARA BLOQUEAR VISTAS QUE NO SE PUEDA ACCEDER SIN INICIAR SESION SE USA
    @auth_bp.route('/usuarios/eliminar/<int:id>')
    @login_required #ASI SE EVITA QUE PUEDAN ACCEDER AL MODULO SI NO HAN INICIADO SESION
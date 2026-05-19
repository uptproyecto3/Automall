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




    #NAV CON TODOS LOS PERMISOS LISTOS

    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
    <div class="container">
        <a class="navbar-brand fw-bold" href="/">
            <i class="bi bi-car-front-fill me-2 text-primary"></i>AutoMall
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto align-items-center">
                <li class="nav-item"><a class="nav-link" href="/">Inicio</a></li>

                {% if 'usuario_nombre' in session %}
                    
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navOperaciones" role="button" data-bs-toggle="dropdown">
                            Operaciones
                        </a>
                        <ul class="dropdown-menu shadow border-0">
                            <li><h6 class="dropdown-header">Inventario y Flota</h6></li>
                            {% if tiene_permiso('Vehículos', 'p_leer') %}
                                <li><a class="dropdown-item" href="{{ url_for('vehiculos.lista') }}"><i class="bi bi-search me-2"></i>Catálogo de Vehículos</a></li>
                            {% endif %}
                            <li><a class="dropdown-item" href="/mantenimiento-vehiculos"><i class="bi bi-tools me-2"></i>Mantenimiento</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><h6 class="dropdown-header">Abastecimiento</h6></li>
                            <li><a class="dropdown-item" href="/proveedores"><i class="bi bi-person-badge-fill me-2"></i>Proveedores</a></li>
                            <li><a class="dropdown-item" href="/adquisicion"><i class="bi bi-cart-plus me-2"></i>Adquisición de Vehículos</a></li>
                        </ul>
                    </li>

                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navVentas" role="button" data-bs-toggle="dropdown">
                            Ventas y Citas
                        </a>
                        <ul class="dropdown-menu shadow border-0">
                            <li><a class="dropdown-item" href="/ventas"><i class="bi bi-cash-stack me-2"></i>Venta de Vehículos</a></li>
                            <li><a class="dropdown-item" href="/traspasos"><i class="bi bi-journal-check me-2"></i>Traspaso de Vehículos</a></li>
                            <li><a class="dropdown-item" href="/citas"><i class="bi bi-calendar-event me-2"></i>Gestión de Citas</a></li>
                        </ul>
                    </li>

                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle fw-bold text-info" href="#" id="navConfig" role="button" data-bs-toggle="dropdown">
                            <i class="bi bi-gear-fill me-1"></i> Sistema
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end shadow border-0">
                            <li><h6 class="dropdown-header">Administración</h6></li>
                            {% if tiene_permiso('Usuarios', 'p_leer') %}
                                <li><a class="dropdown-item" href="{{ url_for('auth.listar') }}"><i class="bi bi-people me-2"></i>Gestión de Usuarios</a></li>
                            {% endif %}
                            {% if tiene_permiso('Permisos', 'p_leer') %}
                                <li><a class="dropdown-item" href="{{ url_for('permisos.gestionar') }}"><i class="bi bi-shield-lock me-2"></i>Permisos y Roles</a></li>
                            {% endif %}
                            <li><a class="dropdown-item" href="/bitacora"><i class="bi bi-list-check me-2"></i>Bitácora de Auditoría</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><h6 class="dropdown-header">Reportes y Datos</h6></li>
                            <li><a class="dropdown-item" href="/reportes"><i class="bi bi-file-earmark-bar-graph me-2"></i>Reportes Estadísticos</a></li>
                            <li><a class="dropdown-item" href="/respaldo"><i class="bi bi-database-fill-gear me-2"></i>Mantenimiento de BD</a></li>
                        </ul>
                    </li>

                    <li class="nav-item ms-lg-3">
                        <a class="btn btn-outline-warning btn-sm rounded-pill px-3" href="/logout">
                            <i class="bi bi-box-arrow-right"></i> Salir
                        </a>
                    </li>

                {% else %}
                    <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.login') }}">Login</a></li>
                    <li class="nav-item">
                        <a class="btn btn-primary btn-sm rounded-pill px-4 ms-lg-2" href="{{ url_for('auth.registro') }}">Registro</a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>

#PARA AGREGAR DESPUES CUANDO ESTEN TODOS LOS MODULOS





#PARA REGISTRAR EN BITACORA SE DEBE ANEXAR LA SIGUIENTE LINEA DE CODIGO

Bitacora.registrar(session['usuario_nombre'], f"Eliminó el Usuario ID: {id}", "Usuarios")


#SE CAMBIA LA ACCION Y EL MODULO EN DONDE SE REALIZO PUEDE SER EN CUALQUIER ACCION, ELIMINAR,REGISTRAR O EDITAR

QUEDARIA ASI:

Bitacora.registrar(session['usuario_nombre'], f"Eliminó el Usuario ID: {id}", "Usuarios")
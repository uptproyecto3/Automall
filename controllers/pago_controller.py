import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.pagos import Pagos
from utils.permisos import requiere_permiso
from utils.decorators import login_required

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/pagos/listar_pagos')
@login_required
def listar_pagos():

    cedula_usuario = session.get('cedula_usuario')

    pagos = Pagos.obtener_todos(cedula_usuario)

    if not pagos:
        return render_template('pagos/lista_pagos.html', pagos=[], mensaje="No se encontraron pagos registrados.")
    
    return render_template('pagos/lista_pagos.html', pagos=pagos)

@pagos_bp.route('/pagos/registrar_pago')
@login_required
def registrar_pago():
    # Aquí iría el formulario para pagar cuotas
    return render_template('pagos/registrar.html')
    

from flask import Blueprint, render_template, session
from models.bitacora import Bitacora
from utils.decorators import login_required
from utils.permisos import requiere_permiso

bitacora_bp = Blueprint('bitacora', __name__)

@bitacora_bp.route('/bitacora')
@login_required
@requiere_permiso('Bitácora', 'p_leer')
def listar_bitacora():
    # Obtenemos todos los registros usando el modelo que creamos
    logs = Bitacora.obtener_todas()
    return render_template('bitacora/bitacora.html', logs=logs)
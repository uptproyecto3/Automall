from flask import Blueprint, render_template
from models.catalogo import Catalogo
from utils.permisos import requiere_permiso

catalogo_bp = Blueprint('catalogo', __name__)

@catalogo_bp.route('/catalogo')
@requiere_permiso('Vehiculo', 'p_leer') # Ajusta el permiso según tu tabla
def lista_publica():
    # Obtenemos solo los carros que están en estado 'Disponible'
    productos = Catalogo.obtener_disponibles()
    return render_template('catalogo/lista.html', productos=productos)
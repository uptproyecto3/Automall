from flask import Blueprint, render_template
from models.catalogo import Catalogo

catalogo_bp = Blueprint('catalogo', __name__)

@catalogo_bp.route('/catalogo-ventas')
def listar():
    vehiculos = Catalogo.obtener_disponibles()
    return render_template('vehiculos/catalogo_lista.html', vehiculos=vehiculos)
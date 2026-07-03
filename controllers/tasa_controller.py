from flask import Blueprint, jsonify
from utils.decorators import login_required
from models.tasa import Tasa
import requests
from datetime import datetime
tasa_bp = Blueprint('tasa', __name__)


@tasa_bp.route('/tasa/api/obtener_tasa', methods=['GET'])
@login_required
def obtener_tasa():
    try:
        tasa_db = Tasa.get_tasa()
        fecha_hoy = datetime.now().date()
        necesita_actualizar = False

        # 1. Evaluar si necesitamos conectarnos a la API
        if not tasa_db:
            necesita_actualizar = True
        else:
            # Asumiendo que tu columna de fecha se llama 'fecha'
            # y tu columna del precio se llama 'valor'
            fecha_guardada = tasa_db.get('fecha')
            
            # Si la fecha guardada no es la de hoy, hay que actualizar
            if fecha_guardada != fecha_hoy:
                necesita_actualizar = True

        # 2. Si necesita actualizar, llamamos a DolarApi
        if necesita_actualizar:
            respuesta = requests.get('https://ve.dolarapi.com/v1/dolares/oficial', timeout=5)
            
            if respuesta.status_code == 200:
                data = respuesta.json()
                nuevo_valor = data.get('promedio')
                
                # Guardamos la nueva tasa en la base de datos
                Tasa.guardar_nueva_tasa(nuevo_valor)
                
                return jsonify({
                    'status': 'success', 
                    'tasa': nuevo_valor, 
                    'mensaje': 'Tasa actualizada desde BCV'
                })
            else:
                # Si la API falla por alguna razón, usamos la última guardada como respaldo
                if tasa_db:
                    return jsonify({
                        'status': 'warning', 
                        'tasa': tasa_db.get('valor'), 
                        'mensaje': 'API no respondió, usando última tasa guardada'
                    })

        # 3. Si NO necesita actualizar (ya es de hoy), devolvemos la de la BD
        return jsonify({
            'status': 'success', 
            'tasa': tasa_db.get('valor'), 
            'mensaje': 'Tasa obtenida de base de datos'
        })

    except Exception as e:
        print(f"Error en obtener_tasa: {e}")
        return jsonify({'status': 'error', 'message': 'Ocurrió un error en el servidor'}), 500
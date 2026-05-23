import os
import subprocess
from flask import Blueprint, render_template, jsonify, request, send_file

mantenimiento_bp = Blueprint('mantenimiento', __name__)

# Configuración de conexión (Ajusta con tus credenciales)
DB_USER = "root"
DB_PASS = ""
DATABASES = ["seguridad", "automall"]

@mantenimiento_bp.route('/mantenimiento')
def vista_mantenimiento():
    # Renderiza la interfaz con los botones
    return render_template('mantenimiento/mant_bd.html')

@mantenimiento_bp.route('/api/backup/<db_name>', methods=['GET'])
def respaldar_bd(db_name):
    if db_name not in DATABASES:
        return jsonify({"status": "error", "message": "Base de datos no válida"}), 400
    
    filename = f"backup_{db_name}.sql"
    filepath = os.path.join(os.environ.get('TEMP', ''), filename) if os.name == 'nt' else os.path.join('/tmp', filename)

    try:
        # Buscamos si existe la variable en el archivo .env de esta PC
        bin_path = os.environ.get('MYSQL_BIN_PATH', '')
        
        # Construimos el comando dinámicamente apuntando al ejecutable
        mysqldump_exe = os.path.join(bin_path, "mysqldump")
        
        # Si la contraseña está vacía, no incluimos el parámetro -p
        pass_arg = f"-p{DB_PASS}" if DB_PASS else ""
        
        comando = f'"{mysqldump_exe}" -u {DB_USER} {pass_arg} {db_name} > "{filepath}"'
        
        subprocess.run(comando, shell=True, check=True)

        return send_file(filepath, as_attachment=True, download_name=filename)

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Error al generar el respaldo: {str(e)}"}), 500

@mantenimiento_bp.route('/api/restore/<db_name>', methods=['POST'])
def restaurar_bd(db_name):
    if db_name not in DATABASES:
        return jsonify({"status": "error", "message": "Base de datos no válida"}), 400

    if 'backup_file' not in request.files:
        return jsonify({"status": "error", "message": "No se subió ningún archivo"}), 400

    file = request.files['backup_file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Archivo no seleccionado"}), 400

    # Guardar el archivo temporalmente recibido desde la PC del usuario
    filename = f"restore_{db_name}.sql"
    filepath = os.path.join("/tmp", filename) if os.name != 'nt' else os.path.join(os.environ.get('TEMP', ''), filename)
    file.save(filepath)

    try:
        # Ejecuta el comando nativo de restauración (mysql)
        comando = f"mysql -u {DB_USER} -p{DB_PASS} {db_name} < {filepath}"
        subprocess.run(comando, shell=True, check=True)
        
        return jsonify({"status": "success", "message": f"Base de datos '{db_name}' restaurada con éxito."})

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Error al restaurar: {str(e)}"}), 500
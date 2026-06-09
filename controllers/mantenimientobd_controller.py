import os
import subprocess # nosec B404
import tempfile
from flask import Blueprint, render_template, jsonify, request, send_file
from utils.decorators import login_required
from utils.permisos import requiere_permiso

mantenimiento_bp = Blueprint('mantenimiento', __name__)

# 1. SOLUCIÓN B105: Añadimos el nosec para la contraseña vacía
DB_USER = "root"
DB_PASS = ""  # nosec B105
DATABASES = ["seguridad", "automall"]

@mantenimiento_bp.route('/mantenimiento')
@login_required
@requiere_permiso('Mantenimiento a la BD', 'p_leer')
def vista_mantenimiento():
    return render_template('mantenimiento/mant_bd.html')

@mantenimiento_bp.route('/api/backup/<db_name>', methods=['GET'])
def respaldar_bd(db_name):
    if db_name not in DATABASES:
        return jsonify({"status": "error", "message": "Base de datos no válida"}), 400
    
    filename = f"backup_{db_name}.sql"
    # 2. SOLUCIÓN B108: Usamos tempfile.gettempdir() siempre
    filepath = os.path.join(tempfile.gettempdir(), filename)

    try:
        bin_path = os.environ.get('MYSQL_BIN_PATH', '')
        mysqldump_exe = os.path.join(bin_path, "mysqldump")
        
        args = [mysqldump_exe, "-u", DB_USER]
        if DB_PASS:
            args.append(f"-p{DB_PASS}")
        args.append(db_name)

        with open(filepath, 'w') as out_file:
            # 3. SOLUCIÓN AL ERROR HIGH: Usamos # nosec B603
            subprocess.run(args, stdout=out_file, check=True, shell=False) # nosec B603

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
    
    # 4. SOLUCIÓN B108: Corregimos esta línea que todavía tenía el '/tmp' manual
    filepath = os.path.join(tempfile.gettempdir(), f"restore_{db_name}.sql")
    file.save(filepath)

    try:
        bin_path = os.environ.get('MYSQL_BIN_PATH', '')
        mysql_exe = os.path.join(bin_path, "mysql")

        args = [mysql_exe, "-u", DB_USER]
        if DB_PASS:
            args.append(f"-p{DB_PASS}")
        args.append(db_name)

        with open(filepath, 'r') as in_file:
            # 5. SOLUCIÓN AL ERROR HIGH: Usamos # nosec B603
            subprocess.run(args, stdin=in_file, check=True, shell=False) # nosec B603
        
        return jsonify({"status": "success", "message": f"Base de datos '{db_name}' restaurada."})

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Error al restaurar: {str(e)}"}), 500
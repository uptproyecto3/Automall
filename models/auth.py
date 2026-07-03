from models.db import obtener_conexion_seguridad
from utils.validaciones import ValidacionUsuario  
from werkzeug.security import check_password_hash 

class Auth: 
    def __init__(self, cedula_usuario, nombre, apellido, telefono, direccion, correo, password):
        self.cedula_usuario = cedula_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        self.password = password

    @staticmethod
    def verificar_credenciales(correo, password):
        error_correo = ValidacionUsuario.validar_formato_correo(correo)
        if error_correo:
            return {"error": error_correo} 

        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        sql = "SELECT cedula_usuario, nombre, cod_rol, password FROM t_usuario WHERE correo = %s"
        cursor.execute(sql, (correo,))
        usuario = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if usuario:
            db_password = usuario['password']
            
            # 1. Si la clave es un Hash moderno d e Flask (empieza por pbkdf2 o scrypt)
            if db_password.startswith('pbkdf2:') or db_password.startswith('scrypt:'):
                if check_password_hash(db_password, password):
                    usuario.pop('password', None)
                    return usuario
            # 2. Respaldo: Si es una clave vieja guardada en texto plano (sin hashear)
            else:
                if db_password == password:
                    usuario.pop('password', None)
                    return usuario
            
        return None
    
    @staticmethod
    def obtener_pregunta(correo):
        # Validar formato de correo
        error_correo = ValidacionUsuario.validar_formato_correo(correo)
        if error_correo:
            return None

        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        sql = "SELECT pregunta_seguridad FROM t_usuario WHERE correo = %s"
        cursor.execute(sql, (correo,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        return resultado

    @staticmethod
    def validar_respuesta(correo, respuesta):
        # Validar formato de correo
        if ValidacionUsuario.validar_formato_correo(correo):
            return None
            
        # Validar que la respuesta no sea vacía
        if not respuesta or respuesta.strip() == "":
            return None

        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        # Comparamos correo y respuesta
        sql = "SELECT cedula_usuario FROM t_usuario WHERE correo = %s AND respuesta_seguridad = %s"
        cursor.execute(sql, (correo, respuesta))
        usuario = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        return usuario 

    @staticmethod
    def actualizar_password(correo, nueva_password):
        # 1. VALIDACIONES antes de guardar
        # Validar formato del correo
        error_correo = ValidacionUsuario.validar_formato_correo(correo)
        if error_correo:
            return {"status": False, "mensaje": error_correo}
        
        # Validar que la nueva contraseña sea segura
        error_pass = ValidacionUsuario.validar_password_segura(nueva_password)
        if error_pass:
            return {"status": False, "mensaje": error_pass}

        # 2. Si las validaciones pasan, se guarda en la BD
        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor()
            
            sql = "UPDATE t_usuario SET password = %s WHERE correo = %s"
            cursor.execute(sql, (nueva_password, correo))
            conexion.commit()
            
            filas_afectadas = cursor.rowcount
            
            cursor.close()
            conexion.close()
            
            if filas_afectadas > 0:
                return {"status": True, "mensaje": "Contraseña actualizada exitosamente."}
            else:
                return {"status": False, "mensaje": "No se encontró el usuario para actualizar."}
                
        except Exception as e:
            return {"status": False, "mensaje": f"Error en la base de datos: {str(e)}"}
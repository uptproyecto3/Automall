from models.db import obtener_conexion_seguridad
from utils.validaciones import ValidacionUsuario  # Importamos la clase de validaciones

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
        # Validar formato de correo antes de consultar
        error_correo = ValidacionUsuario.validar_formato_correo(correo)
        if error_correo:
            # Puedes retornar un diccionario o manejar el error según tu controlador
            return {"error": error_correo} 

        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        # IMPORTANTE: Se incluye cod_rol para el manejo de sesiones
        sql = "SELECT cedula_usuario, nombre, cod_rol FROM t_usuario WHERE correo = %s AND password = %s"
        cursor.execute(sql, (correo, password))
        usuario = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        return usuario
    
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
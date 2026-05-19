from models.db import obtener_conexion_seguridad

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
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        # IMPORTANTE: Asegúrate de incluir 'id_rol' en el SELECT
        sql = "SELECT id, nombre, cedula_usuario, id_rol FROM t_usuario WHERE correo = %s AND password = %s"
        cursor.execute(sql, (correo, password))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario
    
    @staticmethod
    def obtener_pregunta(correo):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        # Solo traemos la pregunta para mostrársela al usuario
        sql = "SELECT pregunta_seguridad FROM t_usuario WHERE correo = %s"
        cursor.execute(sql, (correo,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado

    @staticmethod
    def validar_respuesta(correo, respuesta):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        # Comparamos correo y respuesta
        sql = "SELECT id FROM t_usuario WHERE correo = %s AND respuesta_seguridad = %s"
        cursor.execute(sql, (correo, respuesta))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario # Si devuelve algo, la respuesta es correcta

    @staticmethod
    def actualizar_password(correo, nueva_password):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        sql = "UPDATE t_usuario SET password = %s WHERE correo = %s"
        cursor.execute(sql, (nueva_password, correo))
        conexion.commit()
        cursor.close()
        conexion.close()
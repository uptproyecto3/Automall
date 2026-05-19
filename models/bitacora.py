from models.db import obtener_conexion_seguridad

class Bitacora:
    @staticmethod
    def registrar(cedula_usuario, accion, modulo):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        sql = "INSERT INTO t_bitacora (cedula_usuario, accion, modulo) VALUES (%s, %s, %s)"
        cursor.execute(sql, (cedula_usuario, accion, modulo))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_todas():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM t_bitacora ORDER BY fecha DESC")
        logs = cursor.fetchall()
        cursor.close()
        conexion.close()
        return logs
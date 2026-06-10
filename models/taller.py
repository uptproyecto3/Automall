from models.db import obtener_conexion

class Taller:
    def __init__(self, cod_taller=None, nombre_taller=None, direccion=None, estado='1'):
        self.cod_taller = cod_taller
        self.nombre_taller = nombre_taller
        self.direccion = direccion
        self.estado = estado

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT cod_taller, nombre_taller, direccion, estado
            FROM taller
            ORDER BY cod_taller DESC
        """)
        talleres = cursor.fetchall()
        cursor.close()
        conexion.close()
        return talleres

    @staticmethod
    def obtener_por_id(cod_taller):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT cod_taller, nombre_taller, direccion, estado
            FROM taller
            WHERE cod_taller = %s
        """, (cod_taller,))
        taller = cursor.fetchone()
        cursor.close()
        conexion.close()
        return taller

    @staticmethod
    def guardar(nombre_taller, direccion, estado='1'):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO taller (nombre_taller, direccion, estado)
            VALUES (%s, %s, %s)
        """, (nombre_taller, direccion, estado))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True

    @staticmethod
    def actualizar(cod_taller, nombre_taller, direccion, estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE taller
            SET nombre_taller = %s,
                direccion = %s,
                estado = %s
            WHERE cod_taller = %s
        """, (nombre_taller, direccion, estado, cod_taller))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True

    @staticmethod
    def eliminar(cod_taller):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE taller
            SET estado = '0'
            WHERE cod_taller = %s
        """, (cod_taller,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
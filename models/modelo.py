from models.db import obtener_conexion

class Modelo:
    @staticmethod
    def guardar(nombre, estado, cod_marca):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "INSERT INTO modelo (nombre_modelo, estado, cod_marca) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, estado, cod_marca))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_todas():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT m.*, ma.nombre_marca 
            FROM modelo m 
            INNER JOIN marca ma ON m.cod_marca = ma.cod_marca
        """
        cursor.execute(sql)
        modelos = cursor.fetchall()
        conexion.close()
        return modelos

    @staticmethod
    def actualizar(id, nombre, estado, cod_marca):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE modelo SET nombre_modelo=%s, estado=%s, cod_marca=%s WHERE cod_modelo=%s"
        cursor.execute(sql, (nombre, estado, cod_marca, id))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar(id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "DELETE FROM modelo WHERE cod_modelo = %s"
        cursor.execute(sql, (id,))
        conexion.commit()
        cursor.close()
        conexion.close()
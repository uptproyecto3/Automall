from models.db import obtener_conexion

class Modelo:
    @staticmethod
    def guardar(nombre, estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "INSERT INTO modelo (nombre_modelo, estado) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, estado))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_todas():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM modelo")
        modelos = cursor.fetchall()
        conexion.close()
        return modelos

    @staticmethod
    def eliminar(id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM modelo WHERE cod_modelo = %s", (id,))
        conexion.commit()
        conexion.close()
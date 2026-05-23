from models.db import obtener_conexion

class Marca:
    @staticmethod
    def guardar(nombre, estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "INSERT INTO marca (nombre_marca, estado) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, estado))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_todas():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM marca")
        marcas = cursor.fetchall()
        conexion.close()
        return marcas

    @staticmethod
    def eliminar(id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM marca WHERE cod_marca = %s", (id,))
        conexion.commit()
        conexion.close()
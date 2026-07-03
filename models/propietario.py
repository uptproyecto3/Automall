from models.db import obtener_conexion

class Propietario:
    @staticmethod
    def guardar(cedula, razon_social, telefono, direccion, tipo, estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """INSERT INTO propietario (cedula_propietario, razon_social, telefono, direccion, tipo, estado) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (cedula, razon_social, telefono, direccion, tipo, estado))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM propietario")
        propietarios = cursor.fetchall()
        conexion.close()
        return propietarios

    @staticmethod
    def eliminar(cedula):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM propietario WHERE cedula_propietario = %s", (cedula,))
        conexion.commit()
        conexion.close()
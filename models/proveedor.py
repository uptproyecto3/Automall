from models.db import obtener_conexion

class Proveedor:
    @staticmethod
    def guardar(cedula, razon_social, telefono, direccion, tipo, estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """INSERT INTO proveedor (cedula_proveedor, razon_social, telefono, direccion, tipo, estado) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (cedula, razon_social, telefono, direccion, tipo, estado))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM proveedor")
        proveedores = cursor.fetchall()
        conexion.close()
        return proveedores

    @staticmethod
    def eliminar(cedula):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM proveedor WHERE cedula_proveedor = %s", (cedula,))
        conexion.commit()
        conexion.close()
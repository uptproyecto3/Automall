from models.db import obtener_conexion_seguridad

class Vehiculo:
    @staticmethod
    def guardar(placa, color, anio, tipo, estado, marca, modelo, cedula, imagen):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        sql = """INSERT INTO vehiculo (Placa, Color, Anio, Tipo, Estado, Marca, Modelo, Cedula_Proveedor, Imagen_URL) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (placa, color, anio, tipo, estado, marca, modelo, cedula, imagen))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion_seguridad()
        # Usamos dictionary=True para poder acceder por nombre (ej: v['Placa'])
        cursor = conexion.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM vehiculo")
        vehiculos = cursor.fetchall()
        conexion.close()
        return vehiculos
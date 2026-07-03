from models.db import obtener_conexion

class Insumo:
    def __init__(self, nombre_insumo, descripcion=None, stock=0):
        self.nombre_insumo = nombre_insumo
        self.descripcion = descripcion
        self.stock = stock

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM insumos ORDER BY nombre_insumo")
        insumos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return insumos

    @staticmethod
    def obtener_por_id(cod_insumo):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM insumos WHERE cod_insumo = %s", (cod_insumo,))
        insumo = cursor.fetchone()
        cursor.close()
        conexion.close()
        return insumo

    @staticmethod
    def crear(nombre_insumo, descripcion, stock=0):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO insumos (nombre_insumo, descripcion, stock) 
            VALUES (%s, %s, %s)
        """, (nombre_insumo, descripcion, stock))
        conexion.commit()
        cod_insumo = cursor.lastrowid
        cursor.close()
        conexion.close()
        return cod_insumo

    @staticmethod
    def actualizar(cod_insumo, nombre_insumo, descripcion, stock):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE insumos 
            SET nombre_insumo = %s, descripcion = %s, stock = %s 
            WHERE cod_insumo = %s
        """, (nombre_insumo, descripcion, stock, cod_insumo))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True

    @staticmethod
    def eliminar(cod_insumo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM insumos WHERE cod_insumo = %s", (cod_insumo,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
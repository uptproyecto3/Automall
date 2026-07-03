from models.db import obtener_conexion
from datetime import datetime

class Tasa:
    @staticmethod
    def get_tasa():
        conexion = obtener_conexion()
        # Usamos dictionary=True para que devuelva un diccionario en lugar de una tupla
        # Si usas pymysql, el parámetro puede ser cursorclass=pymysql.cursors.DictCursor
        cursor = conexion.cursor(dictionary=True) 
        
        # Ordenamos por ID o Fecha descendente para traer siempre la más reciente
        cursor.execute("SELECT * FROM tasa_cambio ORDER BY id DESC LIMIT 1")
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        return resultado

    @staticmethod
    def guardar_nueva_tasa(valor):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        fecha_actual = datetime.now().date()
        
        # Insertamos el nuevo registro para tener un historial de tasas
        cursor.execute(
            "INSERT INTO tasa_cambio (valor, fecha) VALUES (%s, %s)", 
            (valor, fecha_actual)
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()
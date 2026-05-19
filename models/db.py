import mysql.connector
from config import Config

def obtener_conexion():
    # Esta fallará si 'automall_negocio' no está creada en MySQL
    return mysql.connector.connect(**Config.DB_NEGOCIO)

def obtener_conexion_seguridad():
    # Esta es la que usa Permisos y Bitácora
    return mysql.connector.connect(**Config.DB_SEGURIDAD)
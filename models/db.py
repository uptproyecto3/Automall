import mysql.connector
from config import Config

def obtener_conexion():
    return mysql.connector.connect(**Config.DB_CONFIG)
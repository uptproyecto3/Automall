# models/catalogo.py
from models.db import obtener_conexion

class Catalogo:
    @staticmethod
    def obtener_disponibles():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT 
                v.placa, 
                v.anio, 
                v.estado,
                ma.nombre_marca, 
                mo.nombre_modelo, 
                i.URL as imagen_url, 
                c.precio, 
                c.descripcion,
                d.fecha_ingreso,
                p.razon_social as nombre_proveedor
            FROM vehiculo v
            JOIN catalogo c ON v.placa = c.placa
            JOIN modelo mo ON v.cod_modelo = mo.cod_modelo
            JOIN marca ma ON mo.cod_marca = ma.cod_marca
            JOIN documentacion d ON v.cod_documento = d.cod_documento
            JOIN proveedor p ON v.cedula_proveedor = p.cedula_proveedor
            LEFT JOIN imagen i ON v.placa = i.placa
            WHERE v.estado = 'Disponible'
            ORDER BY c.fecha_publicacion DESC
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conexion.close()
        return res
from models.db import obtener_conexion

class Catalogo:
    @staticmethod
    def obtener_disponibles():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        # Traemos datos del vehiculo + catalogo + marca + modelo + imagen
        # Filtramos solo donde el vehiculo esté 'Disponible'
        sql = """
            SELECT 
                c.cod_catalogo, c.precio, c.descripcion, c.fecha_publicacion,
                v.placa, v.color, v.anio, v.kilometraje, v.tipo,
                m.nombre_marca, mo.nombre_modelo,
                (SELECT URL FROM imagen WHERE placa = v.placa LIMIT 1) as imagen_url
            FROM catalogo c
            JOIN vehiculo v ON c.placa = v.placa
            JOIN marca m ON v.cod_marca = m.cod_marca
            JOIN modelo mo ON v.cod_modelo = mo.cod_modelo
            WHERE v.estado = 'Disponible'
            ORDER BY c.fecha_publicacion DESC
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conexion.close()
        return res
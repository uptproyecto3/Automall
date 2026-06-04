from models.db import obtener_conexion_seguridad

class seleccionar:
    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)

        sql= """
            SELECT
            v.placa,
            v.color,
            v.anio,
            c.cod_catalogo,
            m.nombre_modelo,
            ma.nombre_marca
            FROM automall.vehiculo v
            INNER JOIN automall.catalogo c ON v.placa = c.placa
            INNER JOIN automall.modelo m ON v.cod_modelo = m.cod_modelo
            INNER JOIN automall.marca ma ON v.cod_marca = ma.cod_marca
            WHERE v.estado = 'disponible'
            """

        cursor.execute(sql)
        seleccionar = cursor.fetchall()

        cursor.close()
        conexion.close()

        return seleccionar
    
    def registrar_citas(fecha, hora, cod_catalogo):
        conexion = obtener_conexion_seguridad ()
        cursor = conexion.cursor()

        sql= """
            INSERT INTO automall.citas
            (fecha, hora, cod_catalogo, estado)

            VALUES (%s, %s, %s, 'Pendiente')
            """
        
        valores = (fecha, hora, cod_catalogo)

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()
        return True


## es una prueba---------------------------------------------->
    @staticmethod
    def obtener_citas_transito():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        # 🔗 Traemos solo lo esencial de forma segura usando las llaves de tu diagrama
        sql = """
            SELECT 
                c.fecha,
                v.placa,
                m.nombre_modelo,
                ma.nombre_marca
            FROM automall.citas c
            INNER JOIN automall.catalogo cat ON c.cod_catalogo = cat.cod_catalogo
            INNER JOIN automall.vehiculo v   ON cat.placa = v.placa
            INNER JOIN automall.modelo m     ON v.cod_modelo = m.cod_modelo
            INNER JOIN automall.marca ma     ON v.cod_marca = ma.cod_marca
        """
    

        cursor.execute(sql)
        resultado = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        return resultado
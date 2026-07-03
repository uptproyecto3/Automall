from models.db import obtener_conexion_seguridad

class Bitacora:
    @staticmethod
    def registrar(cedula_usuario, cod_accion, cod_modulo):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        
        # Ajustado a tus nuevas columnas numéricas
        sql = """
            INSERT INTO t_bitacora (cedula_usuario, cod_accion, cod_modulo) 
            VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(sql, (cedula_usuario, cod_accion, cod_modulo))
            conexion.commit()
        except Exception as e:
            print(f"Error al registrar en bitácora: {e}")
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_todas():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        # Hacemos JOINs lógicos. Usamos 'AS accion' y 'AS modulo' 
        # para que el diccionario devuelva las mismas llaves que ya usa tu HTML.
        sql = """
            SELECT 
                b.fecha, 
                b.cedula_usuario, 
                a.nombre_accion AS accion,  -- Ajusta 'nombre_accion' si se llama distinto
                m.nombre_modulo AS modulo   -- Ajusta 'nombre_modulo' si se llama distinto
            FROM t_bitacora b
            LEFT JOIN t_accion a ON b.cod_accion = a.cod_accion
            LEFT JOIN t_modulo m ON b.cod_modulo = m.cod_modulo
            ORDER BY b.fecha DESC
        """
        try:
            cursor.execute(sql)
            logs = cursor.fetchall()
            return logs if logs else []
        except Exception as e:
            print(f"Error al obtener bitácora: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()
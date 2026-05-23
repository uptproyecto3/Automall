from models.db import obtener_conexion_seguridad 

class Permiso:
    @staticmethod
    def obtener_roles():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM t_rol")
        roles = cursor.fetchall()
        cursor.close()  # ¡Importante cerrar siempre el cursor antes de la conexión!
        conexion.close()
        return roles

    @staticmethod
    def obtener_por_rol(cod_rol):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        # Agregamos espacios limpios al inicio de cada línea del string multilinea
        sql = """
            SELECT rp.*, m.nombre_modulo 
            FROM t_permiso_rol_modulo rp
            JOIN t_modulo m ON rp.cod_modulo = m.cod_modulo
            WHERE rp.cod_rol = %s
        """
        cursor.execute(sql, (cod_rol,))
        permisos = cursor.fetchall()
        cursor.close()  # Cerramos el cursor
        conexion.close()
        return permisos

    @staticmethod
    def actualizar(cod_permiso, p_crear, p_leer, p_actualizar, p_eliminar):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        
        # Aseguramos espacios limpios alrededor de las palabras clave del UPDATE
        sql = """
            UPDATE t_permiso_rol_modulo 
            SET p_crear = %s, 
                p_leer = %s, 
                p_actualizar = %s, 
                p_eliminar = %s 
            WHERE cod_permiso = %s
        """
        cursor.execute(sql, (p_crear, p_leer, p_actualizar, p_eliminar, cod_permiso))
        conexion.commit()
        cursor.close()  # Cerramos el cursor para liberar el búfer del comando UPDATE
        conexion.close()
from models.db import obtener_conexion_seguridad 

class Permiso:
    @staticmethod
    def obtener_roles():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM t_rol")
        roles = cursor.fetchall()
        cursor.close()  
        conexion.close()
        return roles

    @staticmethod
    def obtener_por_rol(cod_rol):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        sql = """
            SELECT rp.*, m.nombre_modulo 
            FROM t_permiso_rol_modulo rp
            JOIN t_modulo m ON rp.cod_modulo = m.cod_modulo
            WHERE rp.cod_rol = %s
        """
        cursor.execute(sql, (cod_rol,))
        permisos = cursor.fetchall()
        cursor.close()  
        conexion.close()
        return permisos

    @staticmethod
    def actualizar(cod_permiso, p_crear, p_leer, p_actualizar, p_eliminar):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        
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
        cursor.close()  
        conexion.close()

    @staticmethod
    def verificar_acceso(cod_rol, modulo, tipo_permiso):
        """
        Verifica si un rol específico cuenta con un permiso activo para un módulo determinado.
        Regresa True si tiene acceso (1), de lo contrario False.
        """
        permisos_validos = ['p_crear', 'p_eliminar', 'p_actualizar', 'p_leer']
        
        if tipo_permiso not in permisos_validos:
            return False

        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        # Al validar contra la lista blanca, evitamos inyecciones en el identificador de columna
        sql = f"""
            SELECT rp.{tipo_permiso} as tiene_permiso 
            FROM t_permiso_rol_modulo rp 
            JOIN t_modulo m ON rp.cod_modulo = m.cod_modulo 
            WHERE rp.cod_rol = %s AND m.nombre_modulo = %s
        """ # nosec B608
        
        cursor.execute(sql, (cod_rol, modulo))
        res = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        # Evaluamos explícitamente si el registro existe y su bit/int está activo en 1
        return True if res and res['tiene_permiso'] == 1 else False
from models.db import obtener_conexion

class Permiso:
    @staticmethod
    def obtener_roles():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rol")
        roles = cursor.fetchall()
        conexion.close()
        return roles

    @staticmethod
    def obtener_por_rol(id_rol):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        # Traemos permisos solo del rol seleccionado, junto con el nombre del módulo
        sql = """SELECT rp.*, m.nombre_modulo 
                 FROM rol_permisos rp
                 JOIN modulo m ON rp.id_modulo = m.id_modulo
                 WHERE rp.id_rol = %s"""
        cursor.execute(sql, (id_rol,))
        permisos = cursor.fetchall()
        conexion.close()
        return permisos

    @staticmethod
    def actualizar(id_permiso, p_crear, p_leer, p_actualizar, p_eliminar):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """UPDATE rol_permisos 
                 SET p_crear=%s, p_leer=%s, p_actualizar=%s, p_eliminar=%s 
                 WHERE id_permiso=%s"""
        cursor.execute(sql, (p_crear, p_leer, p_actualizar, p_eliminar, id_permiso))
        conexion.commit()
        conexion.close()
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
    def obtener_matriz_permisos(cod_rol):
        """
        Trae TODAS las combinaciones de módulo-acción registradas en t_permiso,
        marcando con un '1' (activo) si el rol seleccionado cuenta con ese permiso,
        o con un '0' si no lo tiene. Ideal para renderizar la tabla de asignación.
        """
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        sql = """
            SELECT 
                p.cod_permiso,
                m.cod_modulo,
                m.nombre_modulo,
                a.cod_accion,
                a.nom_accion,
                IF(rp.cod_rol IS NOT NULL, 1, 0) AS activo
            FROM t_permiso p
            INNER JOIN t_modulo m ON p.cod_modulo = m.cod_modulo
            INNER JOIN t_acciones a ON p.cod_accion = a.cod_accion
            LEFT JOIN t_rol_permiso rp ON p.cod_permiso = rp.cod_permiso AND rp.cod_rol = %s
            ORDER BY m.cod_modulo, a.cod_accion
        """
        try:
            cursor.execute(sql, (cod_rol,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener matriz de permisos: {e}")
            return []
        finally:
            cursor.close()  
            conexion.close()

    @staticmethod
    def sincronizar_permisos(cod_rol, lista_cod_permisos):
        """
        Estrategia limpia para base de datos normalizada:
        Limpia las asignaciones previas del rol e inserta el nuevo lote seleccionado.
        """
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        try:
            # 1. Eliminar asignaciones viejas de este rol específico
            cursor.execute("DELETE FROM t_rol_permiso WHERE cod_rol = %s", (cod_rol,))
            
            # 2. Si marcaron casillas, insertarlas en lote (Bulk Insert)
            if lista_cod_permisos:
                sql_insert = "INSERT INTO t_rol_permiso (cod_rol, cod_permiso) VALUES (%s, %s)"
                # Preparamos las tuplas mapeando cada cod_permiso a entero
                datos_lote = [(cod_rol, int(cod_p)) for cod_p in lista_cod_permisos]
                cursor.executemany(sql_insert, datos_lote)
                
            conexion.commit()
            return {"status": True}
        except Exception as e:
            conexion.rollback()
            print(f"Error crítico al sincronizar los permisos del rol {cod_rol}: {e}")
            return {"status": False, "error": str(e)}
        finally:
            cursor.close()  
            conexion.close()

    @staticmethod
    def verificar_acceso(cod_rol, modulo, tipo_permiso):
        """
        Verifica mediante JOIN si el rol actual posee la relación activa
        para el módulo y la acción solicitada.
        """
        # Mapeo preventivo para no romper tus decoradores ya declarados en el resto de la app
        mapeo_acciones = {
            'p_crear': 'CREAR',
            'p_leer': 'LEER',
            'p_actualizar': 'ACTUALIZAR',
            'p_eliminar': 'ELIMINAR'
        }
        
        accion_real = mapeo_acciones.get(tipo_permiso)
        if not accion_real:
            return False

        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        sql = """
            SELECT COUNT(*) AS autorizado
            FROM t_rol_permiso rp
            INNER JOIN t_permiso p ON rp.cod_permiso = p.cod_permiso
            INNER JOIN t_modulo m ON p.cod_modulo = m.cod_modulo
            INNER JOIN t_acciones a ON p.cod_accion = a.cod_accion
            WHERE rp.cod_rol = %s AND m.nombre_modulo = %s AND a.nom_accion = %s
        """
        try:
            cursor.execute(sql, (cod_rol, modulo, accion_real))
            res = cursor.fetchone()
            return True if res and res['autorizado'] > 0 else False
        except Exception as e:
            print(f"Error en la verificación de seguridad relacional: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
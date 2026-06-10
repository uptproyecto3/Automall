from models.db import obtener_conexion


class Servicios:
    def __init__(self, cod_servicios=None, nombre_servicio=None, estado=None):
        self.cod_servicios = cod_servicios
        self.nombre_servicio = nombre_servicio
        self.estado = estado

    @staticmethod
    def obtener_servicios():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                sr.cod_servicios,
                sr.nombre_servicio,
                sr.estado,
                ds.cod_det_servicio,
                ds.costo,
                ds.descripcion_especifica,
                ds.placa,
                v.estado AS estado_vehiculo
            FROM servicios_realizados sr
            LEFT JOIN det_servicios ds ON ds.cod_det_servicio = sr.cod_det_servicio
            LEFT JOIN vehiculo v ON v.placa = ds.placa
            ORDER BY sr.cod_servicios DESC
        """)
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    @staticmethod
    def obtener_vehiculos_disponibles():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT placa, estado
            FROM vehiculo
            WHERE estado IN ('Disponible', 'Servicio')
            ORDER BY placa ASC
        """)
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    @staticmethod
    def guardar(nombre_servicio, costo, descripcion_especifica, placa):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            conexion.autocommit = False

            cursor.execute("""
                INSERT INTO det_servicios (costo, descripcion_especifica, placa)
                VALUES (%s, %s, %s)
            """, (costo, descripcion_especifica, placa))

            cod_det_servicio = cursor.lastrowid

            cursor.execute("""
                INSERT INTO servicios_realizados (nombre_servicio, estado, cod_det_servicio)
                VALUES (%s, %s, %s)
            """, (nombre_servicio, 'Activo', cod_det_servicio))

            cursor.execute("""
                UPDATE vehiculo
                SET estado = 'Servicio'
                WHERE placa = %s
            """, (placa,))

            conexion.commit()
            return True

        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(cod_servicios, nombre_servicio, costo, descripcion_especifica, placa):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            conexion.autocommit = False

            cursor.execute("""
                SELECT ds.placa
                FROM servicios_realizados sr
                JOIN det_servicios ds ON ds.cod_det_servicio = sr.cod_det_servicio
                WHERE sr.cod_servicios = %s
            """, (cod_servicios,))
            actual = cursor.fetchone()
            placa_anterior = actual[0] if actual else None

            cursor.execute("""
                UPDATE servicios_realizados
                SET nombre_servicio = %s
                WHERE cod_servicios = %s
            """, (nombre_servicio, cod_servicios))

            cursor.execute("""
                UPDATE det_servicios ds
                JOIN servicios_realizados sr ON sr.cod_det_servicio = ds.cod_det_servicio
                SET ds.costo = %s,
                    ds.descripcion_especifica = %s,
                    ds.placa = %s
                WHERE sr.cod_servicios = %s
            """, (costo, descripcion_especifica, placa, cod_servicios))

            if placa_anterior and placa_anterior != placa:
                cursor.execute("UPDATE vehiculo SET estado = 'Disponible' WHERE placa = %s", (placa_anterior,))
                cursor.execute("UPDATE vehiculo SET estado = 'Servicio' WHERE placa = %s", (placa,))

            conexion.commit()
            return True

        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def inactivar(cod_servicios):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            conexion.autocommit = False

            cursor.execute("""
                UPDATE servicios_realizados
                SET estado = 'Inactivo'
                WHERE cod_servicios = %s
            """, (cod_servicios,))

            conexion.commit()
            return True

        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def finalizar(cod_servicios, placa):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            conexion.autocommit = False

            cursor.execute("""
                UPDATE servicios_realizados
                SET estado = 'Finalizado'
                WHERE cod_servicios = %s
            """, (cod_servicios,))

            cursor.execute("""
                UPDATE vehiculo
                SET estado = 'Disponible'
                WHERE placa = %s
            """, (placa,))

            conexion.commit()
            return True

        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_vehiculos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT placa
            FROM vehiculo
            ORDER BY placa ASC
        """)
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    @staticmethod
    def filtrar_reporte(cod_servicio, nombre_servicio, estado, placa):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                sr.cod_servicios,
                sr.nombre_servicio,
                sr.estado,
                ds.cod_det_servicio,
                ds.costo,
                ds.descripcion_especifica,
                ds.placa,
                v.estado AS estado_vehiculo
            FROM servicios_realizados sr
            LEFT JOIN det_servicios ds ON ds.cod_det_servicio = sr.cod_det_servicio
            LEFT JOIN vehiculo v ON v.placa = ds.placa
            WHERE (%s = '' OR sr.cod_servicios = %s)
              AND (%s = '' OR sr.nombre_servicio LIKE %s)
              AND (%s = '' OR sr.estado = %s)
              AND (%s = '' OR ds.placa = %s)
            ORDER BY sr.cod_servicios DESC
        """, (
            cod_servicio, cod_servicio,
            nombre_servicio, f"%{nombre_servicio}%",
            estado, estado,
            placa, placa
        ))
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    @staticmethod
    def obtener_servicio_por_codigo(cod_servicios):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                sr.cod_servicios,
                sr.nombre_servicio,
                sr.estado,
                ds.cod_det_servicio,
                ds.costo,
                ds.descripcion_especifica,
                ds.placa,
                v.estado AS estado_vehiculo
            FROM servicios_realizados sr
            LEFT JOIN det_servicios ds ON ds.cod_det_servicio = sr.cod_det_servicio
            LEFT JOIN vehiculo v ON v.placa = ds.placa
            WHERE sr.cod_servicios = %s
            LIMIT 1
        """, (cod_servicios,))
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fila
from models.db import obtener_conexion


class MantenimientoOperacional:
    def __init__(self, cod_mantenimiento=None, descripcion_general=None, quien_autoriza=None, estado=None):
        self.cod_mantenimiento = cod_mantenimiento
        self.descripcion_general = descripcion_general
        self.quien_autoriza = quien_autoriza
        self.estado = estado

    @staticmethod
    def obtener_mantenimientos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                m.cod_mantenimiento,
                m.descripcion_general,
                m.quien_autoriza,
                m.estado,
                dm.cod_detalle,
                dm.tipo,
                dm.fecha_salida,
                dm.fecha_entrega,
                dm.placa,
                dm.cod_taller,
                t.nombre_taller
            FROM mantenimiento m
            LEFT JOIN det_mantenimiento dm ON dm.cod_mantenimiento = m.cod_mantenimiento
            LEFT JOIN taller t ON t.cod_taller = dm.cod_taller
            ORDER BY m.cod_mantenimiento DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conexion.close()
        return rows

    @staticmethod
    def obtener_talleres():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT cod_taller, nombre_taller
            FROM taller
            WHERE estado = '1'
            ORDER BY nombre_taller ASC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conexion.close()
        return rows

    @staticmethod
    def obtener_proveedores():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT cedula_proveedor, razon_social
            FROM proveedor
            WHERE estado = 'Activo' OR estado = '1'
            ORDER BY razon_social ASC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conexion.close()
        return rows

    @staticmethod
    def obtener_vehiculos_disponibles():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT placa, estado
            FROM vehiculo
            WHERE estado IN ('Disponible', 'Mantenimiento')
            ORDER BY placa ASC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conexion.close()
        return rows

    @staticmethod
    def guardar(descripcion_general, quien_autoriza, tipo, fecha_salida, fecha_entrega, placa, cod_taller):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            conexion.autocommit = False

            cursor.execute("""
                INSERT INTO mantenimiento (descripcion_general, quien_autoriza, estado)
                VALUES (%s, %s, %s)
            """, (descripcion_general, quien_autoriza, 'Activo'))

            cod_mantenimiento = cursor.lastrowid

            cursor.execute("""
                INSERT INTO det_mantenimiento (tipo, fecha_salida, fecha_entrega, cod_mantenimiento, placa, cod_taller)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (tipo, fecha_salida, fecha_entrega, cod_mantenimiento, placa, cod_taller))

            cursor.execute("""
                UPDATE vehiculo
                SET estado = 'Mantenimiento'
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
    def actualizar(cod_mantenimiento, descripcion_general, quien_autoriza, tipo, fecha_salida, fecha_entrega, placa, cod_taller):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            conexion.autocommit = False

            cursor.execute("""
                UPDATE mantenimiento
                SET descripcion_general = %s,
                    quien_autoriza = %s
                WHERE cod_mantenimiento = %s
            """, (descripcion_general, quien_autoriza, cod_mantenimiento))

            cursor.execute("""
                UPDATE det_mantenimiento
                SET tipo = %s,
                    fecha_salida = %s,
                    fecha_entrega = %s,
                    placa = %s,
                    cod_taller = %s
                WHERE cod_mantenimiento = %s
            """, (tipo, fecha_salida, fecha_entrega, placa, cod_taller, cod_mantenimiento))

            cursor.execute("""
                UPDATE vehiculo
                SET estado = 'Mantenimiento'
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
    def inactivar(cod_mantenimiento):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            conexion.autocommit = False

            cursor.execute("""
                UPDATE mantenimiento
                SET estado = 'Inactivo'
                WHERE cod_mantenimiento = %s
            """, (cod_mantenimiento,))

            conexion.commit()
            return True

        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def finalizar(cod_mantenimiento, placa):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            conexion.autocommit = False

            cursor.execute("""
                UPDATE mantenimiento
                SET estado = 'Finalizado'
                WHERE cod_mantenimiento = %s
            """, (cod_mantenimiento,))

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
    def filtrar_reporte(cod_mantenimiento=None, placa=None, estado=None, cod_taller=None, fecha_inicio=None, fecha_fin=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            consulta = """
                SELECT
                    m.cod_mantenimiento,
                    m.descripcion_general,
                    m.quien_autoriza,
                    m.estado,
                    dm.tipo,
                    dm.fecha_salida,
                    dm.fecha_entrega,
                    dm.placa,
                    dm.cod_taller,
                    t.nombre_taller
                FROM mantenimiento m
                LEFT JOIN det_mantenimiento dm ON dm.cod_mantenimiento = m.cod_mantenimiento
                LEFT JOIN taller t ON t.cod_taller = dm.cod_taller
                WHERE 1 = 1
            """
            parametros = []

            if cod_mantenimiento:
                consulta += " AND m.cod_mantenimiento = %s"
                parametros.append(cod_mantenimiento)

            if placa:
                consulta += " AND dm.placa = %s"
                parametros.append(placa)

            if estado:
                consulta += " AND m.estado = %s"
                parametros.append(estado)

            if cod_taller:
                consulta += " AND dm.cod_taller = %s"
                parametros.append(cod_taller)

            if fecha_inicio and fecha_fin:
                consulta += " AND dm.fecha_salida BETWEEN %s AND %s"
                parametros.extend([fecha_inicio, fecha_fin])
            elif fecha_inicio:
                consulta += " AND dm.fecha_salida >= %s"
                parametros.append(fecha_inicio)
            elif fecha_fin:
                consulta += " AND dm.fecha_salida <= %s"
                parametros.append(fecha_fin)

            consulta += " ORDER BY m.cod_mantenimiento DESC"

            cursor.execute(consulta, tuple(parametros))
            rows = cursor.fetchall()
            return rows

        finally:
            cursor.close()
            conexion.close()
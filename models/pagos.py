from models.db import obtener_conexion

class Pagos:
    @staticmethod
    def obtener_todos(cedula_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        sql = """
            SELECT 
                pc.cod_pagos,
                pc.monto_abonado,
                pc.fecha_pago,
                dv.placa,
                cxc.estado AS estado_cuenta,
                cxc.deuda_total,
                cxc.saldo_pendiente,
                cxc.fecha_vencimiento,
                dp.tipo_pago,
                dp.descripcion,
                dp.fecha_det_pago,
                mp.nombre_metodo,
                m.nombre_moneda,
                m.simbolo,
                -- Traemos referencia y monto de banco o digital según existan
                COALESCE(db.refencia, dnd.refencia) AS referencia,
                COALESCE(db.monto, dnd.monto) AS monto_detalle,
                b.nombre_banco
            FROM pago_cuentas pc
            INNER JOIN cuentas_por_cobrar cxc ON pc.cod_cuentas = cxc.cod_cuentas
            INNER JOIN ventas v ON cxc.cod_venta = v.cod_venta
            INNER JOIN det_venta dv ON v.cod_venta = dv.cod_venta
            INNER JOIN det_pago dp ON pc.cod_pagos = dp.cod_pagos
            INNER JOIN metodo_pago mp ON dp.cod_metodo = mp.cod_metodo
            INNER JOIN moneda m ON dp.cod_moneda = m.cod_moneda
            LEFT JOIN det_banco db ON dp.cod_det_pago = db.cod_det_pago
            LEFT JOIN banco b ON db.cod_banco = b.cod_banco
            LEFT JOIN det_nom_digital dnd ON dp.cod_det_pago = dnd.cod_det_pago
            WHERE v.cedula_usuario = %s
            ORDER BY pc.fecha_pago DESC
        """
        try:
            cursor.execute(sql, (cedula_usuario,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener pagos: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

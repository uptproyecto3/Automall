from models.db import obtener_conexion

class Ventas:
    def __init__(self, data):
        self.cedula_cliente = data.get('cedula_cliente')
        self.placa = data.get('placa')
        self.tipo_venta = data.get('tipo_venta') # 'contado' o 'credito'
        self.poder = 1 if data.get('poder') else 0
        self.traspaso_papel = 1 if data.get('traspaso_papel') else 0
        self.monto_recibido = float(data.get('monto_recibido', 0))
        self.precio_total = float(data.get('precio_vehiculo', 0))
        self.deuda_pendiente = float(data.get('deuda_pendiente', 0))
        self.fecha_vencimiento = data.get('fecha_vencimiento')
        
        # Datos del Pago
        self.cod_metodo = data.get('cod_metodo')
        self.cod_moneda = data.get('cod_moneda')
        self.cod_banco = data.get('cod_banco')
        self.refencia = data.get('refencia', '')

    @staticmethod
    def obtener_bancos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM banco")
        bancos = cursor.fetchall()
        conexion.close()
        return bancos
    
    @staticmethod
    def obtener_metodos_pago():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM metodo_pago")
        metodos = cursor.fetchall()
        conexion.close()
        return metodos
    
    @staticmethod
    def obtener_monedas():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM moneda")
        monedas = cursor.fetchall()
        conexion.close()
        return monedas
    
    @staticmethod
    def obtener_moneda_digital():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM moneda_digital")
        monedas_digitales = cursor.fetchall()
        conexion.close()
        return monedas_digitales

    def registrar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # --- 1. REGISTRAR EN VENTAS ---
            sql_venta = """
                INSERT INTO ventas (estado, fecha_venta, tipo_venta, cedula_usuario)
                VALUES (%s, CURDATE(), %s, %s)
            """
            cursor.execute(sql_venta, ('procesada', self.tipo_venta, self.cedula_cliente))
            cod_venta = cursor.lastrowid  # Aquí obtiene el ID generado automáticamente

            # --- 2. REGISTRAR EN DET_VENTA ---
            sql_det_venta = """
                INSERT INTO det_venta (poder, traspaso_papel, placa, cod_venta)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_det_venta, (self.poder, self.traspaso_papel, self.placa, cod_venta))

            # --- 3. REGISTRAR EN CUENTAS_POR_COBRAR ---
            estado_cuenta = 'pagado' if self.deuda_pendiente <= 0 else 'pendiente'
            sql_cxc = """
                INSERT INTO cuentas_por_cobrar (deuda_total, saldo_pendiente, fecha_vencimiento, estado, cod_venta)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_cxc, (self.precio_total, self.deuda_pendiente, self.fecha_vencimiento, estado_cuenta, cod_venta))
            cod_cuentas = cursor.lastrowid

            # --- 4. REGISTRAR EN PAGO_CUENTAS ---
            if self.monto_recibido > 0:
                sql_pago_c = "INSERT INTO pago_cuentas (monto_abonado, fecha_pago, cod_cuentas) VALUES (%s, NOW(), %s)"
                cursor.execute(sql_pago_c, (self.monto_recibido, cod_cuentas))
                cod_pagos = cursor.lastrowid

                # --- 5. REGISTRAR EN DET_PAGO ---
                sql_det_pago = """
                    INSERT INTO det_pago (tipo_pago, fecha_det_pago, descripcion, cod_pagos, cod_moneda, cod_metodo)
                    VALUES (%s, NOW(), %s, %s, %s, %s)
                """
                desc = f"Pago inicial - Venta {self.tipo_venta}"
                cursor.execute(sql_det_pago, (self.tipo_venta, desc, cod_pagos, self.cod_moneda, self.cod_metodo))
                cod_det_pago = cursor.lastrowid # ID generado para el detalle del pago

                # --- 6. REGISTRAR EN DET_BANCO o MONEDA_DIGITAL ---
                metodos_digitales = ['5', '6', '7'] 
                
                if str(self.cod_metodo) in metodos_digitales:
                    sql_digital = """
                        INSERT INTO det_nom_digital (monto, refencia, cod_mon_digital, cod_det_pago) 
                        VALUES (%s, %s, %s, %s)
                    """
                    # CORRECCIÓN: Usar cod_det_pago (la variable local), no self.cod_det_pago
                    cursor.execute(sql_digital, (self.monto_recibido, self.refencia, self.cod_mon_digital, cod_det_pago))
                else:
                    sql_banco = """
                        INSERT INTO det_banco (monto, refencia, cod_banco, cod_det_pago) 
                        VALUES (%s, %s, %s, %s)
                    """
                    # CORRECCIÓN: Usar cod_det_pago (la variable local)
                    cursor.execute(sql_banco, (self.monto_recibido, self.refencia, self.cod_banco, cod_det_pago))

            # --- 7. ACTUALIZAR ESTADO DEL VEHÍCULO ---
            cursor.execute("UPDATE vehiculo SET estado = 'Vendido' WHERE placa = %s", (self.placa,))

            conexion.commit()
            return {"status": True}

        except Exception as e:
            conexion.rollback()
            print(f"ERROR TRANSACCIONAL: {str(e)}")
            return {"status": False, "error": str(e)}
        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def obtener_todas():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True) # Usamos dictionary=True para manejar nombres de columnas
        
        sql = """
            SELECT 
                v.cod_venta,
                v.fecha_venta,
                v.estado AS estado_venta,
                v.tipo_venta,
                v.cedula_usuario,
                dv.placa,
                cxc.deuda_total,
                cxc.saldo_pendiente,
                cxc.estado AS estado_cuenta,
                pc.monto_abonado,
                pc.fecha_pago
            FROM ventas v
            INNER JOIN det_venta dv ON v.cod_venta = dv.cod_venta
            INNER JOIN cuentas_por_cobrar cxc ON v.cod_venta = cxc.cod_venta
            LEFT JOIN pago_cuentas pc ON cxc.cod_cuentas = pc.cod_cuentas
            GROUP BY v.cod_venta
            ORDER BY v.fecha_venta DESC
        """
        # Nota: Usamos GROUP BY para evitar duplicados si hay varios pagos, 
        # aunque lo ideal para un listado detallado sería una subconsulta.
        
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al listar ventas: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()
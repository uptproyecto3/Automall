from models.db import obtener_conexion

class Ventas:
    def __init__(self, data):
        # ATRIBUTOS PRIVADOS (Encapsulamiento estricto)
        self.__cedula_cliente = data.get('cedula_cliente')
        self.__placa = data.get('placa')
        self.__tipo_venta = data.get('tipo_venta')  # contado o credito
        self.__poder = 1 if data.get('poder') else 0
        self.__traspaso_papel = 1 if data.get('traspaso_papel') else 0
        self.__monto_recibido = float(data.get('monto_recibido', 0))
        self.__precio_total = float(data.get('precio_vehiculo', 0))
        self.__deuda_pendiente = float(data.get('deuda_pendiente', 0))
        self.__fecha_vencimiento = data.get('fecha_vencimiento')
        
        # Datos del Pago
        self.__cod_metodo = data.get('cod_metodo')
        self.__cod_moneda = data.get('cod_moneda')
        self.__cod_banco = data.get('cod_banco')
        self.__cod_mon_digital = data.get('cod_mon_digital')  
        self.__refencia = data.get('refencia', '')

    # =========================================================================
    # GETTERS (Propiedades de Solo Lectura para el exterior)
    # =========================================================================
    @property
    def cedula_cliente(self): return self.__cedula_cliente

    @property
    def placa(self): return self.__placa

    @property
    def tipo_venta(self): return self.__tipo_venta

    @property
    def poder(self): return self.__poder

    @property
    def traspaso_papel(self): return self.__traspaso_papel

    @property
    def monto_recibido(self): return self.__monto_recibido

    @property
    def precio_total(self): return self.__precio_total

    @property
    def deuda_pendiente(self): return self.__deuda_pendiente

    @property
    def fecha_vencimiento(self): return self.__fecha_vencimiento

    @property
    def cod_metodo(self): return self.__cod_metodo

    @property
    def cod_moneda(self): return self.__cod_moneda

    @property
    def cod_banco(self): return self.__cod_banco

    @property
    def cod_mon_digital(self): return self.__cod_mon_digital

    @property
    def refencia(self): return self.__refencia

    # =========================================================================
    # MÉTODOS ESTÁTICOS (Catálogos globales)
    # =========================================================================
    @staticmethod
    def obtener_bancos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM banco")
        bancos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return bancos
    
    @staticmethod
    def obtener_metodos_pago():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM metodo_pago")
        metodos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return metodos
    
    @staticmethod
    def obtener_monedas():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM moneda")
        monedas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return monedas
    
    @staticmethod
    def obtener_moneda_digital():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM moneda_digital")
        monedas_digitales = cursor.fetchall()
        cursor.close()
        conexion.close()
        return monedas_digitales

    # =========================================================================
    # LÓGICA DE NEGOCIO (Métodos de Instancia)
    # =========================================================================
    def registrar(self):
        # --- BARRERA DE VALIDACIÓN DEL BACKEND ---
        from utils.validaciones_ventas import validar_registro_venta
        verificacion = validar_registro_venta(self) # Le pasamos el propio objeto
        
        if not verificacion["status"]:
            return verificacion # Rompe el flujo de inmediato y devuelve el diccionario con el error
            
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # --- 1. REGISTRAR EN VENTAS ---
            sql_venta = """
                INSERT INTO ventas (estado, fecha_venta, tipo_venta, cedula_usuario)
                VALUES (%s, CURDATE(), %s, %s)
            """
            cursor.execute(sql_venta, ('procesada', self.__tipo_venta, self.__cedula_cliente))
            cod_venta = cursor.lastrowid  

            # --- 2. REGISTRAR EN DET_VENTA ---
            sql_det_venta = """
                INSERT INTO det_venta (poder, traspaso_papel, placa, cod_venta)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_det_venta, (self.__poder, self.__traspaso_papel, self.__placa, cod_venta))

            # --- 3. REGISTRAR EN CUENTAS_POR_COBRAR ---
            estado_cuenta = 'pagado' if self.__deuda_pendiente <= 0 else 'pendiente'
            sql_cxc = """
                INSERT INTO cuentas_por_cobrar (deuda_total, saldo_pendiente, fecha_vencimiento, estado, cod_venta)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_cxc, (self.__precio_total, self.__deuda_pendiente, self.__fecha_vencimiento, estado_cuenta, cod_venta))
            cod_cuentas = cursor.lastrowid

            # --- 4. REGISTRAR EN PAGO_CUENTAS ---
            if self.__monto_recibido > 0:
                sql_pago_c = "INSERT INTO pago_cuentas (monto_abonado, fecha_pago, cod_cuentas) VALUES (%s, NOW(), %s)"
                cursor.execute(sql_pago_c, (self.__monto_recibido, cod_cuentas))
                cod_pagos = cursor.lastrowid

                # --- 5. REGISTRAR EN DET_PAGO ---
                sql_det_pago = """
                    INSERT INTO det_pago (tipo_pago, fecha_det_pago, descripcion, cod_pagos, cod_moneda, cod_metodo)
                    VALUES (%s, NOW(), %s, %s, %s, %s)
                """
                desc = f"Pago inicial - Venta {self.__tipo_venta}"
                cursor.execute(sql_det_pago, (self.__tipo_venta, desc, cod_pagos, self.__cod_moneda, self.__cod_metodo))
                cod_det_pago = cursor.lastrowid

                # --- 6. REGISTRAR EN DET_BANCO o MONEDA_DIGITAL ---
                metodos_digitales = ['5', '6', '7'] 
                
                if str(self.__cod_metodo) in metodos_digitales:
                    sql_digital = """
                        INSERT INTO det_nom_digital (monto, refencia, cod_mon_digital, cod_det_pago) 
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(sql_digital, (self.__monto_recibido, self.__refencia, self.__cod_mon_digital, cod_det_pago))
                else:
                    sql_banco = """
                        INSERT INTO det_banco (monto, refencia, cod_banco, cod_det_pago) 
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(sql_banco, (self.__monto_recibido, self.__refencia, self.__cod_banco, cod_det_pago))

            # --- 7. ACTUALIZAR ESTADO DEL VEHÍCULO ---
            cursor.execute("UPDATE vehiculo SET estado = 'Vendido' WHERE placa = %s", (self.__placa,))

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
        cursor = conexion.cursor(dictionary=True)
        
        sql = """
            SELECT 
                v.cod_venta, v.fecha_venta, v.estado AS estado_venta, v.tipo_venta, v.cedula_usuario,
                dv.placa, cxc.deuda_total, cxc.saldo_pendiente, cxc.estado AS estado_cuenta,
                pc.monto_abonado, pc.fecha_pago
            FROM ventas v
            INNER JOIN det_venta dv ON v.cod_venta = dv.cod_venta
            INNER JOIN cuentas_por_cobrar cxc ON v.cod_venta = cxc.cod_venta
            LEFT JOIN pago_cuentas pc ON cxc.cod_cuentas = pc.cod_cuentas
            GROUP BY v.cod_venta
            ORDER BY v.fecha_venta DESC
        """
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al listar ventas: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(cod_venta):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT placa FROM det_venta WHERE cod_venta = %s", (cod_venta,))
            res = cursor.fetchone()
            
            if res:
                placa = res['placa']
                cursor.execute("UPDATE vehiculo SET estado = 'Disponible' WHERE placa = %s", (placa,))

            cursor.execute("DELETE FROM pago_cuentas WHERE cod_cuentas IN (SELECT cod_cuentas FROM cuentas_por_cobrar WHERE cod_venta = %s)", (cod_venta,))
            cursor.execute("DELETE FROM cuentas_por_cobrar WHERE cod_venta = %s", (cod_venta,))
            cursor.execute("DELETE FROM det_venta WHERE cod_venta = %s", (cod_venta,))
            cursor.execute("DELETE FROM ventas WHERE cod_venta = %s", (cod_venta,))

            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            print(f"Error al eliminar venta: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(data):
        # --- BARRERA DE VALIDACIÓN DEL BACKEND (ESTÁTICA) ---
        from utils.validaciones_ventas import validar_actualizacion_venta
        verificacion = validar_actualizacion_venta(data)
        
        if not verificacion["status"]:
            return verificacion # Retorna el dict con el error al controlador
            
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                UPDATE ventas SET tipo_venta = %s, cedula_usuario = %s 
                WHERE cod_venta = %s
            """, (data['tipo_venta'], data['cedula_cliente'], data['cod_venta']))

            cursor.execute("""
                UPDATE cuentas_por_cobrar SET deuda_total = %s, fecha_vencimiento = %s
                WHERE cod_venta = %s
            """, (data['deuda_total'], data['fecha_vencimiento'], data['cod_venta']))

            conexion.commit()
            return {"status": True}
        except Exception as e:
            conexion.rollback()
            print(f"Error al editar venta: {e}")
            return {"status": False, "error": str(e)}
        finally:
            cursor.close()
            conexion.close()
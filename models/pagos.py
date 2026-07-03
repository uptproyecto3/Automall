from models.db import obtener_conexion, obtener_conexion_seguridad

class Pagos:
    def __init__(self, data=None):
        # ATRIBUTOS PRIVADOS (Solo se llenan si se pasa data para registrar/actualizar)
        if data:
            self.__cod_pagos = data.get('cod_pagos')
            self.__monto_pago = float(data.get('monto_pago', 0)) if data.get('monto_pago') else float(data.get('monto_abonado', 0))
            self.__cod_cuentas = data.get('cod_cuentas')
            self.__descripcion = data.get('descripcion', '')
            self.__cod_moneda = data.get('cod_moneda')
            self.__cod_metodo = data.get('cod_metodo')
            self.__referencia = data.get('referencia', data.get('refencia', ''))
            self.__cod_banco = data.get('cod_banco')
            self.__cod_mon_digital = data.get('cod_mon_digital')
            self.__saldo_actual = float(data.get('saldo_actual', 0))
        else:
            self.__cod_pagos = None
            self.__monto_pago = 0.0
            self.__cod_cuentas = None
            self.__descripcion = ''
            self.__cod_moneda = None
            self.__cod_metodo = None
            self.__referencia = ''
            self.__cod_banco = None
            self.__cod_mon_digital = None
            self.__saldo_actual = 0.0

    # =========================================================================
    # GETTERS (Propiedades de Solo Lectura)
    # =========================================================================
    @property
    def cod_pagos(self): return self.__cod_pagos
    @property
    def monto_pago(self): return self.__monto_pago
    @property
    def cod_cuentas(self): return self.__cod_cuentas
    @property
    def descripcion(self): return self.__descripcion
    @property
    def cod_moneda(self): return self.__cod_moneda
    @property
    def cod_metodo(self): return self.__cod_metodo
    @property
    def referencia(self): return self.__referencia
    @property
    def cod_banco(self): return self.__cod_banco
    @property
    def cod_mon_digital(self): return self.__cod_mon_digital
    @property
    def saldo_actual(self): return self.__saldo_actual

    # =========================================================================
    # MÉTODOS DE INSTANCIA (Lógica de Negocio Encapsulada)
    # =========================================================================
    
    def procesar_abono(self):  
        # --- BARRERA DE VALIDACIÓN DEL BACKEND ---
        from utils.validaciones_pagos import validar_abono_pago
        verificacion = validar_abono_pago(self)
        
        if not verificacion["status"]:
            return verificacion  # Frena la ejecución si la validación falla
            
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # 1. Registrar en pago_cuentas
            sql_pago = "INSERT INTO pago_cuentas (monto_abonado, fecha_pago, cod_cuentas) VALUES (%s, NOW(), %s)"
            cursor.execute(sql_pago, (self.__monto_pago, self.__cod_cuentas))
            cod_pagos_generado = cursor.lastrowid

            # 2. Registrar en det_pago
            sql_det = """
                INSERT INTO det_pago (tipo_pago, fecha_det_pago, descripcion, cod_pagos, cod_moneda, cod_metodo)
                VALUES (%s, NOW(), %s, %s, %s, %s)
            """
            cursor.execute(sql_det, ('abono', self.__descripcion, cod_pagos_generado, self.__cod_moneda, self.__cod_metodo))
            cod_det_pago = cursor.lastrowid

            # 3. Registrar en det_banco o det_nom_digital
            metodos_digitales = ['5', '6', '7']
            if str(self.__cod_metodo) in metodos_digitales:
                sql_dig = "INSERT INTO det_nom_digital (monto, refencia, cod_mon_digital, cod_det_pago) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_dig, (self.__monto_pago, self.__referencia, self.__cod_mon_digital, cod_det_pago))
            else:
                sql_ban = "INSERT INTO det_banco (monto, refencia, cod_banco, cod_det_pago) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_ban, (self.__monto_pago, self.__referencia, self.__cod_banco, cod_det_pago))

            # 4. Actualizar cuentas_por_cobrar
            nuevo_saldo = self.__saldo_actual - self.__monto_pago
            nuevo_estado = 'pagado' if nuevo_saldo <= 0 else 'pendiente'
            
            sql_update = "UPDATE cuentas_por_cobrar SET saldo_pendiente = %s, estado = %s WHERE cod_cuentas = %s"
            cursor.execute(sql_update, (max(0, nuevo_saldo), nuevo_estado, self.__cod_cuentas))

            conexion.commit()
            return {"status": True}
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error detectado en el modelo de abonos: {e}")
            return {"status": False, "error": str(e)}
            
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def actualizar(self):  
        # --- BARRERA DE VALIDACIÓN DEL BACKEND ---
        from utils.validaciones_pagos import validar_actualizacion_pago
        verificacion = validar_actualizacion_pago(self)
        
        if not verificacion["status"]:
            return verificacion
            
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            # 1. Obtener monto anterior para ajustar el saldo
            cursor.execute("SELECT monto_abonado, cod_cuentas FROM pago_cuentas WHERE cod_pagos = %s", (self.__cod_pagos,))
            pago_antiguo = cursor.fetchone()
            
            if not pago_antiguo:
                return {"status": False, "error": "El registro de pago original no existe."}
                
            # 2. Calcular diferencia de saldo
            diferencia = float(pago_antiguo['monto_abonado']) - self.__monto_pago
            
            cursor.execute("""
                UPDATE cuentas_por_cobrar 
                SET saldo_pendiente = saldo_pendiente + %s
                WHERE cod_cuentas = %s
            """, (diferencia, pago_antiguo['cod_cuentas']))

            # 3. Actualizar pago_cuentas
            cursor.execute("UPDATE pago_cuentas SET monto_abonado = %s WHERE cod_pagos = %s", 
                           (self.__monto_pago, self.__cod_pagos))

            # 4. Actualizar det_pago
            cursor.execute("""
                UPDATE det_pago SET descripcion = %s, cod_metodo = %s, cod_moneda = %s 
                WHERE cod_pagos = %s
            """, (self.__descripcion, self.__cod_metodo, self.__cod_moneda, self.__cod_pagos))

            # 5. Actualizar det_banco o digital dinámicamente
            metodos_digitales = ['5', '6', '7']
            if str(self.__cod_metodo) in metodos_digitales:
                sql_ref = """
                    UPDATE det_nom_digital 
                    SET refencia = %s 
                    WHERE cod_det_pago = (SELECT cod_det_pago FROM det_pago WHERE cod_pagos = %s)
                """
            else:
                sql_ref = """
                    UPDATE det_banco 
                    SET refencia = %s 
                    WHERE cod_det_pago = (SELECT cod_det_pago FROM det_pago WHERE cod_pagos = %s)
                """
            cursor.execute(sql_ref, (self.__referencia, self.__cod_pagos))

            conexion.commit()
            return {"status": True}
        except Exception as e:
            conexion.rollback()
            print(f"Error al editar pago: {e}")
            return {"status": False, "error": str(e)}
        finally:
            cursor.close()
            conexion.close()

    # =========================================================================
    # MÉTODOS ESTÁTICOS (Permanecen intactos para consultas genéricas)
    # =========================================================================
    @staticmethod
    def obtener_todos(cedula_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT 
                pc.cod_pagos, pc.monto_abonado, pc.fecha_pago, dv.placa,
                cxc.estado AS estado_cuenta, cxc.deuda_total, cxc.fecha_vencimiento,
                dp.tipo_pago, dp.descripcion, dp.fecha_det_pago, mp.nombre_metodo,
                m.nombre_moneda, m.simbolo,
                COALESCE(db.refencia, dnd.refencia) AS referencia,
                COALESCE(db.monto, dnd.monto) AS monto_detalle, b.nombre_banco
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

    @staticmethod
    def obtener_deudas_pendientes(cedula_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT cxc.cod_cuentas, dv.placa, cxc.deuda_total, cxc.saldo_pendiente, v.cod_venta
            FROM cuentas_por_cobrar cxc
            INNER JOIN ventas v ON cxc.cod_venta = v.cod_venta
            INNER JOIN det_venta dv ON v.cod_venta = dv.cod_venta
            WHERE v.cedula_usuario = %s AND cxc.estado = 'pendiente'
        """
        cursor.execute(sql, (cedula_usuario,))
        res = cursor.fetchall()
        cursor.close()
        conexion.close()
        return res
    
    @staticmethod
    def obtener_todos_admin():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        sql_pagos = """
            SELECT 
                pc.cod_pagos, pc.monto_abonado, pc.fecha_pago, dv.placa,
                cxc.estado AS estado_cuenta, cxc.deuda_total, cxc.saldo_pendiente, cxc.fecha_vencimiento,
                dp.tipo_pago, dp.descripcion, dp.fecha_det_pago, mp.nombre_metodo,
                m.nombre_moneda, m.simbolo,
                COALESCE(db.refencia, dnd.refencia) AS referencia,
                COALESCE(db.monto, dnd.monto) AS monto_detalle, b.nombre_banco, v.cedula_usuario
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
            WHERE pc.activo = 1 -- 👈 CAPA 1: Solo traer pagos que no hayan sido anulados logícamente
            ORDER BY pc.fecha_pago DESC
        """
        try:
            cursor.execute(sql_pagos)
            pagos = cursor.fetchall()
            if not pagos:
                return []
                
            ids_clientes = list(set([p['cedula_usuario'] for p in pagos if p['cedula_usuario']]))
            
            if ids_clientes:
                conexion_seg = obtener_conexion_seguridad()
                cursor_seg = conexion_seg.cursor(dictionary=True)
                format_strings = ','.join(['%s'] * len(ids_clientes))
                
                sql_usuarios = f"""
                    SELECT cedula_usuario, nombre, apellido, telefono, direccion
                    FROM t_usuario 
                    WHERE cedula_usuario IN ({format_strings})
                """
                cursor_seg.execute(sql_usuarios, tuple(ids_clientes))
                usuarios = cursor_seg.fetchall()
                cursor_seg.close()
                conexion_seg.close()
                
                mapa_usuarios = {str(u['cedula_usuario']).strip(): u for u in usuarios}
                
                for p in pagos:
                    id_cli = str(p['cedula_usuario']).strip() if p.get('cedula_usuario') else ""
                    info_usuario = mapa_usuarios.get(id_cli, {})
                    
                    p['cedula'] = info_usuario.get('cedula_usuario', p.get('cedula_usuario', 'Sin Cédula'))
                    p['nombre'] = info_usuario.get('nombre', 'Sin Nombre')
                    p['apellido'] = info_usuario.get('apellido', '')
                    p['telefono'] = info_usuario.get('telefono', 'Sin Teléfono')
                    p['direccion'] = info_usuario.get('direccion', 'Sin Dirección')

            return pagos
        except Exception as e:
            print(f"Error al obtener pagos cruzados: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(cod_pagos):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            # Buscamos el pago para saber a qué cuenta pertenece y su monto
            cursor.execute("SELECT cod_cuentas, monto_abonado FROM pago_cuentas WHERE cod_pagos = %s AND activo = 1", (cod_pagos,))
            pago = cursor.fetchone()
            
            if pago:
                # 1. Reversamos el saldo en la cuenta por cobrar (Tu lógica original impecable)
                cursor.execute("""
                    UPDATE cuentas_por_cobrar 
                    SET saldo_pendiente = saldo_pendiente + %s, estado = 'pendiente'
                    WHERE cod_cuentas = %s
                """, (pago['monto_abonado'], pago['cod_cuentas']))

                # 2. ELIMINADO LÓGICO: En vez de DELETE, hacemos UPDATE del estado del pago
                cursor.execute("""
                    UPDATE pago_cuentas 
                    SET activo = 0 
                    WHERE cod_pagos = %s
                """, (cod_pagos,))
            
            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            print(f"Error al anular lógicamente el pago: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
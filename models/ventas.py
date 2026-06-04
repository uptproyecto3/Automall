from models.db import obtener_conexion

class Ventas:
    def __init__(self, cedula_cliente, placa, tipo_venta, poder, traspaso, monto_recibido, fecha_vencimiento=None):
        self.cedula_cliente = cedula_cliente
        self.placa = placa
        self.tipo_venta = tipo_venta  # 'contado' o 'credito'
        self.poder = 1 if poder else 0
        self.traspaso = 1 if traspaso else 0
        self.monto_recibido = float(monto_recibido)
        self.fecha_vencimiento = fecha_vencimiento

    def obtener_vehiculos_disponibles():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT 
                v.placa, v.color, v.anio, 
                m.nombre_marca, mod.nombre_modelo,
                c.precio_venta, c.descripcion
            FROM vehiculo v
            JOIN marca m ON v.cod_marca = m.cod_marca
            JOIN modelo mod ON v.cod_modelo = mod.cod_modelo
            JOIN catalogo c ON v.placa = c.placa
            WHERE v.estado = 'Disponible'
        """
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()    

    def registrar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # 1. Crear la Causal en 'cuentas_por_cobrar' primero (para obtener el ID)
            # El saldo pendiente dependerá de si es contado o crédito
            sql_cuenta = """
                INSERT INTO cuentas_por_cobrar (deuda_total, saldo_pendiente, fecha_vencimiento, estado)
                VALUES (%s, %s, %s, %s)
            """
            # Asumimos que el precio se recupera del vehículo (lógica simplificada)
            # Aquí deberías traer el precio real, usaremos el monto recibido como referencia inicial
            cursor.execute(sql_cuenta, (self.monto_recibido, 0, self.fecha_vencimiento, 'completado'))
            cod_cuentas = cursor.lastrowid

            # 2. Insertar en 'det_venta'
            sql_det = """
                INSERT INTO det_venta (poder, traspaso_papel, placa, cod_cuentas)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_det, (self.poder, self.traspaso, self.placa, cod_cuentas))
            cod_det_venta = cursor.lastrowid

            # 3. Insertar en 'ventas'
            sql_venta = """
                INSERT INTO ventas (estado, fecha_venta, tipo_venta, cedula_usuario, cod_det_venta)
                VALUES (%s, CURDATE(), %s, %s, %s)
            """
            cursor.execute(sql_venta, ('procesada', self.tipo_venta, self.cedula_cliente, cod_det_venta))
            cod_venta = cursor.lastrowid

            # 4. Actualizar el estado del vehículo a 'Vendido'
            sql_vehiculo = "UPDATE vehiculo SET estado = 'Vendido' WHERE placa = %s"
            cursor.execute(sql_vehiculo, (self.placa,))

            # 5. Si hubo un pago inicial, registrarlo en 'pago_cuentas'
            if self.monto_recibido > 0:
                sql_pago = """
                    INSERT INTO pago_cuentas (monto_abonado, fecha_pago, cod_cuentas, cod_metodo, cod_moneda)
                    VALUES (%s, NOW(), %s, %s, %s)
                """
                # Usamos IDs por defecto (1) para método y moneda si no vienen del form
                cursor.execute(sql_pago, (self.monto_recibido, cod_cuentas, 1, 1))

            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            print(f"Error en la transacción: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
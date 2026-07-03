from models.db import obtener_conexion
from datetime import date

class Compra:
    def __init__(self, fecha=None, monto_total=0, estado='Pendiente'):
        self.fecha = fecha or date.today()
        self.monto_total = monto_total
        self.estado = estado

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, COUNT(d.cod_det_compra) as total_items
            FROM compras_accesorios c
            LEFT JOIN det_compra d ON c.cod_compras = d.cod_compras
            GROUP BY c.cod_compras
            ORDER BY c.fecha DESC
        """)
        compras = cursor.fetchall()
        cursor.close()
        conexion.close()
        return compras

    @staticmethod
    def obtener_por_id(cod_compras):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM compras_accesorios WHERE cod_compras = %s
        """, (cod_compras,))
        compra = cursor.fetchone()
        
        # Obtener detalles
        if compra:
            cursor.execute("""
                SELECT d.*, i.nombre_insumo, v.placa, mo.nombre_modelo as modelo, v.color
                FROM det_compra d
                LEFT JOIN insumos i ON d.cod_insumo = i.cod_insumo
                LEFT JOIN vehiculo v ON d.placa = v.placa
                LEFT JOIN modelo mo ON v.cod_modelo = mo.cod_modelo
                WHERE d.cod_compras = %s
            """, (cod_compras,))
            compra['detalles'] = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        return compra

    @staticmethod
    def crear(cod_compras=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        if cod_compras:
            sql = "INSERT INTO compras_accesorios (cod_compras, fecha, monto_total, estado) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (cod_compras, date.today(), 0, 'Pendiente'))
        else:
            sql = "INSERT INTO compras_accesorios (fecha, monto_total, estado) VALUES (%s, %s, %s)"
            cursor.execute(sql, (date.today(), 0, 'Pendiente'))
            cod_compras = cursor.lastrowid
        
        conexion.commit()
        cursor.close()
        conexion.close()
        return cod_compras

    @staticmethod
    def agregar_detalle(cod_compras, cod_insumo, producto, cantidad, costo_unitario, placa):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Insertar detalle
        sql = """
            INSERT INTO det_compra 
            (cod_compras, cod_insumo, producto, cantidad, costo_unitario, placa) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (cod_compras, cod_insumo, producto, cantidad, costo_unitario, placa))
        
        # Actualizar monto_total de la compra
        cursor.execute("""
            UPDATE compras_accesorios 
            SET monto_total = (
                SELECT SUM(cantidad * costo_unitario) 
                FROM det_compra 
                WHERE cod_compras = %s
            )
            WHERE cod_compras = %s
        """, (cod_compras, cod_compras))
        
        # Actualizar stock del insumo
        if cod_insumo:
            cursor.execute("""
                UPDATE insumos 
                SET stock = stock + %s 
                WHERE cod_insumo = %s
            """, (cantidad, cod_insumo))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        return True

    @staticmethod
    def finalizar_compra(cod_compras):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE compras_accesorios 
            SET estado = 'Completada' 
            WHERE cod_compras = %s
        """, (cod_compras,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True

    @staticmethod
    def eliminar_detalle(cod_det_compra, cod_compras, cod_insumo, cantidad):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Eliminar detalle
        cursor.execute("DELETE FROM det_compra WHERE cod_det_compra = %s", (cod_det_compra,))
        
        # Restar del stock
        if cod_insumo:
            cursor.execute("""
                UPDATE insumos 
                SET stock = stock - %s 
                WHERE cod_insumo = %s
            """, (cantidad, cod_insumo))
        
        # Actualizar monto_total
        cursor.execute("""
            UPDATE compras_accesorios 
            SET monto_total = (
                SELECT COALESCE(SUM(cantidad * costo_unitario), 0)
                FROM det_compra 
                WHERE cod_compras = %s
            )
            WHERE cod_compras = %s
        """, (cod_compras, cod_compras))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        return True

    @staticmethod
    def eliminar_compra(cod_compras):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM det_compra WHERE cod_compras = %s", (cod_compras,))
        cursor.execute("DELETE FROM compras_accesorios WHERE cod_compras = %s", (cod_compras,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
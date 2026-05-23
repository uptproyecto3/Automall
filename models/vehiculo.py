from models.db import obtener_conexion_seguridad

class Vehiculo:
    @staticmethod
    def guardar_con_documentos(v_data, d_data, filename):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        try:
            # 1. Insertar Documentación
            sql_doc = """INSERT INTO documentacion (
                original_totalPropiedad, experticia_transito, certificado_origen, 
                carnet_circulacion, reserva_dominio, garantia_vehiculo, 
                certificado_garantia, manual_vehiculoGarantia, finiquito, 
                resguardo, seguro, factura_compra, fecha_ingreso, otro_documento
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql_doc, (
                d_data['original_totalPropiedad'], d_data['experticia_transito'], d_data['certificado_origen'],
                d_data['carnet_circulacion'], d_data['reserva_dominio'], d_data['garantia_vehiculo'],
                d_data['certificado_garantia'], d_data['manual_vehiculoGarantia'], d_data['finiquito'],
                d_data['resguardo'], d_data['seguro'], d_data['factura_compra'], 
                d_data['fecha_ingreso'], d_data['otro_documento']
            ))
            
            cod_documento = cursor.lastrowid

            # 2. Insertar Vehículo vinculado al documento
            # NOTA: Debes agregar la columna 'imagen_url' a tu tabla vehiculo en SQL si no existe.
            sql_veh = """INSERT INTO vehiculo (
                placa, color, anio, kilometraje, tipo, estado, cod_marca, cod_modelo, 
                cedula_proveedor, cod_documento
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql_veh, (
                v_data['placa'], v_data['color'], v_data['anio'], v_data['kilometraje'], v_data['tipo'], 
                'Disponible', v_data['marca'], v_data['modelo'], v_data['cedula'], cod_documento
            ))
            
            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM vehiculo")
        return cursor.fetchall()
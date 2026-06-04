from models.db import obtener_conexion 

class Vehiculo:
    @staticmethod
    def guardar_con_documentos(v_data, d_data, filename):
        conexion = obtener_conexion() 
        cursor = conexion.cursor()
        try:
            # 1. Insertar Documentación
            sql_doc = """INSERT INTO documentacion (
                original_totalPropiedad, experticia_transito, certificado_origen, 
                carnet_circulacion, reserva_dominio, garantia_vehiculo, 
                certificado_garantia, manual_vehiculoGarantia, finiquito, 
                resguardo, fecha_transferencia, seguro, factura_compra, 
                fecha_ingreso, otro_documento
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            
            cursor.execute(sql_doc, (
                d_data['original_totalPropiedad'], d_data['experticia_transito'], d_data['certificado_origen'],
                d_data['carnet_circulacion'], d_data['reserva_dominio'], d_data['garantia_vehiculo'],
                d_data['certificado_garantia'], d_data['manual_vehiculoGarantia'], d_data['finiquito'],
                d_data['resguardo'], 0, d_data['seguro'], d_data['factura_compra'], 
                d_data['fecha_ingreso'], d_data['otro_documento']
            ))
            cod_documento = cursor.lastrowid

            # 2. Insertar Registro de Accesorios (OBLIGATORIO por integridad de tu BD)
            # Registramos un set por defecto (1 = Sí, tiene los implementos básicos)
            sql_acc = "INSERT INTO accesorio (copia_llaves, repuesto, triangulo) VALUES (1, 1, 1)"
            cursor.execute(sql_acc)
            cod_accesorio = cursor.lastrowid

            # 3. Insertar Vehículo usando ambos IDs obtenidos (cod_documento y cod_accesorio)
            sql_veh = """INSERT INTO vehiculo (
                placa, color, anio, kilometraje, tipo, estado, 
                cod_marca, cod_modelo, cedula_proveedor, cod_documento, cod_accesorio
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql_veh, (
                v_data['placa'], v_data['color'], v_data['anio'], v_data['kilometraje'], v_data['tipo'], 
                v_data['estado'], v_data['marca'], v_data['modelo'], v_data['cedula'], 
                cod_documento, cod_accesorio
            ))

            # 4. Insertar Imagen vinculada a la placa
            sql_img = "INSERT INTO imagen (URL, placa) VALUES (%s, %s)"
            cursor.execute(sql_img, (f"uploads/{filename}", v_data['placa']))
            
            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            print(f"ERROR DB DETALLADO: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion() 
        cursor = conexion.cursor(dictionary=True) 
        sql = """
            SELECT v.*, m.nombre_marca, mo.nombre_modelo, i.URL as imagen_url
            FROM vehiculo v
            JOIN marca m ON v.cod_marca = m.cod_marca
            JOIN modelo mo ON v.cod_modelo = mo.cod_modelo
            LEFT JOIN imagen i ON v.placa = i.placa
            ORDER BY v.placa DESC
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conexion.close()
        return res
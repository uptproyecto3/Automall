from models.db import obtener_conexion 
from datetime import date 
from mysql.connector import Error

class Vehiculo:
    @staticmethod
    def guardar_con_documentos(v_data, d_data, a_data, c_data, filename):
        conexion = obtener_conexion() 
        cursor = conexion.cursor()
        try:
            # 1. Insertar Documentación
            sql_doc = """INSERT INTO documentacion (
                original_totalPropiedad, experticia_transito, certificado_origen, 
                carnet_circulacion, reserva_dominio, garantia_vehiculo, 
                certificado_garantia, manual_vehiculoGarantia, finiquito, 
                resguardo, seguro, factura_compra, fecha_ingreso, otro_documento
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            
            cursor.execute(sql_doc, (
                d_data['original_totalPropiedad'], d_data['experticia_transito'], d_data['certificado_origen'],
                d_data['carnet_circulacion'], d_data['reserva_dominio'], d_data['garantia_vehiculo'],
                d_data['certificado_garantia'], d_data['manual_vehiculoGarantia'], d_data['finiquito'],
                d_data['resguardo'], d_data['seguro'], d_data['factura_compra'], 
                d_data['fecha_ingreso'], d_data['otro_documento']
            ))
            cod_documento = cursor.lastrowid

            # 2. Insertar Accesorios
            sql_acc = "INSERT INTO accesorio (copia_llaves, repuesto, triangulo) VALUES (%s,%s,%s)"
            cursor.execute(sql_acc, (
                a_data['copia_llaves'], a_data['repuesto'], a_data['triangulo']
            ))
            cod_accesorio = cursor.lastrowid

            # 3. Insertar Vehículo
            sql_veh = """INSERT INTO vehiculo (
                placa, color, anio, kilometraje, tipo, estado, 
                cod_modelo, cedula_proveedor, cod_documento, cod_accesorio
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql_veh, (
                v_data['placa'], v_data['color'], v_data['anio'], v_data['kilometraje'], v_data['tipo'], 
                v_data['estado'], v_data['modelo'], v_data['cedula'], 
                cod_documento, cod_accesorio
            ))

            # 4. Insertar Catálogo 
            sql_cat = """INSERT INTO catalogo (
                estado, precio, descripcion, fecha_publicacion, placa
            ) VALUES (%s, %s, %s, %s, %s)"""
            
            cursor.execute(sql_cat, (
                c_data['estado'],
                c_data['precio'], 
                c_data['descripcion'], 
                c_data['fecha_pub'], 
                v_data['placa']
            ))

            # 5. Insertar Imagen
            sql_img = "INSERT INTO imagen (URL, placa) VALUES (%s, %s)"
            cursor.execute(sql_img, (f"uploads/{filename}", v_data['placa']))
            
            conexion.commit()
            return True
        except Error as e: # <--- CAMBIAR Exception por Error
            conexion.rollback()
            print(f"ERROR DB: {e}")
            # El código 1062 es "Duplicate entry" (Placa ya existe)
            if e.errno == 1062:
                raise Exception("La placa ingresada ya se encuentra registrada en el sistema.")
            else:
                raise Exception(f"Error en la base de datos: {str(e)}")
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion() 
        cursor = conexion.cursor(dictionary=True) 
        sql = """
            SELECT v.*, ma.nombre_marca, mo.nombre_modelo, i.URL as imagen_url,
                   d.*, a.*, p.razon_social as nombre_propietario
            FROM vehiculo v
            JOIN modelo mo ON v.cod_modelo = mo.cod_modelo
            JOIN marca ma ON mo.cod_marca = ma.cod_marca
            JOIN documentacion d ON v.cod_documento = d.cod_documento
            JOIN accesorio a ON v.cod_accesorio = a.cod_accesorio
            JOIN propietario p ON v.cedula_propietario = p.cedula_propietario
            LEFT JOIN imagen i ON v.placa = i.placa
            ORDER BY v.placa DESC
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conexion.close()
        return res
        
    @staticmethod
    def obtener_por_placa(placa):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT v.*, d.*, a.*, c.precio, c.descripcion as descripcion_catalogo, c.fecha_publicacion, i.URL as imagen_url
            FROM vehiculo v
            JOIN documentacion d ON v.cod_documento = d.cod_documento
            JOIN accesorio a ON v.cod_accesorio = a.cod_accesorio
            LEFT JOIN catalogo c ON v.placa = c.placa
            LEFT JOIN imagen i ON v.placa = i.placa
            WHERE v.placa = %s
        """
        cursor.execute(sql, (placa,))
        res = cursor.fetchone()
        cursor.close()
        conexion.close()
        return res

    @staticmethod
    def actualizar(placa_original, v_data, d_data, a_data, c_data, filename=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("SELECT cod_documento, cod_accesorio FROM vehiculo WHERE placa = %s", (placa_original,))
            ids = cursor.fetchone()
            if not ids: return False
            cod_doc, cod_acc = ids[0], ids[1]

            # 2. Actualizar Documentación
            sql_doc = """UPDATE documentacion SET 
                original_totalPropiedad=%s, experticia_transito=%s, certificado_origen=%s, 
                carnet_circulacion=%s, reserva_dominio=%s, garantia_vehiculo=%s, 
                certificado_garantia=%s, manual_vehiculoGarantia=%s, finiquito=%s, 
                resguardo=%s, seguro=%s, factura_compra=%s, fecha_ingreso=%s, otro_documento=%s
                WHERE cod_documento=%s"""
            cursor.execute(sql_doc, list(d_data.values()) + [cod_doc])

            # 3. Actualizar Accesorios
            sql_acc = "UPDATE accesorio SET copia_llaves=%s, repuesto=%s, triangulo=%s WHERE cod_accesorio=%s"
            cursor.execute(sql_acc, (a_data['copia_llaves'], a_data['repuesto'], a_data['triangulo'], cod_acc))

            # 4. Actualizar Vehículo 
            sql_veh = """UPDATE vehiculo SET 
                placa=%s, color=%s, anio=%s, kilometraje=%s, tipo=%s, estado=%s, 
                cod_modelo=%s, cedula_proveedor=%s WHERE placa=%s"""
            cursor.execute(sql_veh, (v_data['placa'], v_data['color'], v_data['anio'], v_data['kilometraje'], 
                                   v_data['tipo'], v_data['estado'], v_data['modelo'], v_data['cedula'], placa_original))

            # 5. Actualizar Catálogo 
            sql_cat = "UPDATE catalogo SET precio=%s, descripcion=%s, fecha_publicacion=%s, placa=%s WHERE placa=%s"
            cursor.execute(sql_cat, (c_data['precio'], c_data['descripcion'], c_data['fecha_pub'], v_data['placa'], placa_original))

            # 6. Actualizar Imagen
            if filename:
                cursor.execute("UPDATE imagen SET URL=%s, placa=%s WHERE placa=%s", (f"uploads/{filename}", v_data['placa'], placa_original))
            else:
                cursor.execute("UPDATE imagen SET placa=%s WHERE placa=%s", (v_data['placa'], placa_original))
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            print(f"ERROR DB UPDATE: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(placa):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT cod_documento, cod_accesorio FROM vehiculo WHERE placa = %s", (placa,))
            ids = cursor.fetchone()
            
            cursor.execute("DELETE FROM imagen WHERE placa = %s", (placa,))
            cursor.execute("DELETE FROM catalogo WHERE placa = %s", (placa,))
            cursor.execute("DELETE FROM vehiculo WHERE placa = %s", (placa,))
            
            if ids:
                cursor.execute("DELETE FROM documentacion WHERE cod_documento = %s", (ids[0],))
                cursor.execute("DELETE FROM accesorio WHERE cod_accesorio = %s", (ids[1],))
            
            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def buscar_por_placa(placa):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        placa_limpia = placa.strip().upper()
        
        sql = """
            SELECT 
                v.placa, 
                m.nombre_marca AS marca, 
                mo.nombre_modelo AS modelo, 
                v.anio, 
                v.color, 
                v.tipo, 
                c.precio, 
                c.estado
            FROM vehiculo v
            INNER JOIN catalogo c ON v.placa = c.placa
            INNER JOIN modelo mo ON v.cod_modelo = mo.cod_modelo
            INNER JOIN marca m ON mo.cod_marca = m.cod_marca
            WHERE v.placa = %s AND v.estado = 'Disponible'
            LIMIT 1
        """
        
        cursor.execute(sql, (placa_limpia,))
        vehiculo = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        # --- LA RESPONSABILIDAD SE MUDÓ AQUÍ ---
        if vehiculo:
            return {
                'exito': True,
                'vehiculo': {
                    'placa': vehiculo['placa'],
                    'marca': vehiculo['marca'],
                    'modelo': vehiculo['modelo'],
                    'tipo': vehiculo['tipo'],
                    'anio': vehiculo['anio'],
                    'color': vehiculo['color'],
                    'precio': float(vehiculo['precio']),
                    'estado': vehiculo['estado']
                }
            }
            
        return None
    
    @staticmethod
    def obtener_vehiculos_activos():
        """Obtiene solo los vehículos activos (para selects en compras)"""
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.placa, mo.nombre_modelo as modelo, v.color 
            FROM vehiculo v
            JOIN modelo mo ON v.cod_modelo = mo.cod_modelo
            WHERE v.estado = 'Disponible'
            ORDER BY v.placa
        """)
        vehiculos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return vehiculos
    
    @staticmethod
    def obtener_vehiculos_disponibles():
        """Obtiene solo los vehículos disponibles (para selects en ventas)"""
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.placa, mo.nombre_modelo as modelo, v.color 
            FROM vehiculo v
            JOIN modelo mo ON v.cod_modelo = mo.cod_modelo
            WHERE v.estado = 'Disponible'
            ORDER BY v.placa
        """)
        vehiculo = cursor.fetchall()
        cursor.close()
        conexion.close()
        return vehiculo
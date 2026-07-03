from models.db import obtener_conexion_seguridad

class citasModel:

    @staticmethod
    def contar_citas_en_horario(fecha, hora, cod_cita_excluir=None):
        if not fecha or not hora:
            return 0

        fecha_limpia = str(fecha).strip()
        hora_str = str(hora).strip()
        hora_busqueda = hora_str[:5] + "%" if len(hora_str) >= 5 else hora_str
        
        if cod_cita_excluir:
            sql = """
                SELECT COUNT(*) FROM automall.citas
                WHERE fecha = %s AND hora LIKE %s AND cod_citas != %s AND estado != 'Finalizada'
            """
            valores = (fecha_limpia, hora_busqueda, int(cod_cita_excluir))
        else:
            sql = """
                SELECT COUNT(*) FROM automall.citas
                WHERE fecha = %s AND hora LIKE %s AND estado != 'Finalizada'
            """
            valores = (fecha_limpia, hora_busqueda)

        conexion = obtener_conexion_seguridad()         
        cursor = conexion.cursor() 
        cursor.execute(sql, valores) 
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        return resultado[0] if resultado else 0
    

## Registro de cita-------------------------------------------------------------------------------
    @staticmethod
    def registrar_citas(fecha, hora, cod_catalogo, cedula_usuario):
        conexion = obtener_conexion_seguridad ()
        cursor = conexion.cursor()

        sql= """
            INSERT INTO automall.citas
            (fecha, hora, cod_catalogo, cedula_usuario,estado)

            VALUES (%s, %s, %s, %s, 'Pendiente')
            """
        
        valores = (fecha, hora, cod_catalogo, cedula_usuario)

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()
        return True
    
    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)

        sql = """
        SELECT 
            v.placa,
            v.color,
            v.anio,
            c.cod_catalogo,
            m.nombre_modelo,
            ma.nombre_marca,
            i.URL as imagen_url
        FROM automall.vehiculo v
        INNER JOIN automall.catalogo c ON v.placa = c.placa
        LEFT JOIN automall.modelo m   ON v.cod_modelo = m.cod_modelo
        LEFT JOIN automall.marca ma   ON m.cod_marca = ma.cod_marca
        LEFT JOIN automall.imagen i   ON v.placa = i.placa
        """

        cursor.execute(sql)
        vehiculos_catalogo = cursor.fetchall()

        cursor.close()
        conexion.close()

        return vehiculos_catalogo    
    
    @staticmethod
    def obtener_citas_transito():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT c.cod_citas, c.fecha, c.hora, c.estado,
                   m.nombre_marca, mo.nombre_modelo, v.placa, 
                   u.nombre, u.apellido, u.telefono, u.cedula_usuario,
                   i.URL AS imagen_url
            FROM automall.citas c
            JOIN automall.catalogo cat ON c.cod_catalogo = cat.cod_catalogo
            JOIN automall.vehiculo v ON cat.placa = v.placa
            JOIN automall.modelo mo ON v.cod_modelo = mo.cod_modelo
            JOIN automall.marca m ON mo.cod_marca = m.cod_marca
            JOIN seguridad.t_usuario u ON c.cedula_usuario = u.cedula_usuario
            LEFT JOIN automall.imagen i ON v.placa = i.placa"""
        cursor.execute(sql)
        lista_citas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return lista_citas
## Elminar / modificar---------------------------------------------------------------------

    @staticmethod
    def eliminar_cita_db(cod_cita, cedula_usuario=None):
        """Función 100% UNIFICADA para ambos roles"""
        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor(dictionary=True, buffered=True)
            
            # Caso A: Administrador (Borrado físico duro global)
            if cedula_usuario is None:
                sql = "DELETE FROM automall.citas WHERE cod_citas = %s"
                parametros = (cod_cita,)
            
            # Caso B: Cliente (Filtro estricto por IDOR y estado)
            else:
                sql = """
                    DELETE FROM automall.citas 
                    WHERE cod_citas = %s AND cedula_usuario = %s AND estado = 'Pendiente'
                """
                parametros = (cod_cita, cedula_usuario)
            
            cursor.execute(sql, parametros)
            conexion.commit()
            
            filas_afectadas = cursor.rowcount
            cursor.close()
            conexion.close()
            
            if filas_afectadas > 0:
                return {"status": True, "mensaje": "¡La cita ha sido eliminada con éxito!"}
            return {"status": False, "mensaje": "No se pudo eliminar la cita seleccionada."}
        except Exception as e:
            return {"status": False, "mensaje": f"Error: {str(e)}"}
        
    @staticmethod
    def obtener_cita_por_id(cod_cita):
        """
        Recupera de manera segura los campos actuales de una cita específica usando cursores.
        """
        sql = "SELECT fecha, hora, estado FROM automall.citas WHERE cod_citas = %s"
        valores = (int(cod_cita),)
        
        conexion = obtener_conexion_seguridad() 
        cursor = conexion.cursor()
        
        cursor.execute(sql, valores)
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if resultado:
            hora_raw = str(resultado[1]).strip()
            hora_limpia = hora_raw[:5] if len(hora_raw) >= 5 else hora_raw

            return {
                'fecha': str(resultado[0]).strip(),
                'hora': hora_limpia,
                'estado': str(resultado[2]).strip()
            }
        return None

    @staticmethod
    def actualizar_cita(datos):
        """
        Modifica los datos de una cita usando consultas preparadas inmunes a SQL Injection.
        """
        sql = """
            UPDATE automall.citas 
            SET fecha = %s, hora = %s, estado = %s 
            WHERE cod_citas = %s
        """
        hora_envio = datos['hora'].strip()
        if len(hora_envio) >= 5:
            hora_envio = hora_envio[:5]

        valores = (
            datos['fecha'].strip(),
            hora_envio,
            datos['estado'].strip(),
            int(datos['cod_citas'])
        )
        
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        
        cursor.execute(sql, valores)    
        conexion.commit()
        
        cursor.close()
        conexion.close()
## Finalizar cita------------------------------------------------------------------------------
    @staticmethod
    def finalizar_cita_db(cod_citas):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        sql = "UPDATE automall.citas SET estado = 'Finalizada' WHERE cod_citas = %s"
        cursor.execute(sql, (cod_citas,))
        conexion.commit()
        cursor.close()
        conexion.close()

##Esta es la cita personal de cada cliente______________________________________________________
    @staticmethod
    def obtener_por_cliente(cedula_usuario):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True, buffered=True)
        
        sql = """
            SELECT c.cod_citas, c.fecha, c.hora, c.estado,
                   m.nombre_marca, mo.nombre_modelo, v.placa,
                   i.URL AS imagen_url
            FROM automall.citas c
            JOIN automall.catalogo cat ON c.cod_catalogo = cat.cod_catalogo
            JOIN automall.vehiculo v ON cat.placa = v.placa
            JOIN automall.modelo mo ON v.cod_modelo = mo.cod_modelo
            JOIN automall.marca m ON mo.cod_marca = m.cod_marca
            LEFT JOIN automall.imagen i ON v.placa = i.placa
            WHERE c.cedula_usuario = %s
            ORDER BY c.fecha DESC, c.hora DESC
        """
        cursor.execute(sql, (cedula_usuario,))
        citas = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        return citas
    
    @staticmethod
    def modificar_hora_cliente(cod_cita, nueva_hora, cedula_usuario):
        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor(dictionary=True, buffered=True)
            
            # Restricción total de seguridad: Coincidencia de dueño y estado pendiente
            sql = """
                UPDATE automall.citas 
                SET hora = %s 
                WHERE cod_citas = %s AND cedula_usuario = %s AND estado = 'Pendiente'
            """
            cursor.execute(sql, (cod_cita, nueva_hora , cedula_usuario))
            conexion.commit()
            
            filas_afectadas = cursor.rowcount
            cursor.close()
            conexion.close()
            
            if filas_afectadas > 0:
                return {"status": True, "mensaje": "¡La hora de tu cita ha sido modificada con éxito!"}
            return {"status": False, "mensaje": "No se pudo modificar la hora (la cita ya no está pendiente o no te pertenece)."}
        except Exception as e:
            return {"status": False, "mensaje": f"Error: {str(e)}"}
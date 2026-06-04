from models.db import obtener_conexion_seguridad 

class Usuario:
    def __init__(self, cedula, nombre, apellido, telefono, direccion, correo, password, foto):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        self.password = password
        self.foto = foto # Nueva propiedad

    def guardar(self):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        # Agregamos 'foto' a la consulta SQL
        sql = """
            INSERT INTO t_usuario 
            (cedula_usuario, nombre, apellido, telefono, direccion, correo, password, foto) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (self.cedula, self.nombre, self.apellido, 
               self.telefono, self.direccion, self.correo, self.password, self.foto)
        
        cursor.execute(sql, val)
        conexion.commit()
        
        cursor.close()
        conexion.close()


    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM t_usuario")
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return usuarios

    @staticmethod
    def eliminar(cedula_usuario):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        cursor.execute("UPDATE t_usuario SET estado = 0 WHERE cedula_usuario = %s", (cedula_usuario,))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar(cedula_usuario, nombre, apellido, telefono, direccion, correo):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        
        # Eliminamos 'cedula_usuario = %s' de la consulta
        sql = """
            UPDATE t_usuario 
            SET nombre = %s, 
                apellido = %s, 
                telefono = %s, 
                direccion = %s, 
                correo = %s
            WHERE cedula_usuario = %s
        """
        
        # Ajustamos las variables para que coincidan con los %s
        val = (nombre, apellido, telefono, direccion, correo, cedula_usuario)
        
        cursor.execute(sql, val)
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_por_cedula(cedula_usuario):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        # Consulta limpia usando tus campos nativos cod_rol
        sql = """
            SELECT u.nombre, 
                u.apellido, 
                u.telefono, 
                u.direccion, 
                u.correo, 
                u.cedula_usuario, 
                r.nombre_rol 
            FROM t_usuario u
            LEFT JOIN t_rol r ON u.cod_rol = r.cod_rol
            WHERE u.cedula_usuario = %s
        """
        
        # Saneamos la tupla para que no confunda al conector de MySQL
        cursor.execute(sql, (cedula_usuario,))
        usuario = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        return usuario
            
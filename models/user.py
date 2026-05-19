from models.db import obtener_conexion_seguridad

class Usuario:
    def __init__(self, cedula_usuario, nombre, apellido, telefono, direccion, correo, password):
        self.cedula = cedula_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        self.password = password

    def guardar(self):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO t_usuario 
            (cedula_usuario, nombre, apellido, telefono, direccion, correo, password) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (self.cedula_usuario, self.nombre, self.apellido, 
               self.telefono, self.direccion, self.correo, self.password)
        
        cursor.execute(sql, val)
        conexion.commit()  # Esto guarda los cambios en MySQL
        
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
    def eliminar(id):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        cursor.execute("UPDATE t_usuario SET  WHERE id = %s", (id,))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar(id, nombre, apellido, telefono, direccion, correo):
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
            WHERE id = %s
        """
        
        # Ajustamos las variables para que coincidan con los %s
        val = (nombre, apellido, telefono, direccion, correo, id)
        
        cursor.execute(sql, val)
        conexion.commit()
        cursor.close()
        conexion.close()
        
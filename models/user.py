from models.db import obtener_conexion

class Usuario:
    def __init__(self, cedula, nombre, apellido, telefono, direccion, correo, password):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        self.password = password

    def guardar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO usuarios 
            (cedula, nombre, apellido, telefono, direccion, correo, password) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (self.cedula, self.nombre, self.apellido, 
               self.telefono, self.direccion, self.correo, self.password)
        
        cursor.execute(sql, val)
        conexion.commit()  # Esto guarda los cambios en MySQL
        
        cursor.close()
        conexion.close()

    @staticmethod
    def verificar_credenciales(correo, password):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        # IMPORTANTE: Asegúrate de incluir 'id_rol' en el SELECT
        sql = "SELECT id, nombre, id_rol FROM usuarios WHERE correo = %s AND password = %s"
        cursor.execute(sql, (correo, password))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return usuarios

    @staticmethod
    def eliminar(id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar(id, cedula, nombre, apellido, telefono, direccion, correo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            UPDATE usuarios 
            SET cedula = %s, 
                nombre = %s, 
                apellido = %s, 
                telefono = %s, 
                direccion = %s, 
                correo = %s
            WHERE id = %s
        """
        val = (cedula, nombre, apellido, telefono, direccion, correo, id)
        cursor.execute(sql, val)
        conexion.commit()
        cursor.close()
        conexion.close()
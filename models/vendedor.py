from models.db import obtener_conexion_seguridad
from utils.validaciones import ValidacionUsuario
import hashlib

class Vendedor: 
    def __init__(self, cedula, nombre, apellido, telefono, direccion, correo, password, foto="default.png", cod_rol=3):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        # Hashear la contraseña
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.foto = foto
        self.cod_rol = cod_rol
        self.estado = 1

    @staticmethod
    def verificar_existencia(cedula, correo, cedula_actual=None):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        if cedula_actual is None:
            sql = "SELECT cedula_usuario, correo FROM t_usuario WHERE cedula_usuario = %s OR correo = %s"
            cursor.execute(sql, (cedula, correo))
        else:
            sql = "SELECT correo FROM t_usuario WHERE correo = %s AND cedula_usuario != %s"
            cursor.execute(sql, (correo, cedula_actual))
            
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado

    def guardar(self):
        # Validaciones de Formato
        print("=== INICIO GUARDAR VENDEDOR ===")
            
        # Validaciones de Formato - una por una para ver cuál falla
        err1 = ValidacionUsuario.validar_cedula_formato(self.cedula)
        print(f"validar_cedula_formato: {err1}")
            
        err2 = ValidacionUsuario.validar_nombre_apellido(self.nombre, "Nombre")
        print(f"validar_nombre: {err2}")
            
        err3 = ValidacionUsuario.validar_nombre_apellido(self.apellido, "Apellido")
        print(f"validar_apellido: {err3}")
            
        err4 = ValidacionUsuario.validar_telefono(self.telefono)
        print(f"validar_telefono: {err4}")
            
        err5 = ValidacionUsuario.validar_formato_correo(self.correo)
        print(f"validar_correo: {err5}")
            
        err6 = ValidacionUsuario.validar_direccion(self.direccion)
        print(f"validar_direccion: {err6}")
            
        err7 = ValidacionUsuario.validar_password_segura(self.password)
        print(f"validar_password: {err7}")
            
        err = err1 or err2 or err3 or err4 or err5 or err6 or err7
        
        print(f"Resultado final validación: {err}")
        
        if err:
            return {"status": False, "mensaje": err}

        # Validar duplicados
        existe = self.verificar_existencia(self.cedula, self.correo)
        if existe:
            if str(existe.get('cedula_usuario')) == str(self.cedula):
                return {"status": False, "mensaje": "La cédula ya se encuentra registrada."}
            if existe.get('correo') == self.correo:
                return {"status": False, "mensaje": "El correo ya está en uso por otro usuario."}

        # Guardar en BD
        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor()
            sql = """
                INSERT INTO t_usuario 
                (cedula_usuario, nombre, apellido, telefono, direccion, correo, password, foto, estado, cod_rol) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (self.cedula, self.nombre, self.apellido, self.telefono,
                   self.direccion, self.correo, self.password, self.foto, 
                   self.estado, self.cod_rol)
            cursor.execute(sql, val)
            conexion.commit()
            cursor.close()
            conexion.close()
            return {"status": True, "mensaje": "Vendedor registrado exitosamente."}
        except Exception as e:
            return {"status": False, "mensaje": f"Error en BD: {str(e)}"}

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.nombre_rol 
            FROM t_usuario u
            JOIN t_rol r ON u.cod_rol = r.cod_rol
            WHERE u.cod_rol = 3
            ORDER BY u.nombre, u.apellido
        """)
        vendedores = cursor.fetchall()
        cursor.close()
        conexion.close()
        return vendedores

    @staticmethod
    def obtener_por_cedula(cedula):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.nombre_rol 
            FROM t_usuario u
            JOIN t_rol r ON u.cod_rol = r.cod_rol
            WHERE u.cedula_usuario = %s AND u.cod_rol = 3
        """, (cedula,))
        vendedor = cursor.fetchone()
        cursor.close()
        conexion.close()
        return vendedor

    @staticmethod
    def actualizar(cedula, nombre, apellido, telefono, direccion, correo):
        err = (ValidacionUsuario.validar_nombre_apellido(nombre, "Nombre") or
               ValidacionUsuario.validar_nombre_apellido(apellido, "Apellido") or
               ValidacionUsuario.validar_telefono(telefono) or
               ValidacionUsuario.validar_formato_correo(correo) or
               ValidacionUsuario.validar_direccion(direccion))
        
        if err:
            return {"status": False, "mensaje": err}

        existe = Vendedor.verificar_existencia(None, correo, cedula_actual=cedula)
        if existe:
            return {"status": False, "mensaje": "El correo ya está siendo usado por otro usuario."}

        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor()
            sql = """
                UPDATE t_usuario 
                SET nombre = %s, apellido = %s, telefono = %s, direccion = %s, correo = %s
                WHERE cedula_usuario = %s AND cod_rol = 3
            """
            cursor.execute(sql, (nombre, apellido, telefono, direccion, correo, cedula))
            conexion.commit()
            cursor.close()
            conexion.close()
            return {"status": True, "mensaje": "Vendedor actualizado correctamente."}
        except Exception as e:
            return {"status": False, "mensaje": str(e)}

    @staticmethod
    def cambiar_estado(cedula, estado):
        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE t_usuario SET estado = %s 
                WHERE cedula_usuario = %s AND cod_rol = 3
            """, (estado, cedula))
            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except Exception as e:
            print(f"Error al cambiar estado: {e}")
            return False
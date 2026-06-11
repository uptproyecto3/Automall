from models.db import obtener_conexion_seguridad 
from werkzeug.security import generate_password_hash  # <-- IMPORTANTE: Añade esta importación arriba de tu modelo
from utils.validaciones import ValidacionUsuario

class Usuario:
    def __init__(self, cedula, nombre, apellido, telefono, direccion, correo, password, foto):
        self.cedula = cedula
        self.password = generate_password_hash(password)  # <-- HASH LA CONTRASEÑA ANTES DE GUARDARLA
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        self.password = password
        self.foto = foto

    @staticmethod
    def verificar_existencia(cedula, correo, es_nuevo=True, cedula_actual=None):
        """Comprueba si la cédula o correo ya existen en la BD"""
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        
        # Si es registro nuevo, buscamos cualquier coincidencia
        if es_nuevo:
            sql = "SELECT cedula_usuario, correo FROM t_usuario WHERE cedula_usuario = %s OR correo = %s"
            cursor.execute(sql, (cedula, correo))
        else:
            # Si es edición, buscamos que otros (diferentes a la cédula actual) tengan ese correo
            sql = "SELECT correo FROM t_usuario WHERE correo = %s AND cedula_usuario != %s"
            cursor.execute(sql, (correo, cedula_actual))
            
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado

    def guardar(self):
        # 1. Validaciones de Formato (usando utils)
        # Evaluamos la contraseña en texto plano para asegurar que cumple con los requisitos de fuerza
        err = ValidacionUsuario.validar_cedula_formato(self.cedula) or \
            ValidacionUsuario.validar_nombre_apellido(self.nombre, "Nombre") or \
            ValidacionUsuario.validar_nombre_apellido(self.apellido, "Apellido") or \
            ValidacionUsuario.validar_telefono(self.telefono) or \
            ValidacionUsuario.validar_formato_correo(self.correo) or \
            ValidacionUsuario.validar_direccion(self.direccion) or \
            ValidacionUsuario.validar_password_segura(self.password)
        
        if err: return {"status": False, "mensaje": err}

        # 2. Validar duplicados en BD
        existe = self.verificar_existencia(self.cedula, self.correo, es_nuevo=True)
        if existe:
            if str(existe['cedula_usuario']) == str(self.cedula):
                return {"status": False, "mensaje": "La cédula ya se encuentra registrada."}
            if existe['correo'] == self.correo:
                return {"status": False, "mensaje": "El correo ya está en uso por otro usuario."}

        # --- CAMBIO DE SEGURIDAD: Hashear la contraseña ---
        # Generamos un hash seguro a partir de la contraseña original.
        # El método generate_password_hash ya maneja la sal de forma automática y segura.
        password_hasheada = generate_password_hash(self.password)
        # --------------------------------------------------

        # 3. Proceder al guardado
        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor()
            sql = """
                INSERT INTO t_usuario 
                (cedula_usuario, nombre, apellido, telefono, direccion, correo, password, foto, estado) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
            """
            # Sustituimos self.password por la variable local que contiene el hash seguro
            val = (self.cedula, self.nombre, self.apellido, 
                self.telefono, self.direccion, self.correo, password_hasheada, self.foto)
            
            cursor.execute(sql, val)
            conexion.commit()
            cursor.close()
            conexion.close()
            return {"status": True, "mensaje": "Usuario registrado exitosamente."}
        except Exception as e:
            return {"status": False, "mensaje": f"Error en BD: {str(e)}"}

    @staticmethod
    def actualizar(cedula_usuario, nombre, apellido, telefono, direccion, correo):
        # 1. Validaciones de Formato
        err = ValidacionUsuario.validar_nombre_apellido(nombre, "Nombre") or \
              ValidacionUsuario.validar_nombre_apellido(apellido, "Apellido") or \
              ValidacionUsuario.validar_telefono(telefono) or \
              ValidacionUsuario.validar_formato_correo(correo) or \
              ValidacionUsuario.validar_direccion(direccion)
        
        if err: return {"status": False, "mensaje": err}

        # 2. Validar si el correo nuevo ya lo tiene OTRA persona
        existe = Usuario.verificar_existencia(None, correo, es_nuevo=False, cedula_actual=cedula_usuario)
        if existe:
            return {"status": False, "mensaje": "El correo ya está siendo usado por otro usuario."}

        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor()
            sql = """
                UPDATE t_usuario 
                SET nombre = %s, apellido = %s, telefono = %s, direccion = %s, correo = %s
                WHERE cedula_usuario = %s
            """
            cursor.execute(sql, (nombre, apellido, telefono, direccion, correo, cedula_usuario))
            conexion.commit()
            cursor.close()
            conexion.close()
            return {"status": True, "mensaje": "Usuario actualizado correctamente."}
        except Exception as e:
            return {"status": False, "mensaje": str(e)}

    # Los métodos obtener_todos, eliminar, obtener_por_cedula se mantienen igual...
    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM t_usuario WHERE estado = 1") # Solo activos
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return usuarios

    @staticmethod
    def eliminar(cedula_usuario):
        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor()
            cursor.execute("UPDATE t_usuario SET estado = 0 WHERE cedula_usuario = %s", (cedula_usuario,))
            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except:
            return False

    @staticmethod
    def obtener_por_cedula(cedula_usuario):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT u.*, r.nombre_rol 
            FROM t_usuario u
            LEFT JOIN t_rol r ON u.cod_rol = r.cod_rol
            WHERE u.cedula_usuario = %s
        """
        cursor.execute(sql, (cedula_usuario,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()
        return usuario
    
    @staticmethod
    def buscar_cliente_por_cedula(cedula):
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True) 
        
        # Añadimos telefono, direccion y correo a la consulta
        sql = """
            SELECT cedula_usuario, nombre, apellido, telefono, direccion, correo 
            FROM t_usuario 
            WHERE cedula_usuario = %s AND cod_rol = 4 
            LIMIT 1
        """
        
        cursor.execute(sql, (cedula,))
        cliente = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        return cliente
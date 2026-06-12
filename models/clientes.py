# Modelo de clientes — solo SQL parametrizado, sin lógica de negocio
from models.db import obtener_conexion_seguridad
from utils.validaciones import ValidacionUsuario
from werkzeug.security import generate_password_hash


class ClienteModel:

    def __init__(self, cedula, nombre, apellido, telefono, direccion, correo, password, foto, cod_rol=4):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        self.password = password
        self.foto = foto
        self.cod_rol = cod_rol

    # -----------------------------------------------------------------------
    # REGISTRO
    # -----------------------------------------------------------------------
    @staticmethod
    def verificar_existencia(cedula, correo):
        """Comprueba de forma paramétrica si la cédula o correo ya existen."""
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT cedula_usuario, correo FROM seguridad.t_usuario WHERE cedula_usuario = %s OR correo = %s"
        cursor.execute(sql, (cedula, correo))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado

    def registrar_cliente_db(self):
        """
        Ejecuta las validaciones y guarda el cliente en la BD
        mediante consultas parametrizadas inmunes a SQL Injection.
        """
        err = ValidacionUsuario.validar_cedula_formato(self.cedula)
        if err: return {"status": False, "mensaje": err}

        err = ValidacionUsuario.validar_nombre_apellido(self.nombre, "Nombre")
        if err: return {"status": False, "mensaje": err}

        err = ValidacionUsuario.validar_nombre_apellido(self.apellido, "Apellido")
        if err: return {"status": False, "mensaje": err}

        err = ValidacionUsuario.validar_telefono(self.telefono)
        if err: return {"status": False, "mensaje": err}

        err = ValidacionUsuario.validar_direccion(self.direccion)
        if err: return {"status": False, "mensaje": err}

        err = ValidacionUsuario.validar_formato_correo(self.correo)
        if err: return {"status": False, "mensaje": err}

        err = ValidacionUsuario.validar_password_segura(self.password)
        if err: return {"status": False, "mensaje": err}

        if self.verificar_existencia(self.cedula, self.correo):
            return {"status": False, "mensaje": "La cédula o el correo electrónico ya se encuentran registrados."}

        try:
            hash_pwd = generate_password_hash(self.password)

            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor()

            sql = """
                INSERT INTO seguridad.t_usuario
                (cedula_usuario, nombre, apellido, telefono, direccion, correo, password, foto, cod_rol, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """
            valores = (
                self.cedula.strip(),
                self.nombre.strip(),
                self.apellido.strip(),
                self.telefono.strip(),
                self.direccion.strip(),
                self.correo.strip(),
                hash_pwd,
                self.foto,
                self.cod_rol
            )

            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()

            return {"status": True, "mensaje": "¡Tu cuenta de cliente ha sido creada con éxito!"}

        except Exception as e:
            return {"status": False, "mensaje": f"Error interno en el servidor: {str(e)}"}

    # -----------------------------------------------------------------------
    # GESTIÓN (Solo Super Usuario)
    # -----------------------------------------------------------------------
    @staticmethod
    def obtener_clientes():
        """Retorna todos los usuarios con rol de cliente (cod_rol = 4)."""
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT cedula_usuario, nombre, apellido, telefono, direccion, correo, foto
            FROM seguridad.t_usuario
            WHERE cod_rol = 4
            ORDER BY apellido ASC, nombre ASC
        """
        cursor.execute(sql)
        clientes = cursor.fetchall()
        cursor.close()
        conexion.close()
        return clientes

    @staticmethod
    def obtener_por_cedula(cedula):
        """Retorna un cliente específico por su cédula."""
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT cedula_usuario, nombre, apellido, telefono, direccion, correo, foto
            FROM seguridad.t_usuario
            WHERE cedula_usuario = %s AND cod_rol = 4
        """
        cursor.execute(sql, (cedula,))
        cliente = cursor.fetchone()
        cursor.close()
        conexion.close()
        return cliente

    @staticmethod
    def actualizar_cliente(datos):
        """Actualiza los datos personales de un cliente usando SQL parametrizado."""
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor()
        sql = """
            UPDATE seguridad.t_usuario
            SET nombre = %s, apellido = %s, telefono = %s, direccion = %s, correo = %s, foto = %s
            WHERE cedula_usuario = %s AND cod_rol = 4
        """
        valores = (
            datos['nombre'].strip(),
            datos['apellido'].strip(),
            datos['telefono'].strip(),
            datos['direccion'].strip(),
            datos['correo'].strip(),
            datos['foto'],
            datos['cedula']
        )
        cursor.execute(sql, valores)
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        conexion.close()
        return filas > 0

    @staticmethod
    def eliminar_cliente(cedula):
        """Elimina físicamente un cliente. El filtro cod_rol = 4 impide borrar otros roles."""
        try:
            conexion = obtener_conexion_seguridad()
            cursor = conexion.cursor()
            sql = "DELETE FROM seguridad.t_usuario WHERE cedula_usuario = %s AND cod_rol = 4"
            cursor.execute(sql, (cedula,))
            conexion.commit()
            filas = cursor.rowcount
            cursor.close()
            conexion.close()
            if filas > 0:
                return {"status": True, "mensaje": "✨ Cliente eliminado del sistema con éxito."}
            return {"status": False, "mensaje": "No se encontró el cliente o no se puede eliminar."}
        except Exception as e:
            return {"status": False, "mensaje": f"Error al eliminar: {str(e)}"}

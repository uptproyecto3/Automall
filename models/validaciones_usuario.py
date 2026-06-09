import re
from models.db import obtener_conexion_seguridad

class ValidacionUsuario:

    @staticmethod
    def validar_campos_vacios(datos):
        """Verifica que los campos obligatorios no estén vacíos."""
        errores = {}
        for campo, valor in datos.items():
            if not valor or str(valor).strip() == "":
                errores[campo] = f"El campo {campo} es obligatorio."
        return errores

    @staticmethod
    def validar_formato_correo(correo):
        """Valida que el correo tenga un formato válido."""
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.match(regex, correo):
            return "El formato del correo electrónico no es válido."
        return None

    @staticmethod
    def validar_cedula_formato(cedula):
        """Valida que la cédula sea numérica y tenga la longitud correcta (ej. 10 dígitos)."""
        if not cedula.isdigit():
            return "La cédula debe contener solo números."
        if len(cedula) != 10:
            return "La cédula debe tener exactamente 10 dígitos."
        return None

    @staticmethod
    def verificar_unicidad(cedula, correo, excluir_cedula=None):
        """
        Verifica si la cédula o el correo ya existen en la base de datos.
        excluir_cedula: se usa cuando estamos actualizando un usuario para que no se autodetecte.
        """
        conexion = obtener_conexion_seguridad()
        cursor = conexion.cursor(dictionary=True)
        errores = {}

        # Verificar Cédula (Solo si es registro nuevo o cambió la cédula)
        if excluir_cedula:
            sql_cedula = "SELECT cedula_usuario FROM t_usuario WHERE cedula_usuario = %s AND cedula_usuario != %s"
            cursor.execute(sql_cedula, (cedula, excluir_cedula))
        else:
            sql_cedula = "SELECT cedula_usuario FROM t_usuario WHERE cedula_usuario = %s"
            cursor.execute(sql_cedula, (cedula,))
        
        if cursor.fetchone():
            errores['cedula'] = "Esta cédula ya se encuentra registrada."

        # Verificar Correo
        if excluir_cedula:
            sql_correo = "SELECT correo FROM t_usuario WHERE correo = %s AND cedula_usuario != %s"
            cursor.execute(sql_correo, (correo, excluir_cedula))
        else:
            sql_correo = "SELECT correo FROM t_usuario WHERE correo = %s"
            cursor.execute(sql_correo, (correo,))

        if cursor.fetchone():
            errores['correo'] = "Este correo electrónico ya está en uso."

        cursor.close()
        conexion.close()
        return errores

    @classmethod
    def validar_registro(cls, datos):
        """
        Valida todo el proceso de registro de un usuario.
        Retorna (True, None) si todo está bien, o (False, errores) si hay fallas.
        """
        errores = cls.validar_campos_vacios(datos)
        
        # Si hay campos vacíos, retornamos de inmediato
        if errores:
            return False, errores

        # Validaciones de formato
        err_correo = cls.validar_formato_correo(datos.get('correo'))
        if err_correo: errores['correo'] = err_correo

        err_cedula = cls.validar_cedula_formato(datos.get('cedula'))
        if err_cedula: errores['cedula'] = err_cedula

        # Añadimos # nosec B105 para indicarle a Bandit que esto no es una credencial en duro
        if len(datos.get('password', '')) < 6:
            errores['password'] = "La contraseña debe tener al menos 6 caracteres." # nosec B105

        # Si no hay errores de formato, verificar unicidad en BD
        if not errores:
            err_unicidad = cls.verificar_unicidad(datos['cedula'], datos['correo'])
            errores.update(err_unicidad)

        if errores:
            return False, errores
        return True, None

    @classmethod
    def validar_actualizacion(cls, cedula_actual, datos):
        """Valida los datos al editar un perfil."""
        # Filtramos solo los campos que vienen en la actualización
        errores = {}
        
        if 'correo' in datos:
            err_correo = cls.validar_formato_correo(datos['correo'])
            if err_correo: errores['correo'] = err_correo
        
        # Verificar si el nuevo correo ya lo tiene otro usuario
        if not errores:
            err_unicidad = cls.verificar_unicidad(cedula_actual, datos.get('correo'), excluir_cedula=cedula_actual)
            errores.update(err_unicidad)

        if errores:
            return False, errores
        return True, None
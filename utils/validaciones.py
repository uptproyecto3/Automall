import re

class ValidacionUsuario:
    
    @staticmethod
    def validar_formato_correo(correo):
        if not correo:
            return "El correo electrónico es obligatorio."
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(patron, correo):
            return "El formato del correo electrónico no es válido."
        return None

    @staticmethod
    def validar_password_segura(password):
        """
        Reglas: > 8 caracteres, 1 Mayúscula, 1 Carácter alfanumérico (símbolo/especial)
        """
        if not password:
            return "La contraseña es obligatoria."
        if len(password) < 8:
            return "La contraseña debe tener más de 8 caracteres."
        if not any(char.isupper() for char in password):
            return "La contraseña debe contener al menos una letra mayúscula."
        # Verificar carácter especial (no alfanumérico)
        if not re.search(r"[^a-zA-Z0-9]", password):
            return "La contraseña debe contener al menos un carácter especial (ej: !@#$%^&*)."
        return None

    @staticmethod
    def validar_nombre_apellido(texto, campo="Nombre"):
        if not texto or len(texto.strip()) < 2:
            return f"El {campo} debe tener al menos 2 caracteres."
        # Solo letras y espacios
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", texto):
            return f"El {campo} solo debe contener letras."
        return None

    @staticmethod
    def validar_telefono(telefono):
        # Valida formatos comunes (solo números, entre 7 y 15 dígitos)
        if not telefono or not re.match(r"^[0-9]{7,15}$", telefono):
            return "El teléfono debe contener entre 7 y 15 dígitos numéricos."
        return None

    @staticmethod
    def validar_direccion(direccion):
        if not direccion or len(direccion.strip()) < 5:
            return "La dirección es demasiado corta o está vacía."
        return None

    @staticmethod
    def validar_cedula_formato(cedula):
        if not cedula or not str(cedula).isdigit():
            return "La cédula debe ser un valor numérico."
        if len(str(cedula)) < 6:
            return "La cédula es demasiado corta."
        return None

    @staticmethod
    def validar_foto_perfil(archivo):
        """
        Valida la foto de perfil subida:
        - Extensión permitida: jpg, jpeg, png, webp
        - Tamaño máximo: 5 MB
        """
        if not archivo or archivo.filename == '':
            return None  # Foto opcional, no es un error

        extensiones_permitidas = {'jpg', 'jpeg', 'png', 'webp'}
        nombre = archivo.filename.lower()
        extension = nombre.rsplit('.', 1)[-1] if '.' in nombre else ''

        if extension not in extensiones_permitidas:
            return "Formato de imagen no permitido. Use JPG, PNG o WEBP."

        archivo.seek(0, 2)  # Ir al final del archivo
        tamanio = archivo.tell()
        archivo.seek(0)     # Regresar al inicio

        if tamanio > 5 * 1024 * 1024:  # 5 MB
            return "La imagen no puede superar los 5 MB."

        return None

    @staticmethod
    def validar_modificacion_cliente(datos):
        """
        Valida los campos editables de un cliente.
        Retorna (True, {}) si es válido, o (False, errores).
        """
        errores = {}

        err = ValidacionUsuario.validar_nombre_apellido(datos.get('nombre'), "Nombre")
        if err:
            errores['nombre'] = err

        err = ValidacionUsuario.validar_nombre_apellido(datos.get('apellido'), "Apellido")
        if err:
            errores['apellido'] = err

        err = ValidacionUsuario.validar_telefono(datos.get('telefono'))
        if err:
            errores['telefono'] = err

        err = ValidacionUsuario.validar_direccion(datos.get('direccion'))
        if err:
            errores['direccion'] = err

        err = ValidacionUsuario.validar_formato_correo(datos.get('correo'))
        if err:
            errores['correo'] = err

        return len(errores) == 0, errores
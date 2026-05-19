import re

class ValidadorAuth:
    @staticmethod
    def validar_login(correo, password):
        errores = []
        
        # Limpieza básica
        correo = correo.strip() if correo else ""
        
        # Regla: No vacíos
        if not correo or not password:
            errores.append("Todos los campos son obligatorios.")
        
        # Regla: Formato de correo
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if correo and not re.match(email_regex, correo):
            errores.append("El formato del correo no es válido.")
            
        # Regla: Longitud de password (ejemplo 4 caracteres)
        if password and len(password) < 4:
            errores.append("La contraseña debe tener al menos 4 caracteres.")
            
        return errores, correo # Retornamos los errores y el correo ya limpio
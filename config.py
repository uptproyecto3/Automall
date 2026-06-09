class Config:
    # Base de datos principal (Vehículos, Ventas, Clientes)
    DB_NEGOCIO = {
        'host': 'localhost',
        'user': 'root',
        'password': '', # nosec B105
        'database': 'automall'
    }

    # Base de datos de seguridad (Usuarios, Permisos, Bitácora)
    DB_SEGURIDAD = {
        'host': 'localhost',
        'user': 'root',
        'password': '', # nosec B105
        'database': 'seguridad'
    }
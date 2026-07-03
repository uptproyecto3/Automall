from datetime import datetime

def validar_registro_venta(venta):
    """
    Recibe la instancia del modelo Ventas y evalúa sus propiedades.
    Retorna un diccionario indicando el estatus y el error si aplica.
    """
    # 1. Validaciones de presencia y strings obligatorios
    if not venta.cedula_cliente or not str(venta.cedula_cliente).strip():
        return {"status": False, "error": "La cédula del cliente es obligatoria para procesar la venta."}
        
    if not venta.placa or not str(venta.placa).strip():
        return {"status": False, "error": "La placa del vehículo es obligatoria."}
        
    if venta.tipo_venta not in ['contado', 'credito']:
        return {"status": False, "error": "El tipo de venta debe ser obligatoriamente 'contado' o 'credito'."}

    # 2. Validaciones de lógica financiera elemental
    if venta.precio_total <= 0:
        return {"status": False, "error": "El precio total del vehículo debe ser un monto mayor a cero."}
        
    if venta.monto_recibido < 0:
        return {"status": False, "error": "El monto recibido no puede ser un valor negativo."}

    # 3. Reglas de negocio según Tipo de Venta
    if venta.tipo_venta == 'contado':
        if venta.monto_recibido < venta.precio_total:
            return {"status": False, "error": "En ventas de contado, el monto inicial recibido debe cubrir la totalidad del precio."}
        if venta.deuda_pendiente > 0:
            return {"status": False, "error": "Una venta de contado no puede generar un saldo de deuda pendiente."}
            
    elif venta.tipo_venta == 'credito':
        if not venta.fecha_vencimiento:
            return {"status": False, "error": "Las ventas a crédito requieren establecer una fecha de vencimiento de cuotas."}
        
        # Validar formato de fecha y que sea una fecha posterior al día de hoy
        try:
            fecha_venc = datetime.strptime(str(venta.fecha_vencimiento), "%Y-%m-%d").date()
            if fecha_venc <= datetime.now().date():
                return {"status": False, "error": "La fecha de vencimiento del crédito debe ser un día futuro."}
        except ValueError:
            return {"status": False, "error": "El formato de la fecha de vencimiento es inválido (Use AAAA-MM-DD)."}

        # Verificar consistencia matemática del saldo restante
        deuda_calculada = round(venta.precio_total - venta.monto_recibido, 2)
        if round(venta.deuda_pendiente, 2) != deuda_calculada:
            return {"status": False, "error": f"Inconsistencia en montos: La deuda enviada ({venta.deuda_pendiente}) no coincide con el cálculo real ({deuda_calculada})."}

    # 4. Validaciones de pasarela de pagos (Solo si se recibe dinero inicial)
    if venta.monto_recibido > 0:
        if not venta.cod_metodo:
            return {"status": False, "error": "Especifique el método de pago utilizado para el monto recibido."}
       
        if not venta.cod_moneda:
           return {"status": False, "error": "Debe especificar el tipo de moneda del pago inicial."}
        
        # Métodos de pago virtuales/digitales
        metodos_digitales = ['5', '6', '7']
        if str(venta.cod_metodo) in metodos_digitales:
            if not venta.cod_mon_digital:
                return {"status": False, "error": "Seleccione la plataforma o billetera digital correspondiente al pago."}
        else:
            # Si no es efectivo rústico (asumiendo ID '1'), exigir banco emisor
            if str(venta.cod_metodo) != '1' and not venta.cod_banco:
                return {"status": False, "error": "Debe especificar el banco emisor de la transacción bancaria."}

    return {"status": True}


def validar_actualizacion_venta(data):
    """Valida el diccionario de datos antes de ejecutar una consulta UPDATE."""
    if not data.get('cod_venta'):
        return {"status": False, "error": "El código de la venta es requerido para realizar la actualización."}
    if not data.get('cedula_cliente') or not str(data.get('cedula_cliente')).strip():
        return {"status": False, "error": "La cédula del cliente no puede quedar vacía."}
    if data.get('tipo_venta') not in ['contado', 'credito']:
        return {"status": False, "error": "Tipo de venta inválido."}
    if float(data.get('deuda_total', 0)) < 0:
        return {"status": False, "error": "La deuda total no puede ser un valor negativo."}
        
    return {"status": True}
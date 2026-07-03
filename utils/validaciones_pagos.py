def validar_abono_pago(pago):
    """
    Evalúa la instancia del modelo Pagos antes de registrar un abono.
    """
    # 1. Validaciones estructurales básicas
    if not pago.cod_cuentas:
        return {"status": False, "error": "No se especificó el código de la cuenta por cobrar asociada al pago."}
        
    if pago.monto_pago <= 0:
        return {"status": False, "error": "El monto del abono debe ser un valor mayor a cero."}

    # 2. Control de límites financieros (Regla de negocio)
    if pago.monto_pago > pago.saldo_actual:
        return {
            "status": False, 
            "error": f"Monto excedido: Está intentando abonar {pago.monto_pago}$, pero el saldo pendiente actual de la deuda es de {pago.saldo_actual}$."
        }

    # 3. Validaciones obligatorias de pasarela y monedas
    if not pago.cod_metodo:
        return {"status": False, "error": "Debe seleccionar un método de pago."}
        
    if not pago.cod_moneda:
        return {"status": False, "error": "Debe especificar el tipo de moneda con la que cancela."}

    # 4. Validaciones condicionales (Bancos / Billeteras Digitales)
    metodos_digitales = ['5', '6', '7']
    
    # if str(pago.cod_metodo) in metodos_digitales:
    #     if not pago.cod_mon_digital:
    #         return {"status": False, "error": "Para métodos digitales, debe seleccionar la plataforma correspondiente (Pago Móvil, Binance, etc.)."}
    # else:
    #     # Si no es efectivo convencional (asumiendo ID '1'), exigir banco emisor
    #     if str(pago.cod_metodo) != '1' and not pago.cod_banco:
    #         return {"status": False, "error": "Para transacciones bancarias, es obligatorio seleccionar el banco emisor."}

    # Exigir referencia obligatoria para cualquier método que no sea efectivo ('1')
    if str(pago.cod_metodo) != '1' and not str(pago.referencia).strip():
        return {"status": False, "error": "Por motivos de auditoría, las transacciones que no son en efectivo requieren un número de referencia obligatorio."}

    return {"status": True}


def validar_actualizacion_pago(pago):
    """
    Evalúa la instancia del modelo Pagos antes de modificar un registro existente.
    """
    if not pago.cod_pagos:
        return {"status": False, "error": "El código del pago es requerido para poder efectuar una actualización."}
        
    if pago.monto_pago <= 0:
        return {"status": False, "error": "El nuevo monto del pago debe ser mayor a cero."}
        
    if not pago.cod_metodo:
        return {"status": False, "error": "El método de pago no puede quedar vacío."}
        
    if not pago.cod_moneda:
        return {"status": False, "error": "La moneda asociada al pago es obligatoria."}

    return {"status": True}
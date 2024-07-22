def calcular_pago_mensual(propiedad):
    # Parámetros del crédito hipotecario
    valor_uf=2400
    # porcentaje_pie=20
    valor_pie=480
    tasa_interes_anual = 0.05
    numero_meses = 240

    # Cálculo de la tasa de interés mensual
    tasa_interes_mensual = tasa_interes_anual / 12

    # Monto del préstamo (valor de la propiedad menos el pie)
    monto_prestamo = valor_uf - valor_pie

    # Fórmula para calcular el pago mensual
    pago_mensual = (monto_prestamo * tasa_interes_mensual) / (1 - (1 + tasa_interes_mensual) ** -numero_meses)
    
    return pago_mensual


def calcular_puntaje_capacidad_pago(salario, pago_mensual):
    if salario <= pago_mensual:
        return 0
    elif salario >= 6 * pago_mensual:
        return 100
    else:
        return (salario - pago_mensual) / (6 * pago_mensual - pago_mensual) * 100
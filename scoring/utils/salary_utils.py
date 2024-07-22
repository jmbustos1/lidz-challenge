

def calcular_pago_mensual(propiedad):
    """
    Funciones que calculan el valor de los pagos
    de un credito hipotecario
    """    
    valor_uf=2400
    valor_pie=600
    tasa_interes_anual = 0.05
    numero_meses = 240

    tasa_interes_mensual = tasa_interes_anual / 12

    monto_prestamo = valor_uf - valor_pie

    pago_mensual = (monto_prestamo * tasa_interes_mensual) / (1 - (1 + tasa_interes_mensual) ** -numero_meses)
    
    return pago_mensual


def calcular_puntaje_capacidad_pago(salario, pago_mensual):
    """
    Asigan 100 si tu salario es
    6 veces superior a la cuota
    del credito hipotecario
    y 0 si es igual o menor,
    interpola lineal entre los valores
    """
    if salario <= pago_mensual:
        return 0
    elif salario >= 6 * pago_mensual:
        return 100
    else:
        return (salario - pago_mensual) / (6 * pago_mensual - pago_mensual) * 100
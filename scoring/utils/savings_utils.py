
def calcular_puntaje_ahorros(savings, down_payment):
    """
    Funcion que asigna valor a tus ahorros
    si tienes ahorrado la mitad del pie
    asigna 0
    si tienes ahorrado 8 veces el pie 
    asigna 100, e interpola lineal
    """
    if savings <= down_payment / 2:
        return 0
    elif savings >= 8 * down_payment:
        return 100
    else:
        return (savings - down_payment / 2) / (8 * down_payment - down_payment / 2) * 100

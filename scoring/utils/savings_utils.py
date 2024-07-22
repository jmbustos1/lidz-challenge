
def calcular_puntaje_ahorros(savings, down_payment):
    if savings <= down_payment / 2:
        return 0
    elif savings >= 8 * down_payment:
        return 100
    else:
        return (savings - down_payment / 2) / (8 * down_payment - down_payment / 2) * 100

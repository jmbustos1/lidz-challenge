import math

"""
Funcion para ajustar peso a la edad
la idea es que a partir de 70 asigne cercano a 0
"""
def calcular_puntaje_edad(edad):
    if edad <= 18:
        return 100
    else:
        k = math.log(100) / (100 - 18)
        return 100 * math.exp(-k * (edad - 18))
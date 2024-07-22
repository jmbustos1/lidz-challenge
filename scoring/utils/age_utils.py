import math

def calcular_puntaje_edad(edad):
    if edad <= 18:
        return 100
    else:
        # Ajustar k para que el puntaje decaiga exponencialmente y sea cercano a 0 alrededor de los 100 años
        k = math.log(100) / (100 - 18)
        return 100 * math.exp(-k * (edad - 18))
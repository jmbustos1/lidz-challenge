"""Asigna valor lineal a las interacciones con el bot"""

def calcular_puntaje_mensajes(cantidad_mensajes):
    if cantidad_mensajes >= 100:
        return 100
    else:
        return cantidad_mensajes
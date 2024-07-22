import math
from datetime import datetime

"""
funcion que vale 1 en 0
es decir a los 0 años de deuda no pondera
sin embargo acelera con el tiempo 
alcanzando el maximo punto de
inflexion alrededor de los 5 años
es decir pesan mas las deudas antiguas
"""
x_move = 1
factor = 1/6
y_move = 2.6 + 4
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def debt_risk(x,x_move = x_move, factor = factor, y_move = y_move):
    return factor*(sign(x-x_move) * math.log(1 + abs(x-x_move)) +  y_move)
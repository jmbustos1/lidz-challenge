from .risk_functions import debt_risk
from datetime import datetime




def debt_risk_value(debt):
    days_old = (datetime.now().date() - debt.due_date).days
    print("days_old", days_old)
    years_old = days_old / 365.25
    print("years_old", years_old)
    adjustment_factor = debt_risk(20)
    print("adjustment_factor", adjustment_factor)
    adjusted_amount = debt.amount * adjustment_factor
    print("adjusted_amount", adjusted_amount)
    return adjusted_amount


def calculate_score(client):
    """
    Calcula el puntaje de un cliente basado en ciertos criterios.
    Por ahora, la lógica es simplificada, pero puede expandirse según sea necesario.
    """
    # Ejemplo simple de cálculo de puntaje
    base_score = 50 

    # Agrega puntos por cada criterio
    if client.salary > 1000000:
        base_score += 10
    if client.savings > 5000000:
        base_score += 10

    # Resta puntos si tiene deudas grandes
    total_debt = sum(debt.amount for debt in client.debts.all())
    if total_debt > 1000000:
        base_score -= 20

    print(debt_risk_value(client.debts.first()))

    # Asegurar que el puntaje esté entre 0 y 100
    return max(0, min(base_score, 100))
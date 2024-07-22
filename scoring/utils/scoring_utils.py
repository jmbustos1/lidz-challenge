from scoring.utils.age_utils import calcular_puntaje_edad
from scoring.utils.message_utils import calcular_puntaje_mensajes
from scoring.utils.savings_utils import calcular_puntaje_ahorros
from .risk_functions import debt_risk
from datetime import datetime

from stats.models import EstadisticasDeuda
from scoring.enums import BankChoices
from scoring.models import Client, Debt, Message
from .salary_utils import calcular_pago_mensual, calcular_puntaje_capacidad_pago

def get_latest_statistics():
    latest_stats = {}
    for bank in BankChoices:
        latest_stat = EstadisticasDeuda.objects.filter(institution=bank.value).order_by('-timestamp').first()
        if latest_stat:
            latest_stats[bank.value] = {
                'media_deuda': latest_stat.media_deuda,
                'desviacion_estandar_deuda': latest_stat.desviacion_estandar_deuda,
                'deuda_minima': latest_stat.deuda_minima,
                'deuda_maxima': latest_stat.deuda_maxima
            }
    return latest_stats

# Función para estandarizar las deudas
def estandarizar_deudas(cliente_id, latest_stats):
    client = Client.objects.get(id=cliente_id)
    deudas = Debt.objects.filter(client=client)
    
    deudas_estandarizadas = []
    for deuda in deudas:
        bank_stats = latest_stats.get(deuda.institution)
        if bank_stats:
            media = bank_stats['media_deuda']
            desviacion_estandar = bank_stats['desviacion_estandar_deuda']
            
            if desviacion_estandar != 0:
                estandarizada = (deuda.amount - media) / desviacion_estandar
            else:
                estandarizada = 0  # Manejar el caso cuando la desviación estándar es cero

            deudas_estandarizadas.append({
                'deuda': deuda,
                'banco': deuda.institution,
                'valor_estandarizado': estandarizada
            })
    return deudas_estandarizadas
# Función para ajustar la deuda según la antigüedad
def debt_risk_value(deuda, valor):
    days_old = (datetime.now().date() - deuda.due_date).days
    years_old = days_old / 365.25
    adjustment_factor = debt_risk(years_old)
    adjusted_amount = valor * adjustment_factor
    return adjusted_amount

# Función para ajustar las deudas estandarizadas por antigüedad
def ajustar_deudas_estandarizadas(deudas_estandarizadas):
    deudas_ajustadas = []
    for deuda_info in deudas_estandarizadas:
        deuda = deuda_info['deuda']
        valor_estandarizado = deuda_info['valor_estandarizado']
        valor_ajustado = debt_risk_value(deuda, valor_estandarizado)
        deudas_ajustadas.append({
            'deuda': deuda,
            'banco': deuda_info['banco'],
            'valor_ajustado': valor_ajustado
        })
    return deudas_ajustadas

# Función para normalizar las deudas ajustadas entre 0 y 100
def normalizar_deudas(deudas_ajustadas):
    deudas_normalizadas = []
    for deuda_info in deudas_ajustadas:
        valor_ajustado = deuda_info['valor_ajustado']
        valor_normalizado = (valor_ajustado + 2) / 4 * 100
        deudas_normalizadas.append(valor_normalizado)
    return deudas_normalizadas

def prom(deudas):
    puntaje_final = sum(deudas) / len(deudas)
    return puntaje_final
def calculate_score(client):
    """
    Calcula el puntaje de un cliente basado en ciertos criterios.
    Por ahora, la lógica es simplificada, pero puede expandirse según sea necesario.
    """
    uf = 37591
    pie_departamento = 600
    latest_stats = get_latest_statistics()
    # clients = Client.objects.all()


    deudas_estandarizadas = estandarizar_deudas(client.id, latest_stats)
    if deudas_estandarizadas:
        print(f'Deudas estandarizadas para el cliente {client.id}: {deudas_estandarizadas}')

        # Ajustar deudas estandarizadas por antigüedad
        deudas_ajustadas = ajustar_deudas_estandarizadas(deudas_estandarizadas)
        print(f'Deudas ajustadas por antigüedad para el cliente {client.id}: {deudas_ajustadas}')

        # Normalizar deudas ajustadas entre 0 y 100
        deudas_normalizadas = normalizar_deudas(deudas_ajustadas)
        print(f'Deudas normalizadas para el cliente {client.id}: {deudas_normalizadas}')
        # Normalizar deudas ajustadas entre 0 y 100
        puntaje_deuda = prom(deudas_normalizadas)
        puntaje_deuda = 100- puntaje_deuda
        print(f'Puntaje final para el cliente {client.id}: {puntaje_deuda}')

    else:
        print(f'El cliente {client.id} no tiene deudas para estandarizar')

    pago_mensual = calcular_pago_mensual(client.salary)
    print("PAGO MENSUAL", pago_mensual, "SALARIO",  client.salary/uf)
    puntaje_capacidad_pago = calcular_puntaje_capacidad_pago(client.salary/uf, pie_departamento)
    print("puntaje_capacidad_pago", puntaje_capacidad_pago)
    # Calcular puntaje de ahorros
    puntaje_ahorros = calcular_puntaje_ahorros(client.savings/uf, 600)
    print("puntaje_ahorros", puntaje_ahorros)
    # Calcular puntaje de edad
    puntaje_edad = calcular_puntaje_edad(client.age)
    print(" puntaje_edad ", puntaje_edad)
    # Calcular puntaje de mensajes
    cantidad_mensajes = Message.objects.filter(client=client).count()
    puntaje_mensajes = calcular_puntaje_mensajes(cantidad_mensajes)
    print("puntaje_mensajes", puntaje_mensajes)

        # Asignar ponderaciones a los puntajes
    peso_deuda = 0.20
    peso_capacidad_pago = 0.30
    peso_ahorros = 0.20
    peso_mensajes = 0.10
    peso_edad = 0.2  # Asumiendo que no se usa el puntaje de edad en el cálculo final según tus instrucciones

    puntaje_final = (
        puntaje_deuda * peso_deuda +
        puntaje_capacidad_pago * peso_capacidad_pago +
        puntaje_ahorros * peso_ahorros +
        puntaje_mensajes * peso_mensajes +
        puntaje_edad * peso_edad
    )
    # Asegurar que el puntaje esté entre 0 y 100
    return max(0, min(puntaje_final, 100))
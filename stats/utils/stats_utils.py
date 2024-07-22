from django.db.models import Avg, Min, Max
from scoring.models import Debt, Client
from stats.models import EstadisticasDeuda, EstadisticasSalario
from scoring.enums import BankChoices
import numpy as np

def calculate_and_save_statistics():
    """
    Funcion para calcular y agregar a los modelos
    datos estadisticos de los clientes
    esto servira para el modelo de deuda posteriormente.
    """
    bancos = [choice.value for choice in BankChoices]
    
    for banco in bancos:
        deudas = list(Debt.objects.filter(institution=banco).values_list('amount', flat=True))
        if deudas:
            media_deuda = np.mean(deudas)
            desviacion_estandar_deuda = np.std(deudas)
            deuda_minima = np.min(deudas)
            deuda_maxima = np.max(deudas)
            cantidad_datos = len(deudas)
            
            print(f'Banco: {banco}')
            print(f'Deudas: {deudas}')
            print(f'Media de deuda: {media_deuda}')
            print(f'Desviación estándar de deuda: {desviacion_estandar_deuda}')
            print(f'Deuda mínima: {deuda_minima}')
            print(f'Deuda máxima: {deuda_maxima}')

            EstadisticasDeuda.objects.create(
                media_deuda=media_deuda,
                desviacion_estandar_deuda=desviacion_estandar_deuda,
                deuda_minima=deuda_minima,
                deuda_maxima=deuda_maxima,
                institution=banco,
                cantidad_datos = cantidad_datos
            )

    salarios = list(Client.objects.values_list('salary', flat=True))
    if salarios:
        media_salario = np.mean(salarios)
        desviacion_estandar_salario = np.std(salarios)
        salario_minimo = np.min(salarios)
        salario_maximo = np.max(salarios)
        cantidad_datos = len(salarios)
        
        print(f'Salarios: {salarios}')
        print(f'Media de salario: {media_salario}')
        print(f'Desviación estándar de salario: {desviacion_estandar_salario}')
        print(f'Salario mínimo: {salario_minimo}')
        print(f'Salario máximo: {salario_maximo}')

        EstadisticasSalario.objects.create(
            media_salario=media_salario,
            desviacion_estandar_salario=desviacion_estandar_salario,
            salario_minimo=salario_minimo,
            salario_maximo=salario_maximo,
            cantidad_datos = cantidad_datos
        )
from django.db.models import Avg, StdDev, Min, Max
from scoring.models import Debt, Client
from stats.models import EstadisticasDeuda, EstadisticasSalario

def calculate_and_save_statistics():
    # Definir rangos etarios
    age_ranges = {
        '18-30': (18, 30),
        '31-45': (31, 45),
        '46-60': (46, 60),
        '60+': (61, 100)
    }
    
    for edad_minima, edad_maxima in age_ranges.values():
        # Calcular estadísticas de deuda para cada rango etario
        debt_stats = Debt.objects.filter(client__age__gte=edad_minima, client__age__lte=edad_maxima)
        print("DEBTS: ", debt_stats)
        debt_stats = Debt.objects.filter(client__age__gte=edad_minima, client__age__lte=edad_maxima).aggregate(
            media_deuda=Avg('amount'),
            desviacion_estandar_deuda=StdDev('amount'),
            deuda_minima=Min('amount'),
            deuda_maxima=Max('amount')
        )
        
        if all(value is not None for value in debt_stats.values()):
            EstadisticasDeuda.objects.create(
                media_deuda=debt_stats['media_deuda'],
                edad_minima=edad_minima,
                edad_maxima=edad_maxima,
                desviacion_estandar_deuda=debt_stats['desviacion_estandar_deuda'],
                deuda_minima=debt_stats['deuda_minima'],
                deuda_maxima=debt_stats['deuda_maxima']
            )

        # Calcular estadísticas de salario para cada rango etario
        salary_stats = Client.objects.filter(age__gte=edad_minima, age__lte=edad_maxima).aggregate(
            media_salario=Avg('salary'),
            desviacion_estandar_salario=StdDev('salary'),
            salario_minimo=Min('salary'),
            salario_maximo=Max('salary')
        )
        
        if all(value is not None for value in salary_stats.values()):
            EstadisticasSalario.objects.create(
                media_salario=salary_stats['media_salario'],
                edad_minima=edad_minima,
                edad_maxima=edad_maxima,
                desviacion_estandar_salario=salary_stats['desviacion_estandar_salario'],
                salario_minimo=salary_stats['salario_minimo'],
                salario_maximo=salary_stats['salario_maximo']
            )
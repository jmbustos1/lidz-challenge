from django.db import models
import datetime
from django.utils import timezone
from scoring.enums import BankChoices

class EstadisticasDeuda(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    media_deuda = models.FloatField()
    desviacion_estandar_deuda = models.FloatField()
    deuda_minima = models.FloatField()
    deuda_maxima = models.FloatField()
    institution = models.CharField(max_length=100, choices=BankChoices.choices, default='Banco Default')
    cantidad_datos = models.IntegerField(default=0)

    def __str__(self):
        return f"Estadísticas Deuda para {self.timestamp}"


class EstadisticasSalario(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    media_salario = models.FloatField()
    desviacion_estandar_salario = models.FloatField()
    salario_minimo = models.FloatField()
    salario_maximo = models.FloatField()
    # institution = models.CharField(max_length=100, choices=BankChoices.choices, default='Banco Default')
    cantidad_datos = models.IntegerField(default=0)

    def __str__(self):
        return f"Estadísticas Salario para {self.timestamp}"
    

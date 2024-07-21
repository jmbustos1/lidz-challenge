from django.db import models
import datetime
from django.utils import timezone


class EstadisticasDeuda(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    media_deuda = models.FloatField()
    edad_minima = models.IntegerField()
    edad_maxima = models.IntegerField()
    desviacion_estandar_deuda = models.FloatField()
    deuda_minima = models.FloatField()
    deuda_maxima = models.FloatField()

    def __str__(self):
        return f"Estadísticas Deuda para {self.timestamp}"


class EstadisticasSalario(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    media_salario = models.FloatField()
    edad_minima = models.IntegerField()
    edad_maxima = models.IntegerField()
    desviacion_estandar_salario = models.FloatField()
    salario_minimo = models.FloatField()
    salario_maximo = models.FloatField()

    def __str__(self):
        return f"Estadísticas Salario para {self.timestamp}"
    

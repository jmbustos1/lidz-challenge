from django.contrib import admin
from .models import EstadisticasDeuda, EstadisticasSalario



class EstadisticasDeudaAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'media_deuda', 'edad_minima', 'edad_maxima', 'desviacion_estandar_deuda', 'deuda_minima', 'deuda_maxima')
    list_filter = ('edad_minima', 'edad_maxima')
    readonly_fields = ('id',)

class EstadisticasSalarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'media_salario', 'edad_minima', 'edad_maxima', 'desviacion_estandar_salario', 'salario_minimo', 'salario_maximo')
    list_filter = ('edad_minima', 'edad_maxima')
    readonly_fields = ('id',)

admin.site.register(EstadisticasDeuda, EstadisticasDeudaAdmin)
admin.site.register(EstadisticasSalario, EstadisticasSalarioAdmin)
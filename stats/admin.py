from django.contrib import admin
from .models import EstadisticasDeuda, EstadisticasSalario

class EstadisticasDeudaAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'media_deuda', 'desviacion_estandar_deuda', 'deuda_minima', 'deuda_maxima', 'institution', 'cantidad_datos')
    list_filter = ('institution', 'timestamp')
    search_fields = ('id', 'timestamp', 'institution')
    readonly_fields = ('id', 'timestamp')

class EstadisticasSalarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'media_salario', 'desviacion_estandar_salario', 'salario_minimo', 'salario_maximo', 'cantidad_datos')
    list_filter = ('timestamp',)
    search_fields = ('id', 'timestamp')
    readonly_fields = ('id', 'timestamp')

admin.site.register(EstadisticasDeuda, EstadisticasDeudaAdmin)
admin.site.register(EstadisticasSalario, EstadisticasSalarioAdmin)
# Generated by Django 3.2.25 on 2024-07-21 08:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EstadisticasDeuda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('media_deuda', models.FloatField()),
                ('edad_minima', models.IntegerField()),
                ('edad_maxima', models.IntegerField()),
                ('desviacion_estandar_deuda', models.FloatField()),
                ('deuda_minima', models.FloatField()),
                ('deuda_maxima', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='EstadisticasSalario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('media_salario', models.FloatField()),
                ('edad_minima', models.IntegerField()),
                ('edad_maxima', models.IntegerField()),
                ('desviacion_estandar_salario', models.FloatField()),
                ('salario_minimo', models.FloatField()),
                ('salario_maximo', models.FloatField()),
            ],
        ),
    ]

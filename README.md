# Lidz Challenge

## Requisitos
- Docker
- Docker Compose

## Instrucciones

1. **Clonar el repositorio:**
    ```bash
    git clone https://github.com/jmbustos1/lidz-challenge
    ```

2. **Crear archivo .env para pruebas en local:**
    ```bash
    cp env.example.txt .env
    ```

3. **Crear la imagen:**
    ```bash
    sudo docker build .
    ```

4. **Levantar contenedores:**
    ```bash
    sudo docker compose up
    ```
5. **Ingresar al contenedor de Django:**
    ```bash
    sudo docker exec -it lidz-django /bin/bash
    ```
6. **Realizar migraciones:**
    ```bash
    python manage.py migrate
    ```

7. **Poblar base de datos:**
    ```bash
    python manage.py db_data
    ```

8. **Probar endpoint:**
    ```bash
    curl http://localhost:8000/clients
    ```

# Diseño de score
![Diagrama del Proyecto](diagram.png)

## Explicacion:
1. **Score de salario**
Para este item es necesario asumir el interes por cierto departamento
imaginemos uno de 3000 UF con pie de 20%.
Luego de contar con ese supuesto es necesario realizar el calculo de 
cada cuotael cual se muestra a continuacion:


$$\text{Pago Mensual} = \frac{\text{Monto del Préstamo} \times \text{Tasa de Interés Mensual}}{1 - (1 + \text{Tasa de Interés Mensual})^{-\text{Número de Pagos}}}$$

Luego la capacidad de pago se da calculando un factor
$$$\text{Cuota} = \frac{\text{Salario}}{Pago Mensual} $$

Finalmente se ajusta linealmente el factor tal que si alguien tiene salario 8
veces mayor a la cuota entonces se le asigna 100 y si es igual entonces es 0


```python
    def calcular_puntaje_capacidad_pago(salario, pago_mensual):
        """
        Asigan 100 si tu salario es
        6 veces superior a la cuota
        del credito hipotecario
        y 0 si es igual o menor,
        interpola lineal entre los valores
        """
        if salario <= pago_mensual:
            return 0
        elif salario >= 6 * pago_mensual:
            return 100
        else:
            return (salario - pago_mensual) / (6 * pago_mensual - pago_mensual) * 100
```

2. **Score de edad**
para este item se considera un aproach similar al de salario pero esta vez
el mapeo sera exponencial, es decir, si una persona tiene 18 o menos años
se le asignara un score de 0 y si tiene 70 un score de 100
mientras que interpolamos exponencialmente decreciente entre los puntos

```python
    import math

    """
    Funcion para ajustar peso a la edad
    la idea es que a partir de 70 asigne cercano a 0
    """
    def calcular_puntaje_edad(edad):
        if edad <= 18:
            return 100
        else:
            k = math.log(100) / (100 - 18)
            return 100 * math.exp(-k * (edad - 18))
```

3. **Score de ahorros**
El aproach es identico al del salario, es decir calculamos el valor del pie
y ajustamos linealmente el valor del score.

```python
    def calcular_puntaje_ahorros(savings, down_payment):
        """
        Funcion que asigna valor a tus ahorros
        si tienes ahorrado la mitad del pie
        asigna 0
        si tienes ahorrado 8 veces el pie 
        asigna 100, e interpola lineal
        """
        if savings <= down_payment / 2:
            return 0
        elif savings >= 8 * down_payment:
            return 100
        else:
            return (savings - down_payment / 2) / (8 * down_payment - down_payment / 2) * 100

```

4. **Score de mensajes**
El aproach es identico al del salario, es decir calculamos la
cantidad de mensajes y ajustamos linealmente el valor del score.

```python
    def calcular_puntaje_ahorros(savings, down_payment):
        """
        Funcion que asigna valor a tus ahorros
        si tienes ahorrado la mitad del pie
        asigna 0
        si tienes ahorrado 8 veces el pie 
        asigna 100, e interpola lineal
        """
        if savings <= down_payment / 2:
            return 0
        elif savings >= 8 * down_payment:
            return 100
        else:
            return (savings - down_payment / 2) / (8 * down_payment - down_payment / 2) * 100

```

4. **Score de deudas**
Para definir el score de deudas, es necesario preguntarse si corresponde hacer un analisis mas exaustivo.
Para ello se consideran 3 datos.

- Las deudas tienen un horizonte de tiempo, es decir, es mas "grave" si es mas antigua.
- Es dificil asociar las deudas a un departamento tan facilmente como se asocia el salario a un
departamento ya que, una deuda no compra directamente un departamento.
- Al no poder asociar las deudas tan facilmente a un departamento no tenemos asociaciones absolutas
que podemos implementar.

Para abordar estas problematicas vamos a implementar una solucion basada en los datos de la poblacion:

- Primero estandarizamos los datos en una distribucion normal basado en la media y la desviacion estandar 
de los datos disponibles
- Luego ajustamos con una funcion

$$ f(x) = sgn(x)log(1+|x|)$$

Esta funcion tiene un comportamiento exponencial al inicio y luego satura al final sin
ser asintotica. En teoria una deuda podria tener una
antiguedad infinita entonces hay que asignarle un valor estrictamente creciente
pero no tan "severo" como un crecimiento lineal o estrictamente exponencial
mientras que al inicio de adquirir la deuda se puede ser mas estricto. 


```python
    def calcular_puntaje_ahorros(savings, down_payment):
        """
        Funcion que asigna valor a tus ahorros
        si tienes ahorrado la mitad del pie
        asigna 0
        si tienes ahorrado 8 veces el pie 
        asigna 100, e interpola lineal
        """
        if savings <= down_payment / 2:
            return 0
        elif savings >= 8 * down_payment:
            return 100
        else:
            return (savings - down_payment / 2) / (8 * down_payment - down_payment / 2) * 100

```
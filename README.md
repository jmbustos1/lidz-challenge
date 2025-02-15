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
Para este ítem, es necesario asumir el interés por cierto departamento. 
Imaginemos uno de 3000 UF con un pie de 20%. Luego de contar con ese supuesto, 
es necesario realizar el cálculo de cada cuota, el cual se muestra a continuación:


$$\text{Pago Mensual} = \frac{\text{Monto del Préstamo} \times \text{Tasa de Interés Mensual}}{1 - (1 + \text{Tasa de Interés Mensual})^{-\text{Número de Pagos}}}$$

Luego la capacidad de pago se da calculando un factor
$$\text{Cuota} = \frac{\text{Salario}}{Pago Mensual} $$

Finalmente, se ajusta linealmente el factor tal que, 
si alguien tiene un salario 8 veces mayor a la cuota, 
se le asigna 100, y si es igual, entonces es 0


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
Para este ítem, se considera un enfoque similar al del salario, 
pero esta vez el mapeo será exponencial. Es decir, si una persona 
tiene 18 años o menos, se le asignará un puntaje de 0, y si tiene 70 años, 
un puntaje de 100, mientras que interpolamos exponencialmente decreciente entre esos puntos.

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
El enfoque es idéntico al del salario. Es decir, 
calculamos el valor del pie y ajustamos linealmente el valor del puntaje.

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
El enfoque es idéntico al del salario. Es decir, 
calculamos la cantidad de mensajes y ajustamos linealmente el valor del puntaje.

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
Para definir el puntaje de deudas, es necesario preguntarse si corresponde hacer un análisis más exhaustivo. Para ello, se consideran tres datos:

- Las deudas tienen un horizonte de tiempo; es decir, es más "grave" si es más antigua.
- Es difícil asociar las deudas a un departamento tan fácilmente como se asocia el salario a un departamento, ya que una deuda no compra directamente un departamento.
- Al no poder asociar las deudas tan fácilmente a un departamento, no tenemos asociaciones absolutas que podamos implementar.
Para abordar estas problemáticas, vamos a implementar una solución basada en los datos de la población:

- Primero, estandarizamos los datos en una distribución normal basada en la media y la desviación estándar de los datos disponibles.
Luego, ajustamos con una función adecuada.


$$ f(x) = sgn(x)log(1+|x|)$$

Esta función tiene un comportamiento exponencial al inicio y luego se satura al final sin ser asintótica. En teoría, una deuda podría tener una antigüedad infinita, por lo tanto, hay que asignarle un valor estrictamente creciente, pero no tan "severo" como un crecimiento lineal o estrictamente exponencial, mientras que al inicio de adquirir la deuda se puede ser más estricto.

- Finalmente, escalamos los valores entre 0 y 100, integramos para cada banco y obtenemos el riesgo.


4. **Integracion**
Teniendo cada puntaje, finalmente se procede a realizar 
una suma ponderada asignando pesos a cada deuda. En este caso, tomamos:

- 20% score de ahorro
- 20% score de deuda
- 30% score de salario
- 20% score de deudas
- 10% score de mensajes


## Discusion
Si bien es cierto que estos algoritmos sirven en un inicio cuando es necesario empezar a procesar clientes, a futuro, a medida que se recopilan más datos, podemos usar el análisis de ellos junto con el aprendizaje de máquinas para generar mejores estimaciones del puntaje de los clientes, evaluando si cierto cliente con ciertos datos asociados compró o no un departamento.

Por ejemplo, un cliente con un conjunto de datos X compró un departamento y otro no. Así, juntamos un conjunto de datos para generar un algoritmo y asignamos otro conjunto de datos como entrenamiento. A medida que los datos crecen, comparamos la eficiencia de los algoritmos. Si la teoría funciona, deberíamos eventualmente encontrar pesos que funcionen mejor que el algoritmo propuesto.
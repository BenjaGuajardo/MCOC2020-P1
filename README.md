# MCOC2020-P1

![Trayectoria para distintos vientos](https://user-images.githubusercontent.com/69161061/91070593-eeddea80-e604-11ea-90df-661c71c10bdf.png)

## Primeras predicciones con la EDM básica del satélite

+ En la figura 1 se pueden observar las distintas historias de tiempo. Donde se puede ver que x(t) junto con y(t) oscilan entre la distancia máxima de cada uno y se puede notar que la órbita es elíptica al comparar estos dos. También se observa que z(t) permanece constante en 0, esto se debe a que la órbita se encuentra en el plano xy, por lo que permanece en todo momento en el 0 del eje z.

![figura 1](https://user-images.githubusercontent.com/69161061/91486872-dd9e1380-e87a-11ea-98eb-3501cc1bc925.png)

+ En la figura 2 se observa r(t) vs t. Se puede notar que el satélite orbita por sobre la atmósfera, lo que evita que este caiga. La velocidad inicial mínima requerida fue calculada mediante tanteo, donde se obtuvo como resultado vt = 24.550,55 km/h. 

![figura 2](https://user-images.githubusercontent.com/69161061/91486876-e0006d80-e87a-11ea-9655-78e2cf788a8d.png)![Figure_2_zoom](https://user-images.githubusercontent.com/69161061/91487995-a4ff3980-e87c-11ea-82fc-f970e7d4d79f.png)

+ Finalmente, en la figura 3 se puede observar las órbitas del satélite en el plano xy, donde se pueden notar dos órbitas completas, que fueron realizadas en 3.31 horas (también calculado mediante tanteo).

![figura 3](https://user-images.githubusercontent.com/69161061/91486880-e0990400-e87a-11ea-87d2-3e0f904867b1.png)![Figure_3_zoom](https://user-images.githubusercontent.com/69161061/91487996-a6c8fd00-e87c-11ea-99f8-b24595ab2782.png)

## Estudio de convergencia Método de Euler

+ Para el estudio de convergencia del método de Euler, se comparó la solución real de la ecuacion diferencial de oscilamiento armónico con las soluciones que se obtuvieron al utilizar la función odeint de scipy y el método de Euler con distintas subdivisiones. El resultado se puede observar en la siguiente figura:

![Entrega4](https://user-images.githubusercontent.com/69161061/91782656-b5d8e380-ebcb-11ea-9079-3304d300d470.png)

+ A simple vista se puede notar que mientras mayor sea el Nsubdivisiones, el resultado converge primero a la solución real. Y en el caso contrario, como lo es el caso de "eulerint 1", si es menor el paso entonces menor es la precisión del método. Como era de esperar, "odeint" y "eulerint 100" se asemejan bastante a la solución real, pero no resulta completamente igual.

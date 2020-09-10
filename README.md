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

+ Para el estudio de convergencia del método de Euler, se comparó la solución real de la ecuacion diferencial del oscilador armónico con las soluciones que se obtuvieron al utilizar la función odeint de scipy y el método de Euler con distintas subdivisiones. El resultado se puede observar en la siguiente figura:

![Entrega4](https://user-images.githubusercontent.com/69161061/91782656-b5d8e380-ebcb-11ea-9079-3304d300d470.png)

+ A simple vista se puede notar que mientras mayor sea el Nsubdivisiones, el resultado converge primero a la solución real. Y en el caso contrario, como lo es el caso de "eulerint 1", si es menor el paso entonces menor es la precisión del método. Como era de esperar, "odeint" y "eulerint 100" se asemejan bastante a la solución real, pero no resulta completamente igual.

## Mejoras al modelo y estudio de convergencia

+ A continuación se encuentra la posición (x,y,z) en el tiempo del vector de estado de Sentinel 1A/B que me fue asignado.

![pregunta1](https://user-images.githubusercontent.com/69161061/92330787-1cd11f00-f048-11ea-8f4e-1978c554a1bb.png)

+  Usando la condición inicial del archivo OSV, se cmoparó la solución entre odeint y eulerint (Nsubdiviciones=1).

![pregunta2](https://user-images.githubusercontent.com/69161061/92330833-70dc0380-f048-11ea-8f6e-59265cf2b61d.png)

  + Como se puede apreciar en el gráfico, la deriva máxima alcanzada al final de las 24 horas es de 20.879,4 km.

    + Odeint demoró 0,2855 s
    + Eulerint demoró 0.6838 s

+ ¿Cuantas subdivisiones hay que usar para que la predicción con eulerint al final del tiempo esté en menos de un 1% de error? Grafique la deriva en el tiempo. Comente con respecto del tiempo de ejecución de eulerint ahora. 

  + Error según Nsubdivisiones.
  
    + N = 1 : 280% ; Tiempo de ejecución eulerint = 0.6838 s
    + N = 100 : 140% ; Tiempo de ejecución eulerint = 63.3434 s
    + N = 200 : 80% ; Tiempo de ejecución eulerint = 127.8157 s
    + N = 500 : 30% ; Tiempo de ejecución eulerint = 324.3962 s
    + N = 1000 : 20% ; Tiempo de ejecución eulerint = 625.7143 s
    
  + Deriva Nsubdivisiones = 1000
  
  ![pregunta3_N1000](https://user-images.githubusercontent.com/69161061/92331062-1e034b80-f04a-11ea-89dd-747fe0ee4e9f.png)
  
    + No fue posible llegar al 1% de error debido al excesivo tiempo de ejecución que demoraba eulerint con Ns mayores, por esto es que solamente llegué a N = 1000, donde la deriva máxima disminuyó a 1135,7 km (20% de error).

+ Se implementaron las correcciones J2 y J3, para obtener una mayor presición en la predicción.
  
  + En cuanto a la deriva entre euler y odeint, la situación no cambia mucho debido a que ambos se vuelven más precisos pero la diferencia entre estos sigue siendo similiar al caso anterior, llegando a una deriva máxima de 20.857,6 km.
  
![pregunta4_deriva](https://user-images.githubusercontent.com/69161061/92331200-548d9600-f04b-11ea-8e85-d5a42792854c.png)

  + Donde se nota la mejora es en la comparación entre la posición predicha y la real.
    
    + Grafico de posiciones. Se puede observar que la posición predicha (naranja) se acerca bastante a la real (azul), notándose una leve diferencia al final de las 24 horas.
    
    ![comparacionP4](https://user-images.githubusercontent.com/69161061/92331360-69b6f480-f04c-11ea-9fae-a756501a94d8.png)
    
    + En el siguiente gráfico se puede ver que la deriva máxima disminuye considerablemente de los 1841.8, calculados en la entrega3, a 226,6 km por el hecho de haber implementado J2 y J3.
    
    ![deriva_odeint](https://user-images.githubusercontent.com/69161061/92331234-a20a0300-f04b-11ea-82f3-5d3bb7d07470.png)
  
    + El código demora 2.26 s (considera cálculo de odeint, deriva y gráficos).

+ La orbita final predicha en 3 dimensiones es la siguiente

![3d](https://user-images.githubusercontent.com/69161061/92331497-5eb09400-f04d-11ea-9a83-5634ac6e0f56.png)


## Entrega Final
+ Mejoras implementadas:
  + Corregí errores en las correcciones J3 y J4, ya que había evaluado en las coordenadas iniciales y no transformadas mediante la matriz R.
  + Agregué más decimales a los valores de Ω, J3 y J4.
  + Cambié G * M = μ
  + Agregué las correcciones J4 y J5, utilizando algebra simbólica, mediante simpy.
+ Gracias a estas mejoras, principalmente a la adición de decimales las constantes mencionadas, logré una mejora significativa en la corrección, pasando de los cientos de kilómetros a sólo decenas e incluso menos.

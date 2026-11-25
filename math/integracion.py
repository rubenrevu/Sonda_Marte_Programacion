##En este archivo tenemos los metodos de integracion numerica
import numpy as np
#Por trapecios

def my_trapecio (f,a,b): #De datos requiere una funcion, un inicio y un final (es uno definido)
    n = round((b-a)/0.001) #Numero de trapecios PREGUNTAR INTERVALO EN CLASE e^(-15) es contraproducente segun claude, 0,001 puesto de manera temporal
    if n < 1:
        raise ValueError("El intervlo para integrar es mas pequeño que el ancho de nuestro trapecio") 
    #Sacamos los puntos en el eje x para cada trapecio
    x = a + 0.001 * np.arange(n+1) #CAMBIAR 0.001 
    y = f(x) #Sacams la altura de cada trapecio
    #Aplicamos la formula
    return (0.001 / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])  #CAMBIAR 0.001


##En este archivo tenemos los metodos de integracion numerica
import numpy as np
#Por trapecios

def my_trapecio (f,a,b): #De datos requiere una funcion, un inicio y un final (es uno definido)
    n = round((b-a)/dx) #Numero de trapecios PREGUNTAR INTERVALO EN CLASE e^(-15) es contraproducente segun claude, dx puesto de manera temporal
    if n < 1:
        raise ValueError("El intervlo para integrar es mas pequeño que el ancho de nuestro trapecio") 
    #Sacamos los puntos en el eje x para cada trapecio
    x = a + dx * np.arange(n+1) #CAMBIAR 0.001 
    y = f(x) #Sacams la altura de cada trapecio
    #Aplicamos la formula
    return (dx / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])  #CAMBIAR 0.001


#Por simpson

def my_simpson (f,a,b): #Mismos datos, funcion, inicio y final
    n = nodos #PREGUNTAR EN CLASE, EL NUMERO DE NODOS DEBE SER IMPAR 
    x = a + dx * np.arange(n+1) #CAMBIAR dx
    ##Ahi arriba estan puestos n e intervalos aleatorios, no estan relacionados (se relacionan con el espacio de a,b) ni cumplen, REVISAR
    y = f(x)
    return (dx/ 3) * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]) + y[-1])
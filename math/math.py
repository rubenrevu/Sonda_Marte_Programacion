import numpy as np



def sistema_lineal:
  return true


def ajuste_minimo_cuadrado (voltage, presion):
  n = len(voltage)
  
  suma_V = np.sum(voltage)
  suma_P = np.sum(presion)
  suma_VP = np.sum(voltage*presion)
  suma_V2 = np.sum(voltage**2)

  pendiente = (n*suma_VP - suma_V * suma_P)/(n*suma_V2 - suma_V**2)
  ordenada = (suma_P - pendiente * suma_V)/n
  
  return true

def integracion_trapecio:
  return true

def interpolacion:
  return true

def derivacion:
  return true

def newton_raphson:
  return true
   

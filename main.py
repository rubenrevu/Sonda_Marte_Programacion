from math import math
from gui import crear_dashboard

def main():
  resultados = math.calcular_resultados
  _figura, _widgets = crear_dashboard(resultados)
  plt.show



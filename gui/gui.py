
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider

#estas funciones las rellenamos nosotros cuando tengamos los calculos hechos, esto es como una plantilla
def graficar_1(ax):
    pass


def graficar_2(ax):
    pass


def graficar_3(ax):
    pass


def graficar_4(ax):
    pass


def graficar_5(ax):
    pass


def graficar_6(ax, v_objetivo):
    # v_objetivo [m/s] es el valor actual del slider (300 a 1000)
    pass


FUNCIONES = [
    graficar_1,
    graficar_2,
    graficar_3,
    graficar_4,
    graficar_5
]

ETIQUETAS = [
    "1. Balance de masas de propelente\n Sistema Lineal",
    "2. Calibracion del sensor de presion dinamica\n Regresion Lineal",
    "3. Reconstruccion de la trayectoria\n Integracion Numerica",
    "4. Estimacion de la densidad atmosferica\n Interpolacion Numerica",
    "5. Calculo de aceleracion estructural\n Derivacion Numerica",
    "6. Instante critico del vuelo\n Ecuacion no Lineal"
]



fig = plt.figure(figsize=(12, 7))

ax_grafica = fig.add_axes([0.30, 0.20, 0.65, 0.70])
ax_radio = fig.add_axes([0.03, 0.40, 0.18, 0.40])
ax_slider = fig.add_axes([0.38, 0.07, 0.50, 0.04])

radio = RadioButtons(ax_radio, ETIQUETAS)

slider = Slider(
    ax_slider,
    "v_objetivo [m/s]",
    300,
    1000,
    valinit=340,
    valstep=1
)

ax_slider.set_visible(False)


def actualizar(_=None):
    #Limpia el eje y llama a la funcion del boton elegido

    indice = ETIQUETAS.index(radio.value_selected)

    ax_grafica.clear()

    if indice == 5: #caso epsecial para el slider
        ax_slider.set_visible(True)
        graficar_6(ax_grafica, slider.val)

    else:
        ax_slider.set_visible(False)
        FUNCIONES[indice](ax_grafica)

    fig.canvas.draw_idle()


radio.on_clicked(actualizar)
slider.on_changed(actualizar)

plt.show()

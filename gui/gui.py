import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, RadioButtons, Slider

from calculos import calculos as calc
from datos import datos

ETIQUETAS_VISTAS = (
    "1. Balance de masas\n    (sistema lineal)",
    "2. Calibracion Pitot\n    (regresion lineal)",
    "3. Altitud h(t)\n    (integracion)",
    "4. Densidad rho(t)\n    (interpolacion)",
    "5. Aceleracion a(t)\n    (derivacion)",
    "6. Instante critico\n    (Newton-Raphson)",
)
INDICE_APARTADO_6 = len(ETIQUETAS_VISTAS) - 1

ESTILO_CAJA_TEXTO = {"boxstyle": "round,pad=0.5", "facecolor": "#fffbe6",
                         "edgecolor": "#b8a95c", "alpha": 0.95}

def _anadir_texto(ax, texto, x=0.02, y=0.97, ha="left", va="top"):
    """Escribe un recuadro de texto dentro del lienzo, en coordenadas relativas."""
    ax.text(x, y, texto, transform=ax.transAxes, ha=ha, va=va, fontsize=9,
            bbox=ESTILO_CAJA_TEXTO, family="monospace", multialignment="left", zorder=10)

def dibujar_masas(ax, resultados, **_):
    m1, m2, m3 = resultados["masas"]
    barras = ax.bar(["Tanque 1\n(m1)", "Tanque 2\n(m2)", "Tanque 3\n(m3)"],
                    resultados["masas"], color=["#3b78b5", "#e08a2c", "#4f9d69"],
                    label="Masa de propergol")
    ax.bar_label(barras, labels=[f"{m:.2f} kg" for m in resultados["masas"]],
                 padding=3, fontsize=9)
    ax.axhline(datos.b_masas[0] / 3, color="gray", ls="--", lw=1,
               label="Reparto uniforme (16 666.67 kg)")
    ax.set_ylim(0, 1.6 * max(resultados["masas"]))
    ax.set_ylabel("Masa de propergol [kg]")
    ax.set_title("Apartado 1 - Balance de masas de propelente (A·m = b)")
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.4)
    _anadir_texto(
        ax,
        f"m1 = {m1:10.2f} kg\nm2 = {m2:10.2f} kg\nm3 = {m3:10.2f} kg\n"
        f"Suma = {m1 + m2 + m3:.2f} kg\n\n"
        "Significado: el tanque 1 contiene el 43 % del\n"
        "propergol (2·m2) y el 3 supera en 6 667 kg al 2.\n"
        "Los 50 t son un orden de magnitud realista para\n"
        "una primera etapa de lanzador pesado (10^4-10^5 kg).")


  def dibujar_calibracion(ax, resultados, **_):
    ajuste = resultados["ajuste"]
    voltaje_fino = np.linspace(0, 5, 100)
    ax.scatter(datos.V_sensor, datos.P_sensor, color="#c0392b", zorder=3,
               label="Datos de laboratorio")
    ax.plot(voltaje_fino,
            calc.evaluar_recta(voltaje_fino, ajuste.pendiente, ajuste.ordenada),
            color="#2c5aa0",
            label=rf"Ajuste: $P = {ajuste.pendiente:.3f}\,V {ajuste.ordenada:+.3f}$")
    ax.set_xlabel("Voltaje del sensor, V [V]")
    ax.set_ylabel("Presion dinamica, P [kPa]")
    ax.set_title("Apartado 2 - Calibracion del sensor (minimos cuadrados)")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.4)
    _anadir_texto(
        ax,
        f"theta1 = {ajuste.pendiente:.4f} kPa/V\n"
        f"theta0 = {ajuste.ordenada:+.4f} kPa\n"
        f"R^2    = {ajuste.r_cuadrado:.5f}\n"
        f"|residuo| max = {ajuste.residuo_max:.3f} kPa\n\n"
        "Significado: cada voltio equivale a ~21 kPa de\n"
        "presion dinamica; ordenada ~0 (sensor sin offset\n"
        "apreciable). Orden de magnitud coherente con q\n"
        "de decenas de kPa en el ascenso (q_max).",
        x=0.98, y=0.04, ha="right", va="bottom")

def dibujar_altitud(ax, resultados, **_):
    altitud_km = resultados["altitud"] / 1e3
    ax.plot(datos.t_vuelo, altitud_km, color="#2c5aa0",
            label=r"$h(t)=\int_0^t v\,d\tau$ (trapecios)")
    ax.axhline(datos.altitudes_tab[-1] / 1e3, color="gray", ls="--", lw=1,
               label="Limite superior de la tabla atmosferica (30 km)")
    ax.set_xlabel("Tiempo, t [s]")
    ax.set_ylabel("Altitud, h [km]")
    ax.set_title("Apartado 3 - Reconstruccion de la trayectoria (altitud)")
    ax.legend(loc="center left")
    ax.grid(alpha=0.4)
    _anadir_texto(
        ax,
        f"h(120 s) = {resultados['altitud'][-1]:.1f} m  "
        f"({altitud_km[-1]:.1f} km)\n"
        "h(0 s)   = 0 m\n\n"
        "Significado: tras 2 min la sonda esta a ~136 km,\n"
        "en el espacio (linea de Karman: 100 km). Valor\n"
        "algo alto pero del orden de un lanzador pesado:\n"
        "el perfil logistico simulado llega a 2.4 km/s.",
        x=0.02, y=0.97)


def dibujar_densidad(ax, resultados, **_):
    tiempo, densidad = datos.t_vuelo, resultados["densidad"]
    fuera = resultados["fuera_tabla"]
    ax.plot(tiempo, densidad, color="#4f9d69", label=r"$\rho(t)$ interpolada (lineal)")
    if fuera.any():
        t_limite = tiempo[fuera.argmax()]
        ax.axvspan(t_limite, tiempo[-1], color="#e74c3c", alpha=0.15,
                   label="Fuera de tabla (h > 30 km): rho saturada")
    ax.set_xlabel("Tiempo, t [s]")
    ax.set_ylabel(r"Densidad del aire, $\rho$ [kg/m$^3$]")
    ax.set_title("Apartado 4 - Densidad atmosferica a lo largo del vuelo")
    ax.legend(loc="center right")
    ax.grid(alpha=0.4)
    t_fuera = tiempo[fuera.argmax()] if fuera.any() else float("nan")
    _anadir_texto(
        ax,
        f"rho(0 s)   = {densidad[0]:.4f} kg/m^3\n"
        f"rho(120 s) = {densidad[-1]:.4f} kg/m^3\n"
        f"Fuera de tabla desde t = {t_fuera:.0f} s\n\n"
        "Significado: la densidad cae 2 ordenes de magnitud\n"
        "(0.1 % de rho_0 aprox.) al ascender: la resistencia\n"
        "aerodinamica desaparece. AVISO: por encima de 30 km\n"
        "np.interp no extrapola y mantiene 0.018 kg/m^3; la\n"
        "densidad real a 100 km es ~1e-7 kg/m^3, mucho menor.",
        x=0.98, y=0.97, ha="right")



def dibujar_aceleracion(ax, resultados, **_):
    tiempo, aceleracion = datos.t_vuelo, resultados["aceleracion"]
    indice_max = int(np.argmax(np.abs(aceleracion)))
    ax.plot(tiempo, aceleracion, color="#c0392b", label="Diferencias finitas")
    ax.plot(tiempo, calc.aceleracion_logistica(tiempo), "k--", lw=1,
            label="Derivada analitica (validacion)")
    ax.plot(tiempo[indice_max], aceleracion[indice_max], "o", color="#2c5aa0",
            label="Maximo")
    ax.set_ylim(0, 1.75 * aceleracion.max())  # hueco superior para el recuadro
    ax.set_xlabel("Tiempo, t [s]")
    ax.set_ylabel(r"Aceleracion axial, $a$ [m/s$^2$]")
    ax.set_title("Apartado 5 - Aceleracion estructural (diferencias finitas)")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.4)
    a_max = aceleracion[indice_max]
    _anadir_texto(
        ax,
        f"a_max = {a_max:.3f} m/s^2 = {a_max / datos.G0:.2f} g\n"
        f"en t = {tiempo[indice_max]:.0f} s\n"
        f"a(0 s)   = {aceleracion[0]:.3f} m/s^2 (progresiva)\n"
        f"a(120 s) = {aceleracion[-1]:.3f} m/s^2 (regresiva)\n"
        f"Error max vs analitica = {resultados['error_aceleracion'].max():.3f} m/s^2\n\n"
        "Significado: ~3 g de carga axial maxima, del orden\n"
        "de los limites de lanzadores (3-4 g) para la carga util.",
        x=0.02, y=0.97)



def dibujar_critico(ax, resultados, velocidad_objetivo=datos.V_OBJETIVO_DEFECTO, **_):
    solucion = calc.resolver_apartado_6(velocidad_objetivo, resultados)
    newton, biseccion = solucion["newton"], solucion["biseccion"]
    t_fino = np.linspace(0, 120, 600)
    ax.plot(t_fino, calc.velocidad_logistica(t_fino), color="#2c5aa0",
            label="v(t) teorica (logistica)")
    ax.plot(datos.t_vuelo[::5], datos.v_vuelo[::5], ".", color="gray", ms=5,
            label="Telemetria (1 de cada 5 s)")
    ax.axhline(velocidad_objetivo, color="#e08a2c", ls="--",
               label=rf"$v_{{objetivo}}$ = {velocidad_objetivo:.0f} m/s")
    ax.axvline(newton.tiempo_critico, color="#c0392b", ls=":", lw=1)
    ax.plot(newton.tiempo_critico, velocidad_objetivo, "o", color="#c0392b", ms=9,
            zorder=5, label=rf"$t_{{crit}}$ = {newton.tiempo_critico:.3f} s")
    ax.set_xlabel("Tiempo, t [s]")
    ax.set_ylabel("Velocidad, v [m/s]")
    ax.set_title("Apartado 6 - Instante critico: v(t) = v_objetivo "
                 "(Newton-Raphson)")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.4)
    _anadir_texto(
        ax,
        f"t_crit = {newton.tiempo_critico:.6f} s\n"
        f"Iteraciones Newton = {newton.iteraciones}  "
        f"(biseccion: {biseccion.iteraciones})\n"
        f"Residuo v(t_crit)-v_obj = {newton.residuo:.1e} m/s\n"
        f"|t_Newton - t_biseccion| = "
        f"{abs(newton.tiempo_critico - biseccion.tiempo_critico):.1e} s\n"
        f"Mach = {solucion['mach']:.2f}   h(t_crit) = "
        f"{solucion['altitud_critica'] / 1e3:.2f} km\n\n"
        f"Significado: el cohete alcanza {velocidad_objetivo:.0f} m/s "
        f"a los {newton.tiempo_critico:.1f} s,\n"
        "orden de decenas de s como en lanzadores reales.\n"
        "Punto inicial t0 = 60 s: inflexion de v(t) (pendiente\n"
        "maxima) con v(60)=1132 m/s > 1000 m/s => f(t0)>0 y\n"
        "Newton converge monotonamente en todo el slider.",
        x=0.02, y=0.97)


FUNCIONES_VISTA = (dibujar_masas, dibujar_calibracion, dibujar_altitud,
                   dibujar_densidad, dibujar_aceleracion, dibujar_critico)

def crear_dashboard(resultados):
    """Crea la figura con todos los widgets y devuelve (fig, widgets)."""
    fig = plt.figure(figsize=(14, 8))
    fig.suptitle("Panel de control de telemetria - Ares-I (sonda a Marte)",
                 fontsize=14, fontweight="bold")
    ax = fig.add_axes([0.30, 0.20, 0.67, 0.70])

    ax_radio = fig.add_axes([0.02, 0.38, 0.22, 0.52])
    ax_radio.set_title("Apartado", fontsize=11)
    radio = RadioButtons(ax_radio, ETIQUETAS_VISTAS, active=0)

    ax_anterior = fig.add_axes([0.02, 0.28, 0.10, 0.06])
    ax_siguiente = fig.add_axes([0.14, 0.28, 0.10, 0.06])
    boton_anterior = Button(ax_anterior, "< Anterior")
    boton_siguiente = Button(ax_siguiente, "Siguiente >")

    ax_slider = fig.add_axes([0.38, 0.07, 0.50, 0.04])
    slider = Slider(ax_slider, "v_objetivo [m/s]  ", datos.V_OBJETIVO_MIN,
                    datos.V_OBJETIVO_MAX, valinit=datos.V_OBJETIVO_DEFECTO,
                    valstep=1.0)

    estado = {"indice": 0}

    def refrescar():
        """Limpia el eje y pinta la vista activa (el slider solo en el apartado 6)."""
        ax.clear()
        FUNCIONES_VISTA[estado["indice"]](ax, resultados,
                                          velocidad_objetivo=slider.val)
        ax_slider.set_visible(estado["indice"] == INDICE_APARTADO_6)
        fig.canvas.draw_idle()

    def al_elegir_apartado(etiqueta):
        estado["indice"] = ETIQUETAS_VISTAS.index(etiqueta)
        refrescar()

    def al_mover_slider(_valor):
        if estado["indice"] == INDICE_APARTADO_6:
            refrescar()

    def desplazar(paso):
        radio.set_active((estado["indice"] + paso) % len(ETIQUETAS_VISTAS))

    radio.on_clicked(al_elegir_apartado)
    slider.on_changed(al_mover_slider)
    boton_anterior.on_clicked(lambda _evento: desplazar(-1))
    boton_siguiente.on_clicked(lambda _evento: desplazar(+1))

    refrescar()
    # Se devuelven los widgets: matplotlib los desconecta si se recolectan.
    widgets = {"radio": radio, "slider": slider, "anterior": boton_anterior,
                   "siguiente": boton_siguiente, "estado": estado, "refrescar": refrescar}
    return fig, widgets


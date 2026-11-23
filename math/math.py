def calcular_resultados():
    #"""Ejecuta los apartados 1-5 sobre los datos y devuelve un diccionario."""
    #tiempo, velocidad = datos.t_vuelo, datos.v_vuelo
    #altitud = reconstruir_altitud(tiempo, velocidad)
    #aceleracion = calcular_aceleracion(tiempo, velocidad)
    return {
        "masas": 1,1,1#resolver_balance_masas(datos.A_masas, datos.b_masas),
        "ajuste": 1.0,1.0,1.0,1.0#ajustar_calibracion(datos.V_sensor, datos.P_sensor),
        "altitud": 1#altitud,
        "densidad": 1.0#interpolar_densidad(altitud, datos.altitudes_tab,
                                        #datos.densidades_tab),
        "fuera_tabla": true#mascara_fuera_de_tabla(altitud, datos.altitudes_tab),
        "aceleracion": 1#aceleracion,
        "error_aceleracion": 1#np.abs(aceleracion - aceleracion_logistica(tiempo)),
    }

"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import os

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    ruta_entrada = "files/input/solicitudes_de_credito.csv"
    ruta_salida = "files/output/solicitudes_de_credito.csv"

    carpeta_salida = os.path.dirname(ruta_salida)
    os.makedirs(carpeta_salida, exist_ok=True)

    tabla = pd.read_csv(ruta_entrada, sep=";", index_col=0)

    # 1. Eliminar valores nulos
    tabla.dropna(inplace=True)

    # 2. Estandarización y limpieza

    # Limpieza del monto
    tabla["monto_del_credito"] = (
        tabla["monto_del_credito"]
        .astype(str)
        .str.replace("$ ", "", regex=False)
        .str.replace(",", "")
        .astype(float)
    )

    # Columnas que requieren normalización de texto
    columnas_texto = [
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]

    for etiqueta in columnas_texto:
        tabla[etiqueta] = tabla[etiqueta].str.lower()
        tabla[etiqueta] = tabla[etiqueta].str.replace("-", "_")
        tabla[etiqueta] = tabla[etiqueta].str.replace(" ", "_")
        tabla[etiqueta] = tabla[etiqueta].str.replace("__", "_")

    # Columna sexo
    tabla["sexo"] = tabla["sexo"].str.lower()

    # Fecha con formatos mixtos
    tabla["fecha_de_beneficio"] = pd.to_datetime(
        tabla["fecha_de_beneficio"],
        dayfirst=True,
        format="mixed"
    )

    # 3. Eliminar duplicados
    tabla.drop_duplicates(inplace=True)

    # 4. Conversión final de tipos
    tabla["monto_del_credito"] = tabla["monto_del_credito"].astype(int)
    tabla["comuna_ciudadano"] = tabla["comuna_ciudadano"].astype(int)
    tabla["estrato"] = tabla["estrato"].astype(int)

    # Guardar con índice, separado por ;
    tabla.to_csv(ruta_salida, index=True, sep=";")

    return
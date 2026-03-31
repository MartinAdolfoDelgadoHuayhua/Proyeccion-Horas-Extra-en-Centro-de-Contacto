"""
preprocessing.py
----------------
Funciones de carga y limpieza del dataset de HHEE.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_raw(filepath: str | Path) -> pd.DataFrame:
    """Carga el CSV crudo y convierte la columna de período a datetime."""
    df = pd.read_csv(filepath)
    df['fecha'] = pd.to_datetime(df['periodo'] + '-01')
    df = df.sort_values('fecha').reset_index(drop=True)
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera variables derivadas sobre el dataframe cargado.
    Devuelve un nuevo DataFrame con índice de fecha mensual.
    """
    df = df.copy()
    df = df.set_index('fecha')

    df['hhee_per_llamada'] = (
        df['horas_extra_totales'] / df['volumen_llamadas_miles']
    ).round(4)

    df['costo_por_persona'] = (
        df['costo_hhee_soles'] / df['num_personas']
    ).round(2)

    df['quarter']    = df.index.quarter
    df['mes_nombre'] = df.index.strftime('%b')

    q75 = df['horas_extra_totales'].quantile(0.75)
    df['hhee_alta'] = (df['horas_extra_totales'] > q75).astype(int)

    return df


def check_quality(df: pd.DataFrame) -> None:
    """Imprime un reporte básico de calidad de datos."""
    nulls = df.isnull().sum()
    print("=== Reporte de calidad ===")
    print(f"Filas      : {len(df)}")
    print(f"Columnas   : {df.shape[1]}")
    print(f"Nulos total: {nulls.sum()}")
    if nulls.sum() > 0:
        print("\nColumnas con nulos:")
        print(nulls[nulls > 0])
    else:
        print("Sin valores nulos ✅")

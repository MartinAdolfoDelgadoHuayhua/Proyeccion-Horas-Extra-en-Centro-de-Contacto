"""
features.py
-----------
Ingeniería de variables para modelos supervisados y análisis de People Analytics.
"""

import pandas as pd
import numpy as np


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega variables de calendario útiles como regressores."""
    df = df.copy()
    df['mes_sin'] = np.sin(2 * np.pi * df.index.month / 12)
    df['mes_cos'] = np.cos(2 * np.pi * df.index.month / 12)
    df['trim_sin'] = np.sin(2 * np.pi * df.index.quarter / 4)
    df['trim_cos'] = np.cos(2 * np.pi * df.index.quarter / 4)
    df['es_fin_anio'] = df.index.month.isin([11, 12]).astype(int)
    df['es_inicio_anio'] = df.index.month.isin([1, 2]).astype(int)
    return df


def add_lag_features(df: pd.DataFrame, col: str, lags: list[int]) -> pd.DataFrame:
    """Agrega variables rezagadas (lag features) para una columna."""
    df = df.copy()
    for lag in lags:
        df[f'{col}_lag{lag}'] = df[col].shift(lag)
    return df


def add_rolling_features(
    df: pd.DataFrame, col: str, windows: list[int]
) -> pd.DataFrame:
    """Agrega medias móviles para una columna."""
    df = df.copy()
    for w in windows:
        df[f'{col}_ma{w}'] = df[col].rolling(w).mean()
    return df


def get_feature_matrix(
    df: pd.DataFrame,
    target: str = 'horas_extra_totales',
    lags: list[int] | None = None,
    rolling: list[int] | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Construye la matriz de features X e y para modelado supervisado.

    Returns
    -------
    X : pd.DataFrame con features
    y : pd.Series con el target
    """
    lags    = lags    or [1, 2, 3, 12]
    rolling = rolling or [3, 6]

    df = add_calendar_features(df)
    df = add_lag_features(df, target, lags)
    df = add_rolling_features(df, target, rolling)

    df = df.dropna()

    feature_cols = [
        'mes_sin', 'mes_cos', 'es_fin_anio', 'es_inicio_anio',
        'num_personas', 'ausentismo_pct', 'campania_activa',
    ] + [f'{target}_lag{l}' for l in lags] \
      + [f'{target}_ma{w}'  for w in rolling]

    available = [c for c in feature_cols if c in df.columns]
    return df[available], df[target]

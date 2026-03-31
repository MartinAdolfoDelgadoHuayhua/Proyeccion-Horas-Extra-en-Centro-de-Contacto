"""
models.py
---------
Wrappers ligeros para los modelos de series temporales usados en el proyecto.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX


def metricas(real: np.ndarray, pred: np.ndarray, nombre: str) -> dict:
    """Calcula MAE, RMSE, MAPE y R² para un par real/predicho."""
    mae  = mean_absolute_error(real, pred)
    rmse = np.sqrt(mean_squared_error(real, pred))
    mape = np.mean(np.abs((real - pred) / (real + 1e-9))) * 100
    r2   = r2_score(real, pred)
    return {
        'Modelo': nombre,
        'MAE':    round(mae, 1),
        'RMSE':   round(rmse, 1),
        'MAPE_%': round(mape, 1),
        'R2':     round(r2, 3),
    }


def fit_ets(
    series: pd.Series,
    trend: str = 'add',
    seasonal: str | None = None,
    seasonal_periods: int = 12,
) -> ExponentialSmoothing:
    """Ajusta un modelo Holt-Winters (ETS) a la serie dada."""
    model = ExponentialSmoothing(
        series,
        trend=trend,
        seasonal=seasonal,
        seasonal_periods=seasonal_periods if seasonal else None,
        initialization_method='estimated',
    ).fit(optimized=True)
    return model


def fit_sarima(
    series: pd.Series,
    order: tuple = (1, 1, 1),
    seasonal_order: tuple = (1, 0, 1, 12),
) -> SARIMAX:
    """Ajusta un modelo SARIMA a la serie dada."""
    model = SARIMAX(
        series,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit(disp=False)
    return model


def forecast_with_ci(
    model,
    n_periods: int,
    std_resid: float,
    z: float = 1.5,
) -> pd.DataFrame:
    """
    Genera una tabla de proyecciones con intervalo de confianza aproximado.

    Parameters
    ----------
    model   : modelo ETS o SARIMA ya ajustado
    n_periods : meses a proyectar
    std_resid : desviación estándar de los residuos del modelo
    z         : multiplicador para el IC (1.5 ≈ 85%, 1.96 ≈ 95%)
    """
    if hasattr(model, 'forecast'):
        pred = model.forecast(n_periods)
    else:
        pred = model.get_forecast(n_periods).predicted_mean

    df_out = pd.DataFrame({
        'yhat':    pred.values,
        'yhat_lower': np.maximum(pred.values - z * std_resid, 0),
        'yhat_upper': pred.values + z * std_resid,
    }, index=pred.index)

    return df_out

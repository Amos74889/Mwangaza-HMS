import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def predict_admissions():
    df = pd.read_csv("data/admissions.csv")
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    series = df['admissions']

    model = ARIMA(series, order=(1,1,1))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=7)

    return {
        "historical": series.tail(7).tolist(),
        "predicted": forecast.tolist(),
        "confidence": round(model_fit.bic, 2)
    }

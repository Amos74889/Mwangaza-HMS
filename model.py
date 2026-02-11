import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np
import os

# Get absolute base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "admission.csv")
MODEL_PATH = os.path.join(BASE_DIR, "hospital_model.pkl")


# Train model only if it doesn't already exist
def train_model():
    if os.path.exists(MODEL_PATH):
        print("Model already exists. Skipping training.")
        return

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("admission.csv not found in project root.")

    data = pd.read_csv(DATA_PATH)

    # Group by day_number and sum admissions
    data_grouped = data.groupby('day_number')['admissions'].sum().reset_index()

    X = data_grouped[['day_number']]
    y = data_grouped['admissions']

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved successfully.")


# Predict next 7 days
def predict_next_7_days():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file not found. Training may have failed.")

    data = pd.read_csv(DATA_PATH)
    data_grouped = data.groupby('day_number')['admissions'].sum().reset_index()

    last_day = data_grouped['day_number'].max()

    next_days = np.array(
        [last_day + i for i in range(1, 8)]
    ).reshape(-1, 1)

    model = joblib.load(MODEL_PATH)
    preds = model.predict(next_days)

    return [
        {
            "day": int(last_day + i),
            "predicted_admissions": float(preds[i])
        }
        for i in range(7)
    ]

import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

MODEL_PATH = "hospital_model.pkl"

# Train a simple model (Linear Regression) on admissions data
def train_model():
    data = pd.read_csv("data.csv")
    # For simplicity, train per department combined
    data_grouped = data.groupby('day_number')['admissions'].sum().reset_index()
    X = data_grouped[['day_number']]
    y = data_grouped['admissions']

    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved!")

# Predict next 7 days
def predict_next_7_days():
    data = pd.read_csv("data.csv")
    data_grouped = data.groupby('day_number')['admissions'].sum().reset_index()
    last_day = data_grouped['day_number'].max()
    next_days = np.array([last_day + i for i in range(1, 8)]).reshape(-1, 1)
    
    model = joblib.load(MODEL_PATH)
    preds = model.predict(next_days)
    confidence = [0.9] * 7  # placeholder confidence for each day
    
    return [
        {"day": int(last_day + i), "predicted_admissions": float(preds[i]), "confidence": confidence[i]}
        for i in range(7)
    ]

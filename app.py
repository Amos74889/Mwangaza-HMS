from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model import train_model, predict_next_7_days
import uvicorn
import os

app = FastAPI(title="Hospital Admission Prediction System")

# Templates for frontend
templates = Jinja2Templates(directory="templates")

# Static files for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup_event():
    # Train model at startup
    if not os.path.exists("hospital_model.pkl"):
        train_model()
    else:
        print("Model already exists. Skipping training.")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict")
def get_prediction():
    return {"next_7_days_predictions": predict_next_7_days()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

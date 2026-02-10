from flask import Flask, render_template, jsonify
from model import predict_admissions # type: ignore

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/predictions")
def api_predictions():
    results = predict_admissions()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("app/artifacts/model.pkl")
scaler = joblib.load("app/artifacts/scaler.pkl")


@app.route("/")
def home():
    return "Model API Running"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        features = [
            data["fixed acidity"],
            data["volatile acidity"],
            data["citric acid"],
            data["residual sugar"],
            data["chlorides"],
            data["free sulfur dioxide"],
            data["total sulfur dioxide"],
            data["density"],
            data["pH"],
            data["sulphates"],
            data["alcohol"]
        ]

        features = np.array([features])
        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)

        return jsonify({"prediction": float(prediction[0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
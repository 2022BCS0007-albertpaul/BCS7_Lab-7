import joblib
import numpy as np

# Load model and scaler
model = joblib.load("app/artifacts/model.pkl")
scaler = joblib.load("app/artifacts/scaler.pkl")

def predict(input_data):
    try:
        data = np.array([list(input_data.values())])
        data_scaled = scaler.transform(data)
        prediction = model.predict(data_scaled)
        print("Prediction:", prediction[0])
    except Exception as e:
        print("Error:", e)


# ----------------------------
# VALID INPUT
# ----------------------------
valid_input = {
    "fixed acidity": 7.4,
    "volatile acidity": 0.70,
    "citric acid": 0.00,
    "residual sugar": 1.9,
    "chlorides": 0.076,
    "free sulfur dioxide": 11.0,
    "total sulfur dioxide": 34.0,
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4
}

# ----------------------------
# INVALID INPUT (missing feature)
# ----------------------------
invalid_input = {
    "fixed acidity": 7.4,
    "volatile acidity": 0.70,
    "citric acid": 0.00,
    "residual sugar": 1.9,
    "chlorides": 0.076,
    "free sulfur dioxide": 11.0,
    # "total sulfur dioxide" missing
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4
}

print("Valid Input Test:")
predict(valid_input)

print("\nInvalid Input Test:")
predict(invalid_input)
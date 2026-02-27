import pandas as pd
import json
import os
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Ensure artifacts directory exists
os.makedirs("app/artifacts", exist_ok=True)

# Load dataset
DATA_PATH = "dataset/winequality.csv"
data = pd.read_csv(DATA_PATH, sep=';')

target_column = "quality"
X = data.drop(columns=[target_column])
y = data[target_column]

# Train-test split (40% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=42
)

# Standard Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Predict
y_pred = model.predict(X_test_scaled)

# Metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Save model
joblib.dump(model, "app/artifacts/model.pkl")
joblib.dump(scaler, "app/artifacts/scaler.pkl")

# Save metrics
metrics = {
    "mean_squared_error": mse,
    "r2_score": r2
}

with open("app/artifacts/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

# Print metrics
print("Model Evaluation Metrics")
print("------------------------")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R2 Score: {r2:.4f}")

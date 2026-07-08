import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder

os.makedirs("models", exist_ok=True)

# ----------------------------
# Load Dataset
# ----------------------------

df = pd.read_csv("dataset/crowd_dataset.csv")

# ----------------------------
# Encode Categorical Features
# ----------------------------

weather_encoder = LabelEncoder()
brand_encoder = LabelEncoder()
poi_encoder = LabelEncoder()

df["weather"] = weather_encoder.fit_transform(df["weather"])
df["brand"] = brand_encoder.fit_transform(df["brand"])
df["poi_level"] = poi_encoder.fit_transform(df["poi_level"])

# ----------------------------
# Features
# ----------------------------

X = df[[
    "hour",
    "weekday",
    "month",
    "holiday",
    "weather",
    "brand",
    "poi_level",
    "pump_count",
    "service_time"
]]

# ----------------------------
# Target
# ----------------------------

y = df["queue_length"]

# ----------------------------
# Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ----------------------------
# Model
# ----------------------------

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ----------------------------
# Evaluation
# ----------------------------

prediction = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    prediction
)

print()

print("Mean Absolute Error :", round(mae,2), "vehicles")

# ----------------------------
# Save Model
# ----------------------------

joblib.dump(
    model,
    "models/crowd_model.pkl"
)

joblib.dump(
    weather_encoder,
    "models/weather_encoder.pkl"
)

joblib.dump(
    brand_encoder,
    "models/brand_encoder.pkl"
)

joblib.dump(
    poi_encoder,
    "models/poi_encoder.pkl"
)

print()

print("Model Saved Successfully")

from fastapi import FastAPI
import pandas as pd

app = FastAPI(
    title="Vehicle CAN Monitoring API",
    description="API for simulated vehicle data and diagnostics",
    version="1.0"
)

DATA_FILE = "data/vehicle_log.csv"


def load_vehicle_data():
    return pd.read_csv(DATA_FILE)


@app.get("/")
def home():
    return {
        "message": "Vehicle Monitoring API is running"
    }


@app.get("/vehicle-data")
def vehicle_data():
    df = load_vehicle_data()
    return df.to_dict(orient="records")


@app.get("/anomalies")
def anomalies():
    df = load_vehicle_data()
    abnormal = df[df["Anomaly"] != "Normal"]
    return abnormal.to_dict(orient="records")


@app.get("/health")
def health():
    df = load_vehicle_data()

    return {
        "status": "running",
        "total_samples": len(df),
        "anomalies_detected": int(
            (df["Anomaly"] != "Normal").sum()
        )
    }

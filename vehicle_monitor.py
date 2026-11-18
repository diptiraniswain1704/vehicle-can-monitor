
import can
import cantools
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime


# Load the DBC database
db = cantools.database.load_file("vehicle.dbc")

# Get the CAN message definition
message = db.get_message_by_name("VehicleStatus")


# Simulated vehicle data
vehicle_samples = [
    {
        "VehicleSpeed": 0,
        "MotorRPM": 0,
        "BatteryVoltage": 420,
        "BatteryTemperature": 35
    },
    {
        "VehicleSpeed": 20,
        "MotorRPM": 1500,
        "BatteryVoltage": 418,
        "BatteryTemperature": 40
    },
    {
        "VehicleSpeed": 45,
        "MotorRPM": 3000,
        "BatteryVoltage": 415,
        "BatteryTemperature": 45
    },
    {
        "VehicleSpeed": 60,
        "MotorRPM": 4500,
        "BatteryVoltage": 370,
        "BatteryTemperature": 96
    },
    {
        "VehicleSpeed": 30,
        "MotorRPM": 2000,
        "BatteryVoltage": 368,
        "BatteryTemperature": 98
    }
]


records = []

# Create two virtual CAN bus endpoints
tx_bus = can.Bus(
    interface="virtual",
    channel="vehicle_demo"
)

rx_bus = can.Bus(
    interface="virtual",
    channel="vehicle_demo"
)

try:
    for sample in vehicle_samples:

        # Encode physical signals into CAN payload bytes
        payload = message.encode(sample)

        # Create CAN frame
        frame = can.Message(
            arbitration_id=message.frame_id,
            data=payload,
            is_extended_id=False
        )

        # Transmit CAN frame
        tx_bus.send(frame)

        # Receive CAN frame
        received = rx_bus.recv(timeout=2)

        if received is None:
            print("No CAN frame received")
            continue

        # Decode received CAN data using DBC
        decoded = db.decode_message(
            received.arbitration_id,
            received.data
        )

        record = {
            "Timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            **decoded
        }

        records.append(record)

        print("Received:", decoded)

finally:
    tx_bus.shutdown()
    rx_bus.shutdown()


# Convert records into a DataFrame
df = pd.DataFrame(records)

# Detect abnormal conditions
previous_voltage = None
anomaly_results = []

for _, row in df.iterrows():

    flags = []

    if row["BatteryTemperature"] >= 90:
        flags.append("High Battery Temperature")

    if (
        previous_voltage is not None
        and previous_voltage - row["BatteryVoltage"] >= 30
    ):
        flags.append("Sudden Voltage Drop")

    anomaly_results.append(
        "; ".join(flags) if flags else "Normal"
    )

    previous_voltage = row["BatteryVoltage"]


df["Anomaly"] = anomaly_results

# Create output folders
Path("data").mkdir(exist_ok=True)
Path("screenshots").mkdir(exist_ok=True)

# Save vehicle data
df.to_csv("data/vehicle_log.csv", index=False)

print("\nVehicle Monitoring Results:")
print(df.to_string(index=False))


# Plot vehicle signals
fig, axes = plt.subplots(2, 2, figsize=(11, 7))

signals = [
    ("VehicleSpeed", "Vehicle Speed", "km/h"),
    ("MotorRPM", "Motor RPM", "rpm"),
    ("BatteryVoltage", "Battery Voltage", "V"),
    ("BatteryTemperature", "Battery Temperature", "°C")
]

for ax, (column, title, unit) in zip(
    axes.flat, signals
):
    ax.plot(
        range(1, len(df) + 1),
        df[column],
        marker="o"
    )

    ax.set_title(title)
    ax.set_xlabel("Sample")
    ax.set_ylabel(unit)
    ax.grid(True)

fig.tight_layout()

plt.savefig(
    "screenshots/vehicle_signals.png",
    dpi=150
)

plt.show()

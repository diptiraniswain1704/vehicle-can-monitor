
# Vehicle CAN Monitoring and Diagnostics System

## Overview
A Python-based vehicle monitoring project that simulates CAN communication, decodes vehicle signals using a DBC file, detects abnormal vehicle conditions, and exposes diagnostic information through REST APIs.

## Features
- Virtual CAN communication using python-can.
- CAN message encoding and decoding using cantools.
- Vehicle signal monitoring: speed, motor RPM, battery voltage and temperature.
- Anomaly detection for high battery temperature and sudden voltage drops.
- CSV-based vehicle data logging.
- Signal visualisation using Matplotlib.
- REST API development using FastAPI.

## Technologies Used
- Python
- python-can
- cantools
- Pandas
- Matplotlib
- FastAPI
- Uvicorn
- DBC (CAN Database)

## Project Structure
```text
vehicle-can-monitor/
├── app.py
├── vehicle_monitor.py
├── vehicle.dbc
├── requirements.txt
├── README.md
├── data/
│   └── vehicle_log.csv
└── screenshots/
    ├── vehicle_signals.png
    ├── api-home.png
    ├── vehicle-data.png
    └── api-health.png
```

## Vehicle Signals
| Signal | Unit |
|---|---|
| Vehicle Speed | km/h |
| Motor RPM | rpm |
| Battery Voltage | V |
| Battery Temperature | °C |

## Anomaly Detection
The system identifies:
- High battery temperature (above 90°C).
- Sudden battery voltage drops.

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | API status |
| GET | /vehicle-data | Retrieve vehicle readings |
| GET | /anomalies | Retrieve abnormal readings |
| GET | /health | System status and anomaly count |

Interactive API documentation is available at `/docs` when the server is running.

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd vehicle-can-monitor
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the vehicle simulation:

```bash
python vehicle_monitor.py
```

Run the API:

```bash
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

## Results
The simulation generates vehicle signal plots, logs decoded CAN data into CSV, and identifies abnormal temperature and voltage conditions.

## Note
This project uses simulated CAN data and a virtual CAN interface. It is intended for learning and demonstrating automotive software and vehicle diagnostics concepts.

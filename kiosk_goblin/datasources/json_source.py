import os
import json
import streamlit as st

class JSONDataSource:
    """
    JSON File Data Source.
    Loads configurations and state logs from offline examples/*.json files.
    Serves as an intermediate data source before actual DB/API integration.
    """
    def __init__(self, base_dir: str = "examples"):
        self.base_dir = base_dir

    def _read_json(self, filename: str, fallback_data: dict) -> dict:
        """Helper to read JSON file securely with fallback."""
        file_path = os.path.join(self.base_dir, filename)
        if not os.path.exists(file_path):
            return fallback_data
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON file {file_path}: {e}")
            return fallback_data

    def get_ml_training_status(self) -> dict:
        """Reads ML training status metrics from file."""
        fallback = {
            "epoch": 24,
            "max_epochs": 100,
            "loss": 0.245,
            "val_loss": 0.268,
            "accuracy": 0.912,
            "val_accuracy": 0.895,
            "history": {
                "epochs": list(range(1, 25)),
                "loss": [0.85 - (i * 0.025) for i in range(24)],
                "val_loss": [0.90 - (i * 0.026) for i in range(24)],
                "accuracy": [0.65 + (i * 0.011) for i in range(24)],
                "val_accuracy": [0.60 + (i * 0.012) for i in range(24)]
            },
            "learning_rate": 0.0001,
            "time_elapsed": "5h 12m",
            "time_remaining": "15h 48m"
        }
        return self._read_json("ml_training.json", fallback)

    def get_dataset_status(self) -> dict:
        """Reads dataset status distributions from file."""
        fallback = {
            "total_images": 142050,
            "classes": ["Robot-Arm", "Conveyor-Belt", "Safety-Helmet", "Pallet", "Forklift"],
            "split": {"train": 99435, "val": 28410, "test": 14205},
            "class_distribution": {
                "Robot-Arm": 35400,
                "Conveyor-Belt": 28100,
                "Safety-Helmet": 42050,
                "Pallet": 21500,
                "Forklift": 15000
            },
            "labeled_ratio": 98.4,
            "recent_adds_today": 450
        }
        return self._read_json("dataset.json", fallback)

    def get_system_metrics(self) -> dict:
        """Mocked or file-based metrics."""
        # Hardware metrics usually change too fast for offline static JSON files,
        # but we support structured configurations if defined.
        fallback = {
            "cpu_usage": 34.5,
            "gpu_usage": 52.0,
            "gpu_temp": 68.5,
            "ram_usage": 45.8,
            "disk_usage": 74.2,
            "disk_total_gb": 512,
            "disk_used_gb": 380,
            "gpu_memory_used_gb": 8.2,
            "gpu_memory_total_gb": 16.0
        }
        return self._read_json("system_metrics.json", fallback)

    def get_event_logs(self) -> list:
        """Reads recent logs array from file."""
        fallback = [
            {"timestamp": "12:04:12", "level": "INFO", "message": "Initialized from JSON datasource."},
            {"timestamp": "12:05:01", "level": "WARN", "message": "Could not establish DB sync. Operating in fallback JSON mode."}
        ]
        data = self._read_json("events.json", {"logs": fallback})
        return data.get("logs", fallback)

    def get_weather_status(self) -> dict:
        """Reads weather metrics from JSON configuration fallback."""
        fallback = {
            "location": "SEOUL, KR",
            "condition": "OVERCAST_MATRIX",
            "temp": 19.8,
            "humidity": 62,
            "wind_speed": "3.1 m/s",
            "air_quality": "MODERATE (AQI: 54)"
        }
        return self._read_json("weather.json", fallback)

    def get_today_tasks(self) -> list:
        """Reads daily tasks list from JSON fallback."""
        fallback = [
            {"time": "09:00", "task": "Database Integrity Check", "status": "SUCCESS"},
            {"time": "12:00", "task": "Standard Dataset Validation Check", "status": "SUCCESS"},
            {"time": "18:00", "task": "Automatic Backups Sync Run", "status": "PENDING"}
        ]
        data = self._read_json("tasks.json", {"tasks": fallback})
        return data.get("tasks", fallback)

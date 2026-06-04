import time
import random
import streamlit as st

class MockDataSource:
    """
    Mock Data Source for the Kiosk Goblin MVP.
    Uses Streamlit's session state to simulate data changing over time 
    (e.g., training epochs advancing, system metrics fluctuating).
    """
    def __init__(self):
        self._initialize_state()

    def _initialize_state(self):
        """Sets up initial state variables if they do not exist."""
        # ML Training Simulation state
        if "ml_epoch" not in st.session_state:
            st.session_state.ml_epoch = 1
            st.session_state.ml_max_epochs = 100
            st.session_state.ml_history = {
                "epochs": [1],
                "loss": [0.85],
                "val_loss": [0.90],
                "accuracy": [0.65],
                "val_accuracy": [0.60]
            }
            st.session_state.last_sim_time = time.time()
            st.session_state.ml_batch = 0
            
        # System metrics initial state
        if "sys_cpu" not in st.session_state:
            st.session_state.sys_cpu = 42.0
            st.session_state.sys_gpu = 65.0
            st.session_state.sys_gpu_temp = 72.0
            st.session_state.sys_ram = 58.5

        # Event log initial state
        if "mock_logs" not in st.session_state:
            st.session_state.mock_logs = [
                {"timestamp": self._get_time_offset(180), "level": "INFO", "message": "Kiosk Goblin system started."},
                {"timestamp": self._get_time_offset(150), "level": "INFO", "message": "Mock datasource initialized successfully."},
                {"timestamp": self._get_time_offset(120), "level": "INFO", "message": "ML training pipeline initialized with batch size 64."},
                {"timestamp": self._get_time_offset(90), "level": "WARN", "message": "GPU temperature reached 72°C - fan speed adjusted to 80%."},
                {"timestamp": self._get_time_offset(60), "level": "INFO", "message": "Epoch 1 finished. val_loss: 0.90, val_accuracy: 0.60."},
                {"timestamp": self._get_time_offset(30), "level": "INFO", "message": "Epoch 2 started... batch training in progress."}
            ]

    def _get_time_offset(self, seconds_ago):
        """Helper to get a timestamp string relative to now."""
        return time.strftime("%H:%M:%S", time.localtime(time.time() - seconds_ago))

    def update_simulations(self):
        """
        Call this once per rerun to advance simulated states.
        Simulates ML training progress and fluctuates system metrics.
        """
        now = time.time()
        elapsed = now - st.session_state.last_sim_time
        
        # Fluctuate system metrics regardless of elapsed time to keep it lively
        st.session_state.sys_cpu = max(5.0, min(100.0, st.session_state.sys_cpu + random.uniform(-8.0, 8.0)))
        st.session_state.sys_gpu = max(10.0, min(100.0, st.session_state.sys_gpu + random.uniform(-5.0, 5.0)))
        st.session_state.sys_gpu_temp = max(50.0, min(95.0, st.session_state.sys_gpu_temp + random.uniform(-1.5, 1.5)))
        st.session_state.sys_ram = max(30.0, min(100.0, st.session_state.sys_ram + random.uniform(-1.0, 1.0)))

        # Update ML progress roughly every 5-10 seconds of simulated time
        # In a real kiosk refresh (e.g. 60s), this will definitely advance.
        # But to make it feel responsive if they manually refresh or reload, we use a simple chance or elapsed check.
        if elapsed >= 5.0 or random.random() < 0.3:
            st.session_state.last_sim_time = now
            
            # Increment batch or epoch
            if st.session_state.ml_epoch < st.session_state.ml_max_epochs:
                # Advance epoch
                st.session_state.ml_epoch += 1
                ep = st.session_state.ml_epoch
                
                # Formula to simulate realistic decaying loss and rising accuracy
                new_loss = max(0.02, 0.9 * (0.95 ** ep) + random.uniform(-0.01, 0.01))
                new_val_loss = max(0.04, new_loss * 1.08 + random.uniform(-0.02, 0.02))
                new_acc = min(0.99, 0.60 + 0.38 * (1 - 0.93 ** ep) + random.uniform(-0.01, 0.01))
                new_val_acc = min(0.98, new_acc * 0.96 + random.uniform(-0.02, 0.02))
                
                st.session_state.ml_history["epochs"].append(ep)
                st.session_state.ml_history["loss"].append(new_loss)
                st.session_state.ml_history["val_loss"].append(new_val_loss)
                st.session_state.ml_history["accuracy"].append(new_acc)
                st.session_state.ml_history["val_accuracy"].append(new_val_acc)
                
                # Add a log event
                timestamp = time.strftime("%H:%M:%S", time.localtime())
                
                # Randomize event details
                event_roll = random.random()
                if event_roll < 0.15:
                    level = "WARN"
                    message = f"GPU memory usage high. Cached tensors cleared."
                elif event_roll < 0.20:
                    level = "ERROR"
                    message = f"Failed to upload checkpoint artifact to remote store. Retrying..."
                else:
                    level = "INFO"
                    message = f"Epoch {ep} finished. loss: {new_loss:.4f}, val_loss: {new_val_loss:.4f}."
                
                st.session_state.mock_logs.append({
                    "timestamp": timestamp,
                    "level": level,
                    "message": message
                })
                
                # Keep log list size under control
                if len(st.session_state.mock_logs) > 25:
                    st.session_state.mock_logs.pop(0)

    # API methods for the plugins to retrieve simulated data
    def get_ml_training_status(self):
        """Returns the current ML training metrics and history."""
        self.update_simulations()
        return {
            "epoch": st.session_state.ml_epoch,
            "max_epochs": st.session_state.ml_max_epochs,
            "loss": st.session_state.ml_history["loss"][-1],
            "val_loss": st.session_state.ml_history["val_loss"][-1],
            "accuracy": st.session_state.ml_history["accuracy"][-1],
            "val_accuracy": st.session_state.ml_history["val_accuracy"][-1],
            "history": st.session_state.ml_history,
            "learning_rate": max(1e-5, 1e-3 * (0.95 ** st.session_state.ml_epoch)),
            "time_elapsed": f"{int((st.session_state.ml_epoch * 12.5) // 60)}m {int((st.session_state.ml_epoch * 12.5) % 60)}s",
            "time_remaining": f"{int(((st.session_state.ml_max_epochs - st.session_state.ml_epoch) * 12.5) // 60)}m {int(((st.session_state.ml_max_epochs - st.session_state.ml_epoch) * 12.5) % 60)}s"
        }

    def get_system_metrics(self):
        """Returns system hardware resource usage levels."""
        self.update_simulations()
        return {
            "cpu_usage": round(st.session_state.sys_cpu, 1),
            "gpu_usage": round(st.session_state.sys_gpu, 1),
            "gpu_temp": round(st.session_state.sys_gpu_temp, 1),
            "ram_usage": round(st.session_state.sys_ram, 1),
            "disk_usage": 74.2,  # Static for simulation simplicity
            "disk_total_gb": 512,
            "disk_used_gb": 380,
            "gpu_memory_used_gb": round(12.0 * (st.session_state.sys_gpu / 100.0), 1),
            "gpu_memory_total_gb": 16.0
        }

    def get_dataset_status(self):
        """Returns dataset splits and label status statistics."""
        return {
            "total_images": 142050,
            "classes": ["Robot-Arm", "Conveyor-Belt", "Safety-Helmet", "Pallet", "Forklift"],
            "split": {
                "train": 99435,   # 70%
                "val": 28410,     # 20%
                "test": 14205      # 10%
            },
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

    def get_event_logs(self):
        """Returns the simulated terminal log array."""
        self.update_simulations()
        # Return logs copy, reversed so newest are at the bottom or top depending on renderer
        return list(st.session_state.mock_logs)

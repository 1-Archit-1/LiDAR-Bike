import json 
import pandas as pd

def read_imu(imu_json:str)->pd.DataFrame:
    try:
        with open(imu_json, "r") as f:
            imu_list = json.load(f)
        flattened_data = [
            {
                "timestamp": entry["timestamp"],
                **{f"angular_velocity_{k}": v for k, v in entry["angular_velocity"].items()},
                **{f"linear_acceleration_{k}": v for k, v in entry["linear_acceleration"].items()}
            }
            for entry in imu_list
        ]
    
        df = pd.DataFrame(flattened_data)
        return df
    except Exception as e:
        raise ValueError(f"Error in reading imu: {e}")
    
def read_gps(gps_file:str)->pd.DataFrame:
    try:
        with open(gps_file, "r") as f:
            gps_list = json.load(f)
        return pd.DataFrame(gps_list)
    except Exception as e:
        raise ValueError(f"Error in reading gps: {e}")
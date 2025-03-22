import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
pd.set_option('display.precision', 13)
from config import get_logger
import time
logger = get_logger(__name__)

def find_reference(sensor_timestamps:dict) -> tuple:
    """ Find reference sensor based on slowest framerate """
    #checking based on the first 200 timestamps
    lidar_avg_gap = np.mean(np.diff(sensor_timestamps["lidar"][:min(200, len(sensor_timestamps["lidar"]))]))
    image_avg_gap = np.mean(np.diff(sensor_timestamps["image"][:min(200, len(sensor_timestamps["image"]))]))

    reference_sensor = "lidar" if lidar_avg_gap > image_avg_gap else "image"
    avg_gap_ref = lidar_avg_gap if lidar_avg_gap > image_avg_gap else image_avg_gap
    reference_timestamps = sensor_timestamps[reference_sensor]
    return reference_sensor, reference_timestamps, avg_gap_ref

def find_closest(sensor_timestamps:dict, ref_timestamps:np.array) -> np.array:
    """ Find closest timestamps as compared to reference"""
    idx = np.searchsorted(sensor_timestamps, ref_timestamps)
    idx = np.clip(idx, 1, len(sensor_timestamps) - 1)
    
    #compare left ad right to find the closest
    left = sensor_timestamps[idx - 1]
    right = sensor_timestamps[idx]
    closest = np.where(abs(left - ref_timestamps) <= abs(right - ref_timestamps), left, right)
    return closest

def align_sensor_data(
        avg_gap_ref:float,
        sensor_df:pd.DataFrame, 
        ref_timestamps:np.array, 
        sensor_type:str
    )->pd.DataFrame:
    
    avg_gap_sensor = np.mean(np.diff(sensor_df["timestamp"].values[:min(200, len(sensor_df))]))

    if avg_gap_sensor > avg_gap_ref:  # Interpolate if too sparse, mostly for GPS
        logger.info(f"Interpolating {sensor_type} data")
        interp_func = interp1d(
            sensor_df["timestamp"], 
            sensor_df.drop(columns=["timestamp"]).values, 
            axis=0, 
            bounds_error=False, 
            fill_value="extrapolate"
        )
        interpolated_values = interp_func(ref_timestamps)
        return pd.DataFrame(interpolated_values, columns=sensor_df.columns[1:], index=ref_timestamps).reset_index().rename(columns={"index": "timestamp"})
    
    else:
        logger.info(f"Using original {sensor_type} data")
        closest_timestamps = find_closest(sensor_df["timestamp"].values, ref_timestamps)

        aligned_sensor_df = sensor_df.set_index("timestamp").loc[closest_timestamps].reset_index()
        aligned_sensor_df["timestamp"] = ref_timestamps

        #ensure aligned
        #aligned_sensor_df = aligned_sensor_df.set_index("timestamp").reindex(ref_timestamps).reset_index()    
        return aligned_sensor_df
        

def synchronize_data(
        lidar_data:dict,
        image_data:dict, 
        imu_df:pd.DataFrame, 
        gps_df:pd.DataFrame
    ) -> list:

    """ Synchronizes all sensor data based on the slowest frame rate. """
    t = time.time()
    sensor_timestamps = {
        "lidar": np.array(list(lidar_data.keys())),
        "image": np.array(list(image_data.keys())),
        "imu": imu_df["timestamp"].values,
        "gps": gps_df["timestamp"].values
    }
    reference_sensor, reference_timestamps, avg_gap_ref = find_reference(sensor_timestamps)

    lidar_df = pd.DataFrame(list(lidar_data.items()), columns=["timestamp", "lidar"])
    image_df = pd.DataFrame(list(image_data.items()), columns=["timestamp", "image"])
    
    if reference_sensor == "lidar":
        image_df = align_sensor_data(
            avg_gap_ref,
            image_df,
            reference_timestamps,
            "image"
        )
    else:    
        lidar_df = align_sensor_data(
            avg_gap_ref,
            lidar_df,
            reference_timestamps,
            "lidar",
        )
    imu_df = align_sensor_data(
        avg_gap_ref,
        imu_df,
        reference_timestamps,
        "imu",
    )
    gps_df = align_sensor_data(
        avg_gap_ref,
        gps_df,
        reference_timestamps,
        "gps"
    )

    reference_df = image_df if reference_sensor == "image" else lidar_df
    sensor_to_merge = image_df if reference_sensor == "lidar" else lidar_df
    #merge all the data based on the timestamp
    synchronized_df = (
        reference_df
        .merge(sensor_to_merge, on="timestamp", how="left")
        .merge(imu_df, on="timestamp", how="left")
        .merge(gps_df, on="timestamp", how="left")
    )
    synchronized_data = synchronized_df.to_dict(orient="records")
    logger.info("Synchronization completed in %s", time.time() - t)
    return synchronized_data


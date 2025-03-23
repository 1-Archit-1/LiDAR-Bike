import os
import numpy as np
from extraction.helper import extract_timestamp
from config import settings
import time
from config import get_logger
from concurrent.futures import ThreadPoolExecutor
logger = get_logger(__name__)

def read_lidar_file(file_path:str, out_file_path:str)->np.ndarray:
    points = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4) 
    np.save(out_file_path, points)
    return points

def process_file(filename, folder_path, lidar_parsed_path):
    """
    Processes a single LiDAR file and returns a tuple of (timestamp, out_file_path).
    """
    if filename.endswith('.bin') and filename.startswith('lidar_'):
        file_path = os.path.join(folder_path, filename)
        timestamp = extract_timestamp(filename, 'lidar') 
        out_file_path = os.path.join(lidar_parsed_path, filename.replace('.bin', '.npy'))
        read_lidar_file(file_path, out_file_path)
        return timestamp, out_file_path
    return None

def read_lidar_from_folder(folder_path: str, lidar_parsed_path: str) -> dict:
    """
    Reads all LiDAR files in parallel, saves them as .npy files,
    returns a dict mapping timestamps to file path.
    """
    t = time.time()
    logger.info(f"Reading LiDAR data from folder: {folder_path}")
    
    point_cloud_dict = {}
    os.makedirs(lidar_parsed_path, exist_ok=True)

    try:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_file, filename, folder_path, lidar_parsed_path) for filename in os.listdir(folder_path)
            ]
            
            for future in futures:
                result = future.result()
                if result:
                    timestamp, out_file_path = result
                    point_cloud_dict[timestamp] = out_file_path
        
        logger.info(f"processed lidar data in: {time.time() - t:.2f}")
        return point_cloud_dict
    except Exception as e:
        logger.error(f"Error processing Lidar at {folder_path}: {e}")
        raise

def read_lidar_from_folder_sequential(folder_path:str, lidar_parsed_path:str )->dict:
    t = time.time()
    try:
        logger.info(f"Reading Lidar data at timestamp: {t}")
        point_cloud_dict = {}
        out_dir = lidar_parsed_path
        #lidar_timestamps = []
        os.makedirs(out_dir, exist_ok=True)

        for filename in os.listdir(folder_path):
            if filename.endswith('.bin') and filename.startswith('lidar_'):  
                file_path = os.path.join(folder_path, filename)
                timestamp = extract_timestamp(filename, 'lidar')
                #lidar_timestamps.append(timestamp)
                out_file_path = os.path.join(out_dir, filename.replace('.bin','.npy'))
                points = read_lidar_file(file_path, out_file_path)
                point_cloud_dict[timestamp] = out_file_path
        logger.info(f"Finished reading Lidar data at timestamp: {time.time() - t}")
        return point_cloud_dict
    except Exception as e:
        raise ValueError(f"Error in reading lidar: {e}")
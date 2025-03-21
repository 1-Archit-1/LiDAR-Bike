import os
import numpy as np
from extraction.helper import extract_timestamp
from config import settings

def read_lidar_file(file_path:str, out_file_path:str)->np.ndarray:
    with open(file_path, 'rb') as f:
        data = f.read()
    points = np.frombuffer(data, dtype=np.float32).reshape(-1, 4)  
    np.save(out_file_path, points)
    return points

def read_lidar_folder_to_dict(folder_path:str, lidar_parsed_path:str )->dict:
    try:
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

        return point_cloud_dict
    except Exception as e:
        raise ValueError(f"Error in reading lidar: {e}")
import os
import numpy as np
from extraction.helper import extract_timestamp
from concurrent.futures import ThreadPoolExecutor
import time
from config import get_logger
logger = get_logger(__name__)

def read_image(file_path:str ,out_file_path:str)->np.ndarray:
    with open(file_path, 'rb') as f:
        # Read the width and height (each 4 bytes, uint32)
        width = int.from_bytes(f.read(4), byteorder='little')
        height = int.from_bytes(f.read(4), byteorder='little')
        image_data = np.frombuffer(f.read(), dtype=np.uint8)
        image = image_data.reshape((height, width, 3))
    np.save(out_file_path, image)
    return image

def process_image(filename, folder_path, image_parsed_path):
    """
    Processes a single image file
    """
    if filename.endswith('.bin') and filename.startswith('image_'):
        file_path = os.path.join(folder_path, filename)
        timestamp = extract_timestamp(filename, 'image')  
        out_file_path = os.path.join(image_parsed_path, filename.replace('.bin', '.npy'))
        read_image(file_path, out_file_path)
        return timestamp, out_file_path
    return None

def read_images_from_folder(folder_path:str, image_parsed_path:str)->dict:
    """
    Reads all image files in a folder in parallel, saves them as .npy files,
    and returns a dict mapping timestamps to file paths.
    """
    image_dict = {}
    t= time.time()
    os.makedirs(image_parsed_path, exist_ok=True)
    try:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_image, filename, folder_path, image_parsed_path)
                for filename in os.listdir(folder_path)
            ]
            
            for future in futures:
                result = future.result()
                if result:
                    timestamp, out_file_path = result
                    image_dict[timestamp] = out_file_path
        logger.info(f"read images in: {time.time() - t:.2f}")
        return image_dict
    except Exception as e:
        raise ValueError(f"Error in reading images: {e}")
    
def read_images_from_folder_sequential(folder_path:str, image_parsed_path:str)->dict:
    try:
        image_dict = {}
        out_dir = image_parsed_path
        #image_timestamps = []
        os.makedirs(out_dir, exist_ok=True)

        for filename in os.listdir(folder_path):
            if filename.endswith('.bin') and filename.startswith('image_'):
                file_path = os.path.join(folder_path, filename)
                timestamp = extract_timestamp(filename, 'image')
                #image_timestamps.append(timestamp)
                out_file_path = os.path.join(out_dir, filename.replace('.bin','.npy'))
                image = read_image(file_path,out_file_path)
                image_dict[timestamp] = out_file_path
        return image_dict
    except Exception as e:
        raise ValueError(f"Error in reading images: {e}")
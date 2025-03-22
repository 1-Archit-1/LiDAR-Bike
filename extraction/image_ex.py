import os
import numpy as np
from extraction.helper import extract_timestamp

def read_image(file_path:str ,out_file_path:str)->np.ndarray:
    with open(file_path, 'rb') as f:
        # Read the width and height (each 4 bytes, uint32)
        width = int.from_bytes(f.read(4), byteorder='little')
        height = int.from_bytes(f.read(4), byteorder='little')
        image_data = np.frombuffer(f.read(), dtype=np.uint8)
        image = image_data.reshape((height, width, 3))
    np.save(out_file_path, image)
    return image

def read_images_from_folder(folder_path:str, image_parsed_path:str)->dict:
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
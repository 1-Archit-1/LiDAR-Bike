from pydantic_settings import BaseSettings
import logging
import os

class Settings(BaseSettings):

    #API 1 subdirectories
    IMAGE_DIR: str = '/images'
    LIDAR_DIR: str = '/lidar'
    IMU_PATH: str = '/imu.txt'
    GPS_PATH: str = '/gps.txt'

    #API2 bonus data directories
    BONUS_IMAGE_DIR: str = 'data_bonus/image_02/data/'
    BONUS_LIDAR_DIR: str = 'data_bonus/lidar/data/'
    CALIB_VELO_TO_CAM: str = 'data_bonus/calib/calib_velo_to_cam.txt'
    CALIB_CAM_TO_CAM: str = 'data_bonus/calib/calib_cam_to_cam.txt'

    #Output directories/paths
    BONUS_OUT_DIR: str = 'lidar_overlay'
    IMAGES_OUT_DIR: str = '/imagesout'
    LIDAR_OUT_DIR: str = '/lidarout'
    SYNC_DATA_OUT_PATH: str = 'synchronized_data.json'

    class Config:
        case_sensitive = True

settings = Settings(_env_file=".env")

def get_logger(name=''):
    logger = logging.getLogger(name)
    os.makedirs('logs', exist_ok=True)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
            "[%(asctime)s] — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"
    )
    file_handler = logging.FileHandler('logs/debug.log', encoding='utf-8')
    file_handler.setFormatter(formatter) 
    logger.addHandler(file_handler)
    return logger
    


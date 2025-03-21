from pydantic_settings import BaseSettings
class Settings(BaseSettings):

    #API 1 subdirectories
    IMAGE_DIR: str = '/images'
    LIDAR_DIR: str = '/lidar'
    IMU_PATH: str = '/imu.txt'
    GPS_PATH: str = '/gps.txt'

    #API2 bonus data directories
    BONUS_IMAGE_DIR: str = 'data_bonus/image_02'
    BONUS_LIDAR_DIR: str = 'data_bonus/lidar'
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


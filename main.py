from fastapi import FastAPI
from fastapi.routing import APIRouter
from extraction.lidar_ex import read_lidar_folder_to_dict
from extraction.image_ex import read_images_from_folder
from extraction.imu_gps import read_imu, read_gps
from extraction.sync import synchronize_data
from config import settings
from projection.calibrate import visualize_lidar_on_image
import json


app = FastAPI(
    title='Sensor Data', description="Server for GRA assessment, LIDAR Bike", docs_url='/docs'
)

router = APIRouter()

@router.get("/project-lidar")
async def calibrate_and_project_lidar(frame_number:str):
    """ Accepts a frame number and projects the Lidar points onto the image """
    try:
        output_path = visualize_lidar_on_image(frame_number)
        return {"message": "LiDAR points projected onto the image", 'success': True, 'data': {'output_image': output_path}}
    except FileNotFoundError as e:
        msg = "\nFrame number should be a numeric string , e.g: 0,1,2\n and file should be named as a 0 padded 10 digit numeric string"
        return {"message": str(e)+ msg, 'success': False}
    except Exception as e:
        return {"message": str(e), 'success': False}
    
@router.get("/synchronize-sensor")
async def extract_synchronize(folder_path: str = None):
    """ Accepts a folder path, parses and synchronizes the sensor data """
    lidar_path = folder_path + settings.LIDAR_DIR
    lidar_parsed_path = folder_path + settings.LIDAR_OUT_DIR
    image_path = folder_path + settings.IMAGE_DIR
    image_parsed_path = folder_path + settings.IMAGES_OUT_DIR
    imu_path = folder_path + settings.IMU_PATH
    gps_path = folder_path + settings.GPS_PATH

    try:
        print('Creating Lidar parsed output')
        lidar_dict = read_lidar_folder_to_dict(lidar_path, lidar_parsed_path)
        
        print('Creating Image parsed output')
        image_dict = read_images_from_folder(image_path, image_parsed_path)


        #lidar_dict = {1701985839.321918: 'data_q123/lidarout/lidar_1701985839_321918010.npy', 1701985839.3622098: 'data_q123/lidarout/lidar_1701985839_362209796.npy', 1701985839.4104006: 'data_q123/lidarout/lidar_1701985839_410400629.npy', 1701985839.46123: 'data_q123/lidarout/lidar_1701985839_461230039.npy', 1701985839.5114465: 'data_q123/lidarout/lidar_1701985839_511446475.npy', 1701985839.571546: 'data_q123/lidarout/lidar_1701985839_571546077.npy', 1701985839.6105914: 'data_q123/lidarout/lidar_1701985839_610591411.npy', 1701985839.6685147: 'data_q123/lidarout/lidar_1701985839_668514728.npy', 1701985839.71749: 'data_q123/lidarout/lidar_1701985839_717489957.npy', 1701985839.768327: 'data_q123/lidarout/lidar_1701985839_768326997.npy', 1701985839.8149107: 'data_q123/lidarout/lidar_1701985839_814910650.npy', 1701985839.8614798: 'data_q123/lidarout/lidar_1701985839_861479759.npy', 1701985839.9191844: 'data_q123/lidarout/lidar_1701985839_919184446.npy', 1701985839.9638753: 'data_q123/lidarout/lidar_1701985839_963875293.npy', 1701985840.0157256: 'data_q123/lidarout/lidar_1701985840_015725612.npy', 1701985840.0639946: 'data_q123/lidarout/lidar_1701985840_063994646.npy', 1701985840.1129212: 'data_q123/lidarout/lidar_1701985840_112921237.npy', 1701985840.1668463: 'data_q123/lidarout/lidar_1701985840_166846275.npy', 1701985840.2096665: 'data_q123/lidarout/lidar_1701985840_209666490.npy', 1701985840.2733428: 'data_q123/lidarout/lidar_1701985840_273342847.npy'}
        #image_dict = {1701985839.6339679: 'data_q123/imagesout/image_1701985839_633967876.npy', 1701985839.7861893: 'data_q123/imagesout/image_1701985839_786189317.npy', 1701985839.9321508: 'data_q123/imagesout/image_1701985839_932150840.npy', 1701985840.0315874: 'data_q123/imagesout/image_1701985840_031587362.npy', 1701985840.1424825: 'data_q123/imagesout/image_1701985840_142482519.npy', 1701985840.246012: 'data_q123/imagesout/image_1701985840_246011972.npy', 1701985840.3654428: 'data_q123/imagesout/image_1701985840_365442752.npy', 1701985840.4922056: 'data_q123/imagesout/image_1701985840_492205619.npy', 1701985840.5944946: 'data_q123/imagesout/image_1701985840_594494581.npy', 1701985840.7037158: 'data_q123/imagesout/image_1701985840_703715801.npy'}

        imu_data = read_imu(imu_path)
        gps_data = read_gps(gps_path)
            
        print('Synchronizing data')
        data = synchronize_data(lidar_dict,image_dict, imu_data, gps_data)
        # writing synchronized data to a file
        with open(settings.SYNC_DATA_OUT_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        
        return {"message": "Data synchronized", 'success': True, 'data': data}
    
    except Exception as e:
        return {"message": str(e), 'success': False}
    

app.include_router(router)
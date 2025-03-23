import numpy as np
import os
import cv2
from config import get_logger
from config import settings

logger = get_logger(__name__)

def load_calibration(calib_path: str)->dict:
    """Load calibration matrices """
    calib = {}
    with open(calib_path, 'r') as f:
        for line in f:
            key, value = line.split(':', 1)
            calib[key.strip()] = np.array([float(x) for x in value.strip().split()])
    return calib

def project_lidar_to_image(points, R_vc, T_vc, R02, T02, R_rect, P2)->np.ndarray:
    """Project 3D Lidar points to 2D image"""
    
    points_cam0 = (R_vc @ points[:, :3].T).T + T_vc  #(N, 3) transform points to cam0 coordinates

    points_cam2 = (R02 @ points_cam0.T).T + T02  #(N, 3) transform cam0 to cam2 

    points_cam2 = points_cam2[points_cam2[:, 2] > 0] #filter out points behind camera where z<0

    points_rect_xyz = (R_rect @ points_cam2.T).T  #(N,3) rectification
    points_rect = np.hstack((points_rect_xyz, np.ones((points_rect_xyz.shape[0], 1)))) #(N,4)

    points_2d_hom = (P2 @ points_rect.T).T  #(N, 3) Project to 2D 
    points_2d = points_2d_hom[:, :2] / points_2d_hom[:, 2][:, np.newaxis]  #Normalize

    return points_2d


def visualize_lidar_on_image(frame_number:str)->str:
    """Visualize LiDAR points projected onto the corresponding Camera 2 image."""
    
    image_path = os.path.join(settings.BONUS_IMAGE_DIR, f"{frame_number.zfill(10)}.png")
    lidar_path = os.path.join(settings.BONUS_LIDAR_DIR, f"{frame_number.zfill(10)}.bin")
    if not os.path.exists(image_path) or not os.path.exists(lidar_path):
        raise FileNotFoundError(f"Image or LiDAR file not found: {frame_number}")

    image = cv2.imread(image_path)
    points = np.fromfile(lidar_path, dtype=np.float32).reshape(-1, 4)  #(N, 4)
    reflectance = points[:, 3] 

    calib_velo_to_cam = load_calibration(settings.CALIB_VELO_TO_CAM)
    calib_cam_to_cam = load_calibration(settings.CALIB_CAM_TO_CAM)

    #extract matrices for calibration
    R_velo_to_cam = calib_velo_to_cam['R'].reshape(3, 3) 
    T_velo_to_cam = calib_velo_to_cam['T'] 
    R02 = calib_cam_to_cam['R_02'].reshape(3, 3) 
    T02 = calib_cam_to_cam['T_02'] 
    R_rect = calib_cam_to_cam['R_rect_02'].reshape(3, 3)
    P2 = calib_cam_to_cam['P_rect_02'].reshape(3, 4)

    points_2d = project_lidar_to_image(points, R_velo_to_cam, T_velo_to_cam, R02, T02, R_rect, P2)

    #reflectance_normalized = (reflectance - np.min(reflectance)) / (np.max(reflectance) - np.min(reflectance))
    colors = (reflectance * 255).astype(np.uint8)

    #Overlay on image
    for (u, v), color in zip(points_2d, colors):
        if 0 <= u < image.shape[1] and 0 <= v < image.shape[0]:
            #cv2.circle(image, (int(u), int(v)), 1, (255, 255, 255-int(color)), 1)  #Color based on reflectance
            cv2.line(image, (int(u), int(v)), (int(u), int(v)), (255, 255, 255 - int(color)), 1)
    
    os.makedirs(settings.BONUS_OUT_DIR, exist_ok=True)
    output_path =settings.BONUS_OUT_DIR + f"/output_{frame_number}.png"
    cv2.imwrite(output_path, image)

    logger.info(f"Visualization saved to {output_path}")
    return os.path.abspath(output_path)

if __name__ == '__main__':
    frame_number = "4" 
    visualize_lidar_on_image(frame_number)
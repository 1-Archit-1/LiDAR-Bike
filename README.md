# Smart Bike Sensor Data Server

This repository contains a server designed to parse, extract, and calibrate data from various sensors on a smart bike built by the Georgia Tech Smart Cities Lab, including:

- **Cameras**
- **LiDAR**
- **GPS**
- **IMU**

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/1-Archit-1/LiDAR-Bike
   cd LiDAR-Bike
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Server

Start the server using Uvicorn:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

## **API Documentation**

Once the server is running, you can access the API documentation and interact with the endpoints using the following tools:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

This interactive interface allows you to explore and test the available APIs.

---

### **API Endpoints**

#### 1. **Extracting and Transforming Data**
This endpoint is used to synchronize sensor data by extracting and transforming it from the provided directory.

- **Endpoint**:  
  `GET http://localhost:8000/synchronize-sensor`

- **Query Parameters**:
  - `folder_path` (string, required): The path to the directory containing the sensor data (e.g., LiDAR and camera data).

- **Example Request**:
  ```bash
  curl "http://localhost:8000/synchronize-sensor?folder_path=/path/to/data"
#### 2. **Projecting LiDAR Points on Image**
This endpoint projects 3D LiDAR points onto a specific frame of the camera image.

- **Endpoint**:  
  `GET http://localhost:8000/project-lidar`

- **Query Parameters**:
  - `frame_number` (string, required): The frame number of the image onto which the LiDAR points will be projected.

- **Example Request**:
  ```bash
  curl "http://localhost:8000/project-lidar?frame_number=5"

## Configuration

If you want to change the default location for data storage and outputs:

1. Rename `.env.example` to `.env`:
   ```sh
   mv .env.example .env
   ```
2. Edit the `.env` file with your preferred values.

### Adding Sensor Data
Ensure that sensor data is placed in the required folders before running the server. The default locations are specified in `.env.example`. 

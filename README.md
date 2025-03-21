# Smart Bike Sensor Data Server

This repository contains a server designed to parse, extract, and calibrate data from various sensors on a smart bike, including:

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

### API Documentation
Once the server is running, you can access the API documentation at:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

## Configuration

If you want to change the default location for data storage and outputs:

1. Rename `.env.example` to `.env`:
   ```sh
   mv .env.example .env
   ```
2. Edit the `.env` file with your preferred values.

### Adding Sensor Data
Ensure that sensor data is placed in the required folders before running the server. The default locations are specified in `.env.example`. 

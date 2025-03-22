from fastapi import FastAPI
from api import router


app = FastAPI(
    title='Sensor Data', description="Server for GRA assessment, LIDAR Bike", docs_url='/docs'
)

app.include_router(router)
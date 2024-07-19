from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from asyncio import sleep

from app.crud import create_sensor_data, get_sensor_data, update_sensor_data
from app.database import SessionLocal, init_db
from app.models import SensorData

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SensorDataCreate(BaseModel):
    temperature: float
    humidity: float
    is_raining: bool = False
    umbrella_present: bool
    door_open: bool


async def get_db():
    async with SessionLocal() as session:
        yield session


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post("/update")
async def update_sensor_data_endpoint(
    data: SensorDataCreate, db: AsyncSession = Depends(get_db)
):
    if data.humidity >= 80:
        data.is_raining = True
    else:
        data.is_raining = False

    db_data = await get_sensor_data(db, 1)  # Assuming single sensor with ID 1
    if db_data:
        updated_data = await update_sensor_data(db, db_data.id, data.dict())
        return updated_data
    else:
        new_data = SensorData(**data.dict())
        created_data = await create_sensor_data(db, new_data)
        return created_data


@app.get("/status")
async def get_status(db: AsyncSession = Depends(get_db)):
    sensor_data = await get_sensor_data(db, 1)  # Assuming single sensor with ID 1
    if sensor_data:
        return sensor_data
    raise HTTPException(status_code=404, detail="Sensor data not found")


@app.post("/door")
async def control_door(action: str, db: AsyncSession = Depends(get_db)):
    sensor_data = await get_sensor_data(db, 1)  # Assuming single sensor with ID 1
    if not sensor_data:
        raise HTTPException(status_code=404, detail="Sensor data not found")

    if sensor_data.door_open:
        updated_data = await update_sensor_data(
            db, sensor_data.id, {"door_open": False}
        )
        return {"message": "Door closed", "data": updated_data}
    else:
        updated_data = await update_sensor_data(db, sensor_data.id, {"door_open": True})
        return {"message": "Door opened", "data": updated_data}


async def alarm(db: AsyncSession):
    while True:
        sensor_data = await get_sensor_data(db, 1)  # Assuming single sensor with ID 1
        if not sensor_data:
            raise HTTPException(status_code=404, detail="Sensor data not found")

        if sensor_data.umbrella_present and sensor_data.door_open:
            yield "ALARM"
        await sleep(1)


@app.get("/umbrella")
async def check_umbrella(db: AsyncSession = Depends(get_db)):
    return StreamingResponse(alarm(db), media_type="text/event-stream")

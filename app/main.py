from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal, init_db
from app.models import SensorData
from app.crud import create_sensor_data, update_sensor_data, get_sensor_data
from pydantic import BaseModel

#uvicorn main:app --reload
#uvicorn app.main:app --reload


app = FastAPI() #app 인스턴스 생성

# 센서 데이터 모델
class SensorDataCreate(BaseModel):
    temperature: float
    humidity: float
    is_raining: bool
    umbrella_present: bool
    door_open: bool

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/update")
async def update_sensor_data_endpoint(data: SensorDataCreate, db: AsyncSession = Depends(get_db)):
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

    if action == "open":
        updated_data = await update_sensor_data(db, sensor_data.id, {"door_open": True})
        return {"message": "Door opened", "data": updated_data}
    elif action == "close":
        updated_data = await update_sensor_data(db, sensor_data.id, {"door_open": False})
        return {"message": "Door closed", "data": updated_data}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

@app.get("/umbrella")
async def check_umbrella(db: AsyncSession = Depends(get_db)):
    sensor_data = await get_sensor_data(db, 1)  # Assuming single sensor with ID 1
    if not sensor_data:
        raise HTTPException(status_code=404, detail="Sensor data not found")

    if not sensor_data.umbrella_present and sensor_data.door_open:
        return {"alarm": "Umbrella not taken but door is open!"}
    return {"alarm": "All clear"}

@app.get("/alarm")
async def check_alarm(db: AsyncSession = Depends(get_db)):
    sensor_data = await get_sensor_data(db, 1)  # Assuming single sensor with ID 1
    if not sensor_data:
        raise HTTPException(status_code=404, detail="Sensor data not found")

    if not sensor_data.umbrella_present and sensor_data.door_open:
        return {"alarm": "Umbrella not taken but door is open!"}
    return {"alarm": "All clear"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Umbrella Management API"}




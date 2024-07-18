from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import SensorData

async def get_sensor_data(db: AsyncSession, sensor_id: int):
    result = await db.execute(select(SensorData).filter(SensorData.id == sensor_id))
    return result.scalars().first()

async def create_sensor_data(db: AsyncSession, sensor_data: SensorData):
    db.add(sensor_data)
    await db.commit()
    await db.refresh(sensor_data)
    return sensor_data

async def update_sensor_data(db: AsyncSession, sensor_id: int, data: dict):
    result = await db.execute(select(SensorData).filter(SensorData.id == sensor_id))
    sensor_data = result.scalars().first()
    if sensor_data:
        for key, value in data.items():
            setattr(sensor_data, key, value)
        await db.commit()
        await db.refresh(sensor_data)
    return sensor_data

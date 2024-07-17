from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class SensorData(BaseModel):
    temperature: float
    humidity: float
    umbrella_present: bool
    door_open: bool

sensor_data = {
    "temperature": None,
    "humidity": None,
    "umbrella_present": False,
    "door_open": False
}

@app.post("/update")
async def update_sensor_data(data: SensorData):
    sensor_data.update(data.dict())
    return {"message": "Sensor data updated successfully"}

@app.get("/status")
async def get_status():
    return sensor_data

@app.post("/control_door")
async def control_door(action: str):
    if action == "open":
        # 실제 문 열기 코드를 여기 추가
        sensor_data["door_open"] = True
        return {"message": "Door opened"}
    elif action == "close":
        # 실제 문 닫기 코드를 여기 추가
        sensor_data["door_open"] = False
        return {"message": "Door closed"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

@app.get("/check_umbrella")
async def check_umbrella():
    if not sensor_data["umbrella_present"] and sensor_data["door_open"]:
        # 알림 전송 코드를 여기 추가 (예: 이메일, SMS, Push Notification)
        return {"alarm": "Umbrella not taken but door is open!"}
    return {"alarm": "All clear"}

@app.get("/alarm")
async def check_alarm():
    if not sensor_data["umbrella_present"] and sensor_data["door_open"]:
        return {"alarm": "Umbrella not taken but door is open!"}
    return {"alarm": "All clear"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

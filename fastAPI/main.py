from asyncio import sleep

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()  # FastAPI 바탕으로 app 인스턴스 생성
app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 센서 데이터 모델 정의
class SensorData(BaseModel):
    temperature: float
    humidity: float
    is_raining: bool
    umbrella_present: bool
    door_open: bool


# 초기 센서 데이터
sensor_data = {
    "temperature": None,
    "humidity": None,
    "is_raining": False,
    "umbrella_present": False,
    "door_open": False,
}


# 센서 데이터 업데이트 엔드포인트
@app.post("/update")
async def update_sensor_data(data: SensorData):
    sensor_data.update(data.dict())
    return {"message": "Sensor data updated successfully"}


# 현재 상태 확인 엔드포인트
@app.get("/status")
async def get_status():
    return sensor_data


# 문 제어 엔드포인트
@app.post("/door")
async def control_door():
    if sensor_data["door_open"]:
        sensor_data["door_open"] = False
    else:
        sensor_data["door_open"] = True


# 우산 상태 확인 엔드포인트
@app.get("/umbrella")
async def check_umbrella():
    while True:
        if sensor_data["umbrella_present"] and sensor_data["door_open"]:
            # 알림전송코드추가 (이메일, SMS, Push Notification 등등)
            return StreamingResponse(content={"message": "Alarm"})
        await sleep(1)


# 알람 확인 엔드포인트
@app.get("/alarm")
async def check_alarm():
    if not sensor_data["umbrella_present"] and sensor_data["door_open"]:
        return {"alarm": "Umbrella not taken but door is open!"}
    return {"alarm": "All clear"}


# 루트 엔드포인트
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Umbrella Management API"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

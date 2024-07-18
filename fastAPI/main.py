from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import threading
import requests
import time

app = FastAPI()  # FastAPI 바탕으로 app 인스턴스 생성

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
    "door_open": False
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
async def control_door(action: str):
    if action == "open":
        # 문열기코드추가
        sensor_data["door_open"] = True
        return {"message": "Door opened"}
    elif action == "close":
        # 문열기코드추가
        sensor_data["door_open"] = False
        return {"message": "Door closed"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

# 우산 상태 확인 엔드포인트
@app.get("/umbrella")
async def check_umbrella():
    if not sensor_data["umbrella_present"] and sensor_data["door_open"]:
        # 알림전송코드추가 (이메일, SMS, Push Notification 등등)
        return {"alarm": "Umbrella not taken but door is open!"}
    return {"alarm": "All clear"}

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

# 주기적으로 센서 데이터를 서버에 전송하는 함수
def update_sensor_data():
    url = "http://localhost:8000/update"
    while True:
        sensor_data = {
            "temperature": 25.0,
            "humidity": 60.0,
            "is_raining": False,
            "umbrella_present": True,
            "door_open": False
        }
        response = requests.post(url, json=sensor_data)
        print(response.json())
        time.sleep(10)  # 10초마다 데이터를 전송

# 데이터 전송을 thread 시작
thread = threading.Thread(target=update_sensor_data)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    #test


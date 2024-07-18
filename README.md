# 백엔드 개요

<br>

**센서 데이터 수집 및 전송**:

- 센서 데이터를 수집하고 주기적으로 서버에 전송
- 우산 보관 여부, 문이 열렸는지 닫혔는지 여부를 감지
<br>


**FastAPI 서버**:

- 센서 데이터 수신 및 저장
- 특정 조건 만족 시 알림 전송
- 우산 보관함 문 제어 (열기/닫기)
<br>


**알림 시스템**:

- 우산을 가져가지 않고 문이 열렸을 때 알림 전송
<br>


**API 기능**:

- 센서로 우산이 있는지 없는지를 판단 
- 센서로 비가 오는 지 안 오는지를 판단 
- 센서로 문이 열렸는지 안 열렸는지를 판단

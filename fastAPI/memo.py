'''
참조
'''

'''
실행코드
uvicorn main:app --reload
'''
'''
https://wikidocs.net/162082
https://wikidocs.net/175214
''' 


'''받아오는 데이터의 예시'''

#기본 상태
{
    "temperature": 25.0,
    "humidity": 60.0,
    "is_raining": false,
    "umbrella_present": true,
    "door_open": false
}


#비가 오는 상황
{
    "temperature": 20.5,
    "humidity": 80.0,
    "is_raining": true,
    "umbrella_present": false,
    "door_open": true
}

#우산이 있는 상태에서 문이 열림
{
    "temperature": 22.0,
    "humidity": 55.0,
    "is_raining": false,
    "umbrella_present": true,
    "door_open": true
}

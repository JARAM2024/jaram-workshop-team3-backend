from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    is_raining = Column(Boolean, default=False)
    umbrella_present = Column(Boolean, default=False)
    door_open = Column(Boolean, default=False)


#데이터베이스의 모델들을 정의. SQLAlche,y 를 사용하여 데이터베이스 테이블과 매핑되는 ORM 모델을 작성함. 

# +------------------+----------------------+
# |  sensor_data     |                      |
# +------------------+----------------------+
# | id               | Integer (Primary Key)|
# | temperature      | Float (Not Null)     |
# | humidity         | Float (Not Null)     |
# | is_raining       | Boolean (Default=False)|
# | umbrella_present | Boolean (Default=False)|
# | door_open        | Boolean (Default=False)|
# +------------------+----------------------+

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

#DATABASE_URL = "mysql+aiomysql://eoieiie:1234@localhost/UMBRELLA"
#key = 값의 형태 
#드러나서는 안되는 키값을 관리 
#보안에 관련된 정보들은 환경변수에 저장하는데, .env는 그 환경변수 파일 

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

#세션이 자동으로 커밋이나 플러쉬되지 않도록 함. 

async def init_db(): #데이터베잇스 연결을 시작 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


#데이터페이스 연결과 세션을 관리. 

# -- MySQL 콘솔에 로그인
# mysql -u root -p

# -- 데이터베이스 생성
# CREATE DATABASE UMBRELLA;

# -- 새 사용자 생성 및 비밀번호 설정
# CREATE USER '유저이름'@'localhost' IDENTIFIED BY '비밀번호';

# -- 사용자에게 데이터베이스에 대한 권한 부여
# GRANT ALL PRIVILEGES ON UMBRELLA.* TO '유저이름'@'localhost';

# -- 권한 적용
# FLUSH PRIVILEGES;
# DATABASE_URL = "mysql+aiomysql://유저이름:비밀번호@localhost/UMBRELLA"
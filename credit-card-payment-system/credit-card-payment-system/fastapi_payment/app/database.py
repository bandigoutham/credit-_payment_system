from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from .config import DB_NAME,DB_USER,DB_PASSWORD,DB_HOST,DB_PORT
url=URL.create("mysql+pymysql",username=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=int(DB_PORT),database=DB_NAME,query={"charset":"utf8mb4"})
engine=create_engine(url,pool_pre_ping=True,pool_recycle=1800,pool_size=5,max_overflow=10)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False,expire_on_commit=False)
def get_db():
 db=SessionLocal()
 try: yield db
 finally: db.close()

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
engine = create_engine('postgresql+psycopg2://postgres:%40bdulmu33d@localhost:5432/postgres')
meta  = MetaData()

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


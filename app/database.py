from sqlalchemy import create_engine, MetaData

engine = create_engine('postgresql+psycopg2://postgres:%40bdulmu33d@localhost:5432/postgres')
meta  = MetaData()

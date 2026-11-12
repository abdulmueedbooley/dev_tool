from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('postgresql+psycopg2://postgres:%40bdulmu33d@localhost:5432/postgres')

conn = engine.connect()

meta  = MetaData()

people = Table(
    "people",
    meta, 
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('age', Integer, nullable=False)
)

# create table in db
meta.create_all(engine)
conn = engine.connect()

insert_statement = people.insert().values(name="abdulmueed", age=19)
result = conn.execute(insert_statement)
conn.commit()
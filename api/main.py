from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.get("/")
async def home():
    return "hello world"

conn = psycopg2.connect(host = "localhost", dbname = "postgres", user = "postgres", password = "@bdulmu33d", port = 5050)
cur = conn.cursor()
# cur.execute(**SQL QUERY HERE**)
conn.commit()
cur.close()

# testing
from fastapi import FastAPI
import psycopg2

app = FastAPI() # basically acts as the central hub or front door of your application
# it registers all your routers and starts the web server

students = {
    1 : {"name" : "abdul",
         "age" : 19,
         "University" : "CPUT"}
}

@app.get("/")
async def home():
    return "hello world"

@app.get("/get-student/{student_id}") # Path parameters
def get_student(student_id : int):
    return students[student_id]


conn = psycopg2.connect(host = "localhost", dbname = "postgres", user = "postgres", password = "@bdulmu33d", port = 5050)
cur = conn.cursor()
# cur.execute(**SQL QUERY HERE**)
conn.commit()
cur.close()


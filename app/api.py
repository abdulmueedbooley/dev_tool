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

def read_packages(path):
    packages = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            name, assign, version = line.partition('==')
            packages.append({'name:' : name, 'version:' : version})
    return packages

path = 'C:/Users/abdul/Documents/GitHub/upstream/requirements.txt'







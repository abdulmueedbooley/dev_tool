from fastapi import FastAPI, Depends
import psycopg2
from app.database import get_db
from sqlalchemy.orm import Session
from app.clients import pypi
from app.models import projects, health_score

app = FastAPI() # basically acts as the central hub or front door of your application
# it registers all your routers and starts the web server
project_name = "project SteelWing"


@app.post("/scan-dep/{package_name}")
def scan_store_package(package_name : str, db : Session = Depends(get_db)):
    package = pypi(package_name)

    project_insert_statement = projects.insert().values(
        project_name=project_name, project_type="saas", created_at=package["last_release"]
    )

    result = db.execute(project_insert_statement)
    db.commit()

    return {
        "status" : "success",
        "message" : f"Successfully scanned and stored{package_name}",
        "package" : package
    }









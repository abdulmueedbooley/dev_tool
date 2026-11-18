from fastapi import FastAPI, Depends
import psycopg2
from app.database import get_db
from sqlalchemy.orm import Session
from app.clients import pypi
from app.models import projects, health_score
from app.scoring import score_package

app = FastAPI() # basically acts as the central hub or front door of your application
# it registers all your routers and starts the web server
project_name = "project SteelWing"


@app.post("/scan-dep/{pack_name}")
def scan_store_package(pack_name : str, db : Session = Depends(get_db)):
    package = pypi(pack_name)
    health = score_package(package, "saas", vul=0)

    project_insert_statement = projects.insert().values(
        project_name=project_name, project_type="saas", created_at=package["last_release"]
    )

    health_score_statement = health_score.insert().values(
        package_name=pack_name, version=package["latest_version"], grade=health["grade"],
        score=health["score"], license_risk=health["license_risk"], reason=health["reason"])

    db.execute(health_score_statement)
    db.commit()

    result = db.execute(project_insert_statement)
    db.commit()

    return {
        "status" : "success",
        "message" : f"Successfully scanned and stored{pack_name}",
        "package" : package
    }










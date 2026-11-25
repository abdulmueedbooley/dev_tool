from fastapi import FastAPI, Depends
import psycopg2
from app.database import get_db
from sqlalchemy.orm import Session
from app.clients import pypi
from app.models import projects, health_score
from app.scoring import score_package
from app.parsers import read_packages

app = FastAPI() # basically acts as the central hub or front door of your application
# it registers all your routers and starts the web server
project_name = "project SteelWing"


def scan_single_package(pack_name : str, db : Session):

    existing_score = db.execute(health_score.select().where(health_score.c.package_name == pack_name)).first()

    if existing_score:
        return {
            "status" : "cache",
            "message" : f"Data for {pack_name} fetched from database",
            "health" : {
                "project_id" : existing_score.project_id,
                "package_name" : existing_score.package_name,
                "version" : existing_score.version,
                "grade" : existing_score.grade,
                "score" : existing_score.score,
                "license_risk" : existing_score.license_risk,
                "reason" : existing_score.reason
            }
        }

    package = pypi(pack_name)
    health = score_package(package, "saas", vul=0)

    project_insert_statement = projects.insert().values(
        project_name=project_name, project_type="saas", created_at=package["last_release"]
    )

    result = db.execute(project_insert_statement)
    db.commit()

    health_fk = result.inserted_primary_key[0]

    health_score_statement = health_score.insert().values(
        project_id=health_fk, package_name=pack_name, version=package["latest_version"], grade=health["grade"],
        score=health["score"], license_risk=health["license_risk"], reason=health["reason"])

    db.execute(health_score_statement)
    db.commit()


    return {
        "status" : "success",
        "message" : f"Successfully scanned and stored{pack_name}",
        "package" : package
    }


@app.post("/scan-dep{pack_name}")
def scan_store_package(pack_name : str, db : Session = Depends(get_db)):
    return scan_single_package(pack_name, db)


@app.post("/scan-requirements")
def scan_req_file(db : Session = Depends(get_db)):
    dependency_list = read_packages("requirements.txt")
    dependencies = [lib["name"] for lib in dependency_list if lib.get("name")]

    results = []
    for library in dependencies:
        library_result = scan_single_package(library, db)
        results.append(library_result)

    return {
        "Number of libraries" : len(results),
        "Dependency list" : results,
    }




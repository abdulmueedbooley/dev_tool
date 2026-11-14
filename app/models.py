from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from app.database import meta
projects = Table (
    "projects",
    meta,
    Column('id', Integer, primary_key=True),
    Column('project_name', String, nullable=False),
    Column('project_type', String, nullable=False),
    Column('created_at', DateTime, nullable=False)
)

health_score = Table (
    "health_score",
    meta,
    Column('id', Integer, primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('package_name', String, nullable=False),
    Column('version', String, nullable=False),
    Column('grade', String, nullable=False),
    Column('score', Integer, nullable=False),
    Column('license_risk', String, nullable=False),
    Column('reason', String, nullable=False)
)
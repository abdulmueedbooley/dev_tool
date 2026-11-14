from app.database import engine, meta
import app.models

meta.create_all(engine)
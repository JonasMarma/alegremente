from app import db
import os

if os.path.exists("database.db"):
    os.remove("database.db")
db.create_all()
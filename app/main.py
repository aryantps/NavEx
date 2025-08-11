# app/main.py

from fastapi import FastAPI
from app.core.app_factory import create_app

app: FastAPI = create_app()




#  poetry run uvicorn app.main:app --reload --dev
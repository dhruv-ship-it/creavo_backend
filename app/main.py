from fastapi import FastAPI
from app.db.session import engine

app = FastAPI(title="Creavo Backend")

@app.get("/")
def root():
    return {"message": "Creavo backend running"}

@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": "not connected"}

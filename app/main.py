from fastapi import FastAPI

app = FastAPI(title="Creavo Backend")

@app.get("/")
def root():
    return {"message": "Creavo backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}

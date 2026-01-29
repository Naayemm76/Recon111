
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ReconMaster on Fly.io is running!"}


from fastapi import FastAPI
import shutil, subprocess

app = FastAPI()

@app.get("/check-tool")
def check_tool(name: str):
    return {"installed": shutil.which(name) is not None}

@app.post("/install-tool")
def install_tool(name: str):
    subprocess.Popen(["sudo", "apt", "install", "-y", name])
    return {"message": f"{name} installation started."}

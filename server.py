from fastapi import Form
from fastapi.templating import Jinja2Templates
from configparser import ConfigParser
import bcrypt

templates = Jinja2Templates(directory=str(UI / "templates"))

app = FastAPI()

config = ConfigParser()
config.read("/home/Nayem/ReconMaster/Admin/admin.conf")
ADMIN_USER = config.get("DEFAULT", "admin_user")
ADMIN_HASH = config.get("DEFAULT", "admin_pass_hash").encode()

@app.get("/", response_class=HTMLResponse)
def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username != ADMIN_USER or not bcrypt.checkpw(password.encode(), ADMIN_HASH):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

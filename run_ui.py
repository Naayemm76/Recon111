import uvicorn
from server import app
import admin_auth

# Admin-Login erzwingen, bevor der Server startet
admin_auth.admin_login()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8787)
import uvicorn
from server import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8787)

import sys

# 1) Admin-Authentifizierung
import admin_auth
admin_auth.admin_login()

# 2) Legal-Gate
import legal
if not legal.check_legal_acceptance():
    print("Rechtliche Bedingungen nicht akzeptiert. Beende.")
    sys.exit(1)

# 3) Admin-Anfragen UI starten
from Admin.admin_request_ui import start_ui
start_ui(user="KundenName")

# 4) Framework starten (weiteres Workflow-Modul)
import workflow
workflow.start()


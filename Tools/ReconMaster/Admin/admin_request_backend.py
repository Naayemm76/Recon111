import os
import json
from datetime import datetime
import requests

EU_COUNTRIES = ["DE","FR","ES","IT","NL","BE","AT","CH","LU"]

def send_admin_request(user, email, message, category="help", country_code="DE"):
    data = {
        "user": user,
        "email": email,
        "category": category,
        "message": message,
        "country": country_code,
        "time": datetime.utcnow().isoformat()
    }

    log_dir = "logs/admin_requests"
    os.makedirs(log_dir, exist_ok=True)
    log_file = f"{log_dir}/{datetime.utcnow().date()}.json"

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(data)
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

    # Formspree nur außerhalb EU
    if country_code not in EU_COUNTRIES:
        endpoint = "https://formspree.io/f/xnjponzz"
        requests.post(endpoint, data={"message": json.dumps(data)})

from configparser import ConfigParser
import bcrypt
import sys
import requests

# Config laden (RELATIVER PFAD – Linux & Windows kompatibel)
config = ConfigParser()
config.read("/home/Nayem/ReconMaster/Admin/admin.conf")

# Werte aus config
ADMIN_USER = config.get("DEFAULT", "admin_user")
ADMIN_HASH = config.get("DEFAULT", "admin_pass_hash").encode()
FORMSPREE = config.get("DEFAULT", "formspree_endpoint")

def admin_login():
    username = input("Admin Username: ")
    password = input("Admin Passwort: ")

    if username != ADMIN_USER:
        print("Zugriff verweigert")
        sys.exit(1)

    if not bcrypt.checkpw(password.encode(), ADMIN_HASH):
        print("Zugriff verweigert")
        sys.exit(1)

    # Admin erfolgreich → Benachrichtigung
    try:
        requests.post(FORMSPREE, data={
            "message": "Admin Login erfolgreich"
        })
    except:
        pass

    print("[✓] Admin authentifiziert")


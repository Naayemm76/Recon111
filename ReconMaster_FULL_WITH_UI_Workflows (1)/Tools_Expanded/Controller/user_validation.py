import bcrypt
from configparser import ConfigParser
import requests
import sys

config = ConfigParser()
config.read("../Admin/admin.conf")

username_input = input("Admin Username: ")
password_input = input("Admin Passwort: ")

admin_user = config.get("DEFAULT", "admin_user")
admin_pass_hash = config.get("DEFAULT", "admin_pass_hash").encode()
endpoint = config.get("DEFAULT", "formspree_endpoint")

if username_input != admin_user or not bcrypt.checkpw(password_input.encode(), admin_pass_hash):
    print("Zugriff verweigert")
    sys.exit(1)

requests.post(endpoint, data={"message": f"{username_input} hat Zugriff auf das Tool angefordert"})
print("[✓] Admin authentifiziert")


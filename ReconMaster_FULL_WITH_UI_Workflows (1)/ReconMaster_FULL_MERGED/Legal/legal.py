from datetime import datetime
import sys

TERMS_FILE = "../Legal/TERMS.txt"
ACCEPT_LOG = "../Legal/ACCEPTED.db"

def legal_gate(username):
    print("\n===== LEGAL AGREEMENT =====\n")
    with open(TERMS_FILE, "r") as f:
        print(f.read())

    print("\n[1] I ACCEPT the terms")
    print("[2] I DO NOT ACCEPT")

    choice = input("\nSelect option (1/2): ").strip()

    if choice != "1":
        print("Access denied. Legal terms not accepted.")
        sys.exit(1)

    with open(ACCEPT_LOG, "a") as log:
        log.write(f"{datetime.utcnow()} | USER={username} | ACCEPTED\n")

    print("[✓] Legal terms accepted.\n")

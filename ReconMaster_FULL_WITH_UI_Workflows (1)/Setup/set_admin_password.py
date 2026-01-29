from configparser import ConfigParser
from pathlib import Path
import bcrypt
import getpass

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Admin" / "admin.conf"

def main():
    cfg = ConfigParser()
    cfg.read(CONF, encoding="utf-8")
    section = "DEFAULT"
    if cfg.has_section("ADMIN"):
        section = "ADMIN"
    if not cfg.has_section(section) and section != "DEFAULT":
        cfg.add_section(section)

    user = input("Admin username (default: admin): ").strip() or "admin"
    pw = getpass.getpass("New admin password: ")
    pw2 = getpass.getpass("Repeat password: ")
    if pw != pw2:
        print("Passwords do not match.")
        raise SystemExit(1)

    h = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

    # Ensure keys exist
    if section != "DEFAULT" and not cfg.has_section(section):
        cfg.add_section(section)
    cfg.set(section, "admin_user", user)
    cfg.set(section, "admin_pass_hash", h)

    # Keep existing formspree if present
    if not cfg.has_option(section, "formspree_endpoint"):
        cfg.set(section, "formspree_endpoint", "")

    with open(CONF, "w", encoding="utf-8") as f:
        cfg.write(f)

    print("Updated:", CONF)

if __name__ == "__main__":
    main()

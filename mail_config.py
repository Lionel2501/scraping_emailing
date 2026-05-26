import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def load_env_file():
    if not ENV_FILE.exists():
        return

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def get_smtp_config():
    load_env_file()

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    sender_email = os.getenv("SENDER_EMAIL", "")
    sender_password = os.getenv("SMTP_PASSWORD", "")

    if not sender_email or not sender_password:
        raise ValueError(
            "Config SMTP incomplete. Define SENDER_EMAIL and SMTP_PASSWORD "
            "in the environment or in a local .env file."
        )

    return smtp_server, smtp_port, sender_email, sender_password

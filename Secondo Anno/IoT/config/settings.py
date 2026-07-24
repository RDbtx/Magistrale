import os

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Flask session signing key
SECRET_KEY = os.environ.get("WEBAPP_SECRET", "secret_key_here")

# Web server port
PORT = int(os.environ.get("WEBAPP_PORT", "8000"))

# Symmetric key used to encrypt sensitive data
DB_ENCRYPTION_KEY = os.environ.get("DB_ENCRYPTION_KEY", "encription_key_here")

# Digital Replica schema for the house.
SCHEMA_TYPE = "house"
SCHEMA_PATH = os.environ.get("SCHEMA_PATH", os.path.join(_BASE, "src", "virtualization", "templates", "DHome.yaml"))

# Outdoor-temperature feed
OUTDOOR_REFRESH_S = int(os.environ.get("OUTDOOR_REFRESH_S", "150"))

# Seconds of NodeMCU silence before the device is considered offline.
STALE_AFTER_S = int(os.environ.get("STALE_AFTER_S", "45"))

# Outgoing email for fire-alarm alerts
SMTP_HOST = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = os.environ.get("SMTP_PORT", 587)
SMTP_USERNAME = os.environ.get("SMTP_USER", "mail_here@gmail.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "mail_password_here")
SMTP_USE_TLS = True
ALERT_FROM_EMAIL = os.environ.get("SMTP_USER", "mail_here@gmail.com")

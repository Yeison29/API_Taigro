import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


class EmailSettings:
    def __init__(self):
        self.MAIL_USERNAME = os.getenv("MAIL_USERNAME")
        self.MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
        self.MAIL_FROM = os.getenv("MAIL_FROM")
        self.MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
        self.MAIL_PORT = int(os.getenv("MAIL_PORT", 587))  # Valor predeterminado
        self.MAIL_SERVER = os.getenv("MAIL_SERVER")
        self.USE_CREDENTIALS = os.getenv("USE_CREDENTIALS") == "True"
        self.VALIDATE_CERTS = os.getenv("VALIDATE_CERTS") == "True"
        self.MAIL_STARTTLS = os.getenv("MAIL_STARTTLS") == "True"
        self.MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS") == "True"


email_settings = EmailSettings()

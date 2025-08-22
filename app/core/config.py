from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG: bool = True

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8'
    )

    # =========== APP =================
    SERVICE_NAME: str = "notify_service"
    SECRET_KEY: str = "test_secret_key"

    # ========== RABBITMQ ==============
    RABBITMQ_DEFAULT_USER: str = "guest"
    RABBITMQ_DEFAULT_PASS: str = "1234"
    RABBITMQ_DEFAULT_HOST: str = "localhost"
    RABBITMQ_DEFAULT_PORT: str = "5672"
    RABBITMQ_DEFAULT_VHOST: str = "/"
    DLQ_TTL_SECONDS: int = 604800000 # 7 days

    # =========== EMAIL ================
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "user"
    SMTP_PASS: str = "1234"
    SMTP_TIMEOUT: float = 15.0
    EMAIL_START_TLS: bool = True
    FROM_EMAIL: str = "user@mail.com"

    @property
    def RABBITMQ_URL(self):
        return (f"amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}@"
                f"{self.RABBITMQ_DEFAULT_HOST}:{self.RABBITMQ_DEFAULT_PORT}{self.RABBITMQ_DEFAULT_VHOST}")

settings = Settings()

print(settings.RABBITMQ_URL)
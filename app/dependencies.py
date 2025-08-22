from app.services.email import EmailService
from app.core.config import settings


def get_email_service() -> EmailService:
    return EmailService(
        host=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASS,
        from_email=settings.FROM_EMAIL,
        smtp_timeout=settings.SMTP_TIMEOUT,
        start_tls=settings.EMAIL_START_TLS,
    )

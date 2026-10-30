import smtplib
import ssl
import asyncio

from email.message import EmailMessage

from app.core.config import get_settings
from app.utilites.logger import logger


def send_welcome_email_sync( employee_name: str, employee_email: str) -> bool:

    settings = get_settings()

    message = EmailMessage()

    message["From"] = settings.smtp_from_email
    message["To"] = employee_email
    message["Subject"] = "Welcome to Our Company"

    message.set_content(
        f"Hello {employee_name},\n\n"
        "Welcome to our company CG VAK !\n\n"
        "Your employee registration has been completed "
        "successfully.\n\n"
        "We are happy to have you on our team.\n\n"
        "Regards,\n"
        "HR Department"
    )

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
            settings.smtp_host,
            settings.smtp_port,
            context=context,
            timeout=15
        ) as server:

            server.login(
                settings.smtp_username,
                settings.smtp_password
            )

            server.send_message(message)

        logger.info("Welcome email accepted by SMTP ")

        return True

    except (smtplib.SMTPException, OSError) as exc:

        logger.error("Welcome email failed | ""error_type=%s",type(exc).__name__)

        return False


async def send_welcome_email(employee_name: str,employee_email: str) -> bool:

    return await asyncio.to_thread(send_welcome_email_sync,employee_name,employee_email)

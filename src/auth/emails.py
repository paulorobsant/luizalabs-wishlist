import settings as settings
from email_message.services import send_email


def send_new_account_email(email_to: str, fullname: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Your account has been successfully created"

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/new_account.html',
        environment={
            "fullname": fullname
        },
    )


def send_reset_password_email(email_to: str, name: str, code: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Você solicitou a recuperação de senha da sua conta."

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/reset_password.html',
        environment={
            "name": name,
            "url": f"{settings.FRONTEND_URL}/reset-password/?code={code}"
        },
    )

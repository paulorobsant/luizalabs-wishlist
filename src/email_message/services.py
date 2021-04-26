import logging
import emails
import settings as settings

from jinja2 import Environment, FileSystemLoader, select_autoescape
from emails.template import JinjaTemplate


def send_email(
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment=None,
):
    if environment is None:
        environment = {}
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"

    jinja_instance = Environment(
        loader=FileSystemLoader(settings.EMAIL_TEMPLATES_DIR),
        autoescape=select_autoescape(['html', 'xml'])
    )

    email_template = jinja_instance.get_template(html_template)

    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=email_template.render(environment),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )

    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}

    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD

    response = message.send(to=email_to, smtp=smtp_options)
    logging.info(f"send email result: {response}")

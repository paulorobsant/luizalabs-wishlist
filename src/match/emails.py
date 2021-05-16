import settings as settings
from email_message.services import send_email


def send_connection_scheduled_email(email_to: str, name: str, challenge: str,
                                    date: str, time: str, is_mentor=False):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Your connection has been successfully scheduled"

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_scheduled_mentor.html' if is_mentor else '/emails/conn_scheduled_learner.html',
        environment={
            "name": name,
            "date": date,
            "time": time,
            "challenge": challenge
        },
    )


def send_connection_canceled_email(email_to: str, name: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Sua conexão foi cancelada."

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_canceled.html',
        environment={
            "name": name
        },
    )


def send_connection_requested_email(email_to: str, name: str, challenge: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Sua solicitação de conexão foi recebida com sucesso!"

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_requested.html',
        environment={
            "name": name,
            "challenge": challenge
        },
    )


def send_connection_mentor_invite_email(email_to: str, name: str, challenge: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Você foi convidado para ser um mentor."

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_mentor_invite.html',
        environment={
            "name": name,
            "challenge": challenge
        },
    )


def send_mentor_date_suggestion_email(email_to: str, learner_name: str, challenge: str, date: str, time: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Você foi convidado para aprender sobre {challenge}."

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_mentor_date_suggestion.html',
        environment={
            "learner_name": learner_name,
            "challenge": challenge,
            "date": date,
            "time": time
        },
    )


def send_learner_date_suggestion_email(email_to: str, mentor_name: str, challenge: str, date: str, time: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - O seu mentor sugeriu uma data para conexão."

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_learner_date_suggestion.html',
        environment={
            "learner_name": learner_name,
            "mentor_name": mentor_name,
            "challenge": challenge,
            "date": date,
            "time": time
        },
    )
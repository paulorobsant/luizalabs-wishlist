import settings as settings
from email_message.services import send_email


def send_connection_scheduled_email(email_to: str, target_conn_name: str, other_conn_name: str, challenge: str,
                                    start_datetime: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Your connection has been successfully scheduled"

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_scheduled.html',
        environment={
            "target_conn_name": target_conn_name,
            "start_datetime": start_datetime,
            "challenge": challenge,
            "other_conn_name": other_conn_name,
        },
    )


def send_connection_canceled_email(email_to: str, name: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Your connection has been canceled."

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
    subject = f"{project_name} - Your connection has been successfully requested."

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
    subject = f"{project_name} - You have been invited to mentor."

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_mentor_invite.html',
        environment={
            "name": name,
            "challenge": challenge
        },
    )


def send_mentor_date_suggestion_email(email_to: str, learner_name: str, mentor_name: str, challenge: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - You have been invited to learn with {mentor_name} about {challenge}."

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_mentor_date_suggestion.html',
        environment={
            "learner_name": learner_name,
            "mentor_name": mentor_name,
            "challenge": challenge
        },
    )


def send_learner_date_suggestion_email(email_to: str, learner_name: str, mentor_name: str, challenge: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - {learner_name} suggested a date for the connection."

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_learner_date_suggestion.html',
        environment={
            "learner_name": learner_name,
            "mentor_name": mentor_name,
            "challenge": challenge
        },
    )


def send_connection_remember_email(email_to: str, learner_name: str, mentor_name: str, challenge: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - {learner_name} suggested a date for the connection."

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template='/emails/conn_remember.html',
        environment={
            "learner_name": learner_name,
            "mentor_name": mentor_name,
            "challenge": challenge
        },
    )

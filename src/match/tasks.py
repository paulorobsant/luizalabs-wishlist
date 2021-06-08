import logging
import uuid
from datetime import timedelta

from celery import group
from sqlalchemy import literal, func

import settings
from core import utils
from core.database.session import Session
from match import services, emails, schemas
from match.models import MatchStep, MatchRequestStatus, MatchStatus, Match
from match.services import get_top_priorities, get_recommended_users_by_cluster
from periodic import app
from user import services as user_services

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


@app.task(queue=settings.QUEUE_EMAILS)
def process_alert_connection(conn_id: str):
    db = Session()

    connection = services.get_connection_by_id(db=db, conn_id=conn_id)
    mentor = user_services.get_user_by_id(db=db, id=connection.mentor_id)
    learner = user_services.get_user_by_id(db=db, id=connection.learner_id)

    print(f"ID: {connection.id} - Status: {connection.status} - Current Step: {connection.current_step}")

    if connection.current_step == MatchStep.MENTOR_SUGGEST_SCHEDULING:
        print('MatchStep.MENTOR_SUGGEST_SCHEDULING')
        emails.send_mentor_date_suggestion_email(
            email_to=learner.email,
            learner_name=learner.name,
            challenge=connection.data.get("keyword"),
            date=str(connection.start_datetime.date()),
            time=str(connection.start_datetime.time()),
        )

    elif connection.current_step == MatchStep.LEARNER_SUGGEST_SCHEDULING:
        print('MatchStep.LEARNER_SUGGEST_SCHEDULING')
        emails.send_learner_date_suggestion_email(
            email_to=mentor.email,
            mentor_name=mentor.name,
            challenge=connection.data.get("keyword"),
            date=str(connection.start_datetime.date()),
            time=str(connection.start_datetime.time()),
        )

    elif connection.current_step == MatchStep.SCHEDULING_CONFIRMED:
        print('MatchStep.SCHEDULING_CONFIRMED')
        emails.send_connection_scheduled_email(
            email_to=mentor.email,
            name=mentor.name,
            challenge=connection.data.get("keyword"),
            date=str(connection.start_datetime.date()),
            time=str(connection.start_datetime.time()),
            is_mentor=True
        )

        emails.send_connection_scheduled_email(
            email_to=learner.email,
            name=learner.name,
            challenge=connection.data.get("keyword"),
            date=str(connection.start_datetime.date()),
            time=str(connection.start_datetime.time()),
            is_mentor=False
        )

    updated_connection = schemas.MatchUpdate(**{"latest_alert": func.now()})
    services.update_connection(db=db, old_entry=connection, new_entry=updated_connection)


@app.task(name=settings.TASK_ALERT_CONNECTION)
def process_alert_connections():
    """
    This function is responsible for sending notifications regarding connections.
    """
    try:
        db = Session()

        connections = services.get_latest_updated_connections(db=db, n=10000, hours=24)

        tasks = [process_alert_connection.s(connection.id) for connection in connections]
        results = group(tasks)()
        print(results.get())

    except Exception as e:
        LOGGER.exception(e)


@app.task(name=settings.TASK_RECOMMENDATION_FIND_CONNECTION)
def get_recommended_users():
    """
    This function is responsible for obtaining the recommended users for a match request and creating a connection if
    the rules below are accepted.
    """
    try:
        db = Session()
        match_requests = get_top_priorities(db=db, n=10)

        for match_request in match_requests:
            match_challenge = match_request.data["keyword"]

            if not match_challenge:
                raise Exception("The challenge was not found.")

            recommended_users = get_recommended_users_by_cluster(db=db, challenge=match_challenge)

            # If no connection is found, then queue the request again with a higher priority.
            if not recommended_users:
                match_request_to_update = {"priority": match_request.priority + 1}
                match_request_to_update = schemas.MatchRequestUpdate(**match_request_to_update)

                # If this request has been processed more than 10 times. So let's overflow it and ignore it in the next
                # iterations.
                if match_request_to_update.priority > settings.MAX_NUMBER_ITERATIONS_FIND_CONNECTION:
                    match_request_to_update.status = MatchRequestStatus.OVERFLOWED

                services.update_match_request(
                    db=db,
                    old_entry=match_request,
                    new_entry=match_request_to_update
                )

                return

            for up in recommended_users:
                has_pending_connection = db.query(literal(True)).filter(
                    db.query(Match)
                        .filter_by(mentor_id=up.user_id, status=MatchStatus.IN_PROGRESS)
                        .filter_by(mentor_id=up.user_id, status=MatchStatus.PENDING)
                        .exists()
                ).scalar()

                if has_pending_connection:
                    continue

                new_connection = schemas.MatchInDB(**{
                    "mentor_id": up.user_id,
                    "learner_id": match_request.user_id,
                    "status": MatchStatus.PENDING,
                    "start_datetime": utils.get_datetime(),
                    "end_datetime": (utils.get_datetime() + timedelta(hours=1)),
                    "current_step": MatchStep.IN_PROGRESS,
                    "data": {
                        "meeting_url": f"https://meet.jit.si/gt-{uuid.uuid4().hex.upper()[0:6]}"
                    },
                    "is_approved": False
                })

                services.create_connection(db=db, entry=new_connection)
                services.remove_match_request(db=db, entry=match_request)

                # Send an invite to the mentor user
                emails.send_connection_mentor_invite_email(
                    email_to=up.user.email,
                    name=up.user.name,
                    challenge=match_challenge.capitalize(),
                    connection_url=settings.FRONTEND_URL
                )

                break

    except Exception as e:
        LOGGER.exception(e)

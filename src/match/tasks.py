import logging
import user.services as user_services

from sqlalchemy import literal
from datetime import timedelta

import settings
from core import utils
from core.database.session import Session
from match import services, schemas, models as match_models, emails
from match.models import MatchStep
from match.services import get_recommended_users_by_cluster, get_top_priorities
from periodic import app

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


@app.task(name=settings.TASK_ALERT_CONNECTION)
def process_alert_connections():
    """
    This function is responsible for sending notifications regarding connections.
    """
    try:
        session = Session()
        connections = services.get_latest_updated_connections(db=session, n=10, hours=24)

        for connection in connections:
            mentor = user_services.get_user_by_id(db=session, id=connection.mentor_id)
            learner = user_services.get_user_by_id(db=session, id=connection.learner_id)

            if connection.status == MatchStep.MENTOR_SUGGEST_SCHEDULING:
                emails.send_mentor_date_suggestion_email(
                    email_to=learner.email,
                    learner_name=learner.name,
                    challenge=connection.data["keyword"],
                    date=str(connection.start_datetime.date()),
                    time=str(connection.start_datetime.time()),
                )

            elif connection.status == MatchStep.LEARNER_SUGGEST_SCHEDULING:
                emails.send_learner_date_suggestion_email(
                    email_to=mentor.email,
                    mentor_name=mentor.name,
                    challenge=connection.data["keyword"],
                    date=str(connection.start_datetime.date()),
                    time=str(connection.start_datetime.time()),
                )

            elif connection.status == MatchStep.SCHEDULING_CONFIRMED:
                emails.send_connection_scheduled_email(
                    email_to=mentor.email,
                    name=mentor.name,
                    challenge=connection.data["keyword"],
                    date=str(connection.start_datetime.date()),
                    time=str(connection.start_datetime.time()),
                    is_mentor=True
                )

                emails.send_connection_scheduled_email(
                    email_to=learner.email,
                    name=learner.name,
                    challenge=connection.data["keyword"],
                    date=str(connection.start_datetime.date()),
                    time=str(connection.start_datetime.time()),
                    is_mentor=False
                )

    except Exception as e:
        LOGGER.exception(e)


@app.task(name=settings.TASK_RECOMMENDATION_FIND_CONNECTION)
def get_recommended_users():
    """
    This function is responsible for obtaining the recommended users for a match request and creating a connection if
    the rules below are accepted.
    """
    try:
        db_session = Session()
        match_requests = get_top_priorities(db=Session(), n=10)

        for match_request in match_requests:
            match_challenge = match_request.data["keyword"]

            if not match_challenge:
                raise Exception("The challenge was not found.")

            recommended_users = get_recommended_users_by_cluster(db=db_session, challenge=match_challenge)

            # If no connection is found, then queue the request again with a higher priority.
            if not recommended_users:
                match_request_to_update = {"priority": match_request.priority + 1}
                match_request_to_update = schemas.MatchRequestUpdate(**match_request_to_update)

                # If this request has been processed more than 10 times. So let's overflow it and ignore it in the next
                # iterations.
                if match_request_to_update.priority > settings.MAX_NUMBER_ITERATIONS_FIND_CONNECTION:
                    match_request_to_update.status = match_models.MatchRequestStatus.OVERFLOWED

                services.update_match_request(
                    db=db_session,
                    old_entry=match_request,
                    new_entry=match_request_to_update
                )

                return

            for up in recommended_users:
                has_pending_connection = db_session.query(literal(True)).filter(
                    db_session.query(match_models.Match)
                        .filter_by(mentor_id=up.user_id, status=match_models.MatchStatus.IN_PROGRESS)
                        .filter_by(mentor_id=up.user_id, status=match_models.MatchStatus.PENDING)
                        .exists()
                ).scalar()

                if has_pending_connection:
                    continue

                new_connection = schemas.MatchInDB(**{
                    "mentor_id": up.user_id,
                    "learner_id": match_request.user_id,
                    "status": match_models.MatchStatus.PENDING,
                    "start_datetime": utils.get_datetime(),
                    "end_datetime": (utils.get_datetime() + timedelta(hours=1)),
                    "current_step": match_models.MatchStep.IN_PROGRESS
                })

                services.create_connection(db=db_session, entry=new_connection)
                services.remove_match_request(db=db_session, entry=match_request)

                # Send an invite to the mentor user

                emails.send_connection_mentor_invite_email(
                    email_to=up.user.email,
                    name=up.user.name,
                    challenge=match_challenge.capitalize()
                )

                break
    except Exception as e:
        LOGGER.exception(e)

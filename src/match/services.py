import datetime as datetime

import pandas as pd
import numpy as np

from core.database.session import Session
from core.errors.exceptions import MatchNotFoundError, MatchTermNotFoundError
from core.utils import from_schema_to_model
from match import models
from match.classification.classifier import load_model, create_model, save_model
from match.classification.utils import must_retrain_the_model, create_challenges_request
from match.schemas import MatchRequestInDB, MatchInDB, MatchScheduleCreate, MatchReplaceGuest, MatchTermCreate, \
    MatchRequestUpdate, MatchUpdate, MatchTermUpdate
from user import models as user_models

"""
    Match Request
"""


def find_the_next_available_mentor():
    pass


def create_connection_request(db: Session, entry: MatchRequestInDB):
    new_entry = models.MatchRequest(
        status=entry.status,
        data=entry.data,
        priority=entry.priority,
        user_id=entry.user_id
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


def remove_match_request(db: Session, entry: models.MatchRequest):
    try:
        db.delete(entry)
        db.commit()
    except Exception as e:
        return e


def get_match_request_by_id(db: Session, id: str):
    return db.query(models.MatchRequest).filter(models.MatchRequest.id == id).first()


def update_match_request(db: Session, old_entry: models.MatchRequest, new_entry: MatchRequestUpdate):
    entry_to_update = from_schema_to_model(schema=new_entry, model=old_entry)

    db.add(entry_to_update)
    db.commit()
    db.refresh(entry_to_update)

    return entry_to_update


def get_top_priorities(db: Session, n=10):
    """
    Get the most priority requests
    """
    return db.query(models.MatchRequest) \
        .filter(models.MatchRequest.status != models.MatchRequestStatus.OVERFLOWED) \
        .order_by(models.MatchRequest.priority.desc()) \
        .limit(n) \
        .all()


def get_top_48h_priorities(db: Session, n=10):
    return db.query(models.Match) \
        .order_by(models.MatchRequest.priority.desc()) \
        .limit(n) \
        .all()


"""
    Match Connection
"""


def create_connection(db: Session, entry: MatchInDB):
    new_entry = models.Match(
        mentor_id=entry.mentor_id,
        learner_id=entry.learner_id,
        start_datetime=entry.start_datetime,
        end_datetime=entry.end_datetime,
        status=entry.status,
        current_step=entry.current_step
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


def update_connection(db: Session, old_entry: models.Match, new_entry: MatchUpdate):
    entry = from_schema_to_model(schema=new_entry, model=old_entry)

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


def approve_connection(db: Session, conn_id: str):
    db_entry = get_connection_by_id(db=db, conn_id=conn_id)

    if not db_entry:
        raise MatchNotFoundError

    new_entry = MatchUpdate(**{"is_approved": True})

    update_connection(db=db, old_entry=db_entry, new_entry=new_entry)


def get_connection_by_id(db: Session, conn_id: str):
    return db.query(models.Match).filter(models.Match.id == conn_id).first()


def get_all_connections_by_user_id(db: Session, user_id: str):
    return db.query(models.Match).filter((
                                                 models.Match.mentor_id == user_id or models.Match.learner_id == user_id) and models.Match.is_approved == True).first()


def cancel_connection_by_id(db: Session, conn_id: str):
    match = get_connection_by_id(db=db, conn_id=conn_id)

    if not match:
        raise MatchNotFoundError

    match.status = models.MatchStatus.CANCELLED

    db.add(match)
    db.commit()
    db.refresh(match)

    return match


def schedule_connection_by_id(db: Session, conn_id: str, entry: MatchScheduleCreate):
    match = get_connection_by_id(db=db, conn_id=conn_id)

    if not match:
        raise MatchNotFoundError

    match.start_datetime = datetime.datetime.strptime(entry.datetime, "%Y-%m-%dT%H:%M:%S%z")
    match.end_datetime = match.start_datetime + datetime.timedelta(hours=float(entry.duration))

    db.add(match)
    db.commit()
    db.refresh(match)

    return match


def replace_guest_from_connection(db: Session, conn_id: str, entry: MatchReplaceGuest):
    """
    Exchanges a guest from a connection
    """
    connection = get_connection_by_id(db=db, conn_id=conn_id)

    if not connection:
        raise MatchNotFoundError

    if connection.learner_id == entry.old_guest_id:
        connection.learner_id = entry.new_guest_id

    if connection.mentor_id == entry.old_guest_id:
        connection.mentor_id = entry.new_guest_id

    db.add(connection)
    db.commit()
    db.refresh(connection)


"""
    Match Terms
"""


def get_all_terms(db: Session, search_sentence: str = None):
    if search_sentence:
        return db.query(models.MatchTerm).filter(models.MatchTerm.label.ilike(search_sentence)).all()

    return db.query(models.MatchTerm).all()


def create_term(db: Session, entry: MatchTermCreate):
    last_term = db.query(models.MatchTerm).order_by(models.MatchTerm.value.desc()).first()
    next_value = last_term.value + 1 if last_term else 0

    new_entry = models.MatchTerm(
        label=entry.label,
        value=next_value
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


def get_term_by_label(db: Session, label: str):
    return db.query(models.MatchTerm).filter(models.MatchTerm.label.ilike(label)).all()


def get_term_by_id(db: Session, term_id: str):
    return db.query(models.MatchTerm).filter(models.MatchTerm.id == term_id).all()


def update_term(db: Session, old_entry: models.MatchTerm, new_entry: MatchTermUpdate):
    entry = from_schema_to_model(schema=new_entry, model=old_entry)

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


def approve_term(db: Session, term_id: str):
    db_entry = get_term_by_id(db=db, term_id=term_id)

    if not db_entry:
        raise MatchTermNotFoundError

    new_entry = MatchTermUpdate(**{"is_approved": True})

    update_term(db=db, old_entry=db_entry, new_entry=new_entry)


"""
    Recommendation
"""


def get_recommended_users_by_cluster(db: Session, challenge: str):
    """
    Get a group of users that can resolve a challenge
    """
    last_training = db.query(models.MatchTraining).order_by(models.MatchTraining.created_at.desc()).first()
    must_train_again = False

    if last_training:
        must_train_again = must_retrain_the_model(
            curr_trained_amount=last_training.total_prev_entries,
            new_trained_amount=last_training.total_new_entries
        )

    model_recommendation = load_model('expertises_model')

    if not model_recommendation or must_train_again:
        model_recommendation = create_training(db=db)

    if last_training and not must_train_again:
        save_or_update_training(
            db=db,
            total_prev_entries=last_training.total_prev_entries,
            total_new_entries=last_training.total_new_entries + 1
        )

    # Get some recommendations

    terms = [r.label for r in db.query(models.MatchTerm.label).all()]

    # Prevent words that don't exist

    if not challenge in terms:
        return []

    challenges_data = create_challenges_request(terms_list=terms, challenges=[challenge])
    challenges_df = pd.DataFrame([challenges_data], columns=terms)
    model_prediction = model_recommendation.predict(challenges_df)
    recommended_cluster = model_prediction[0] if len(model_prediction) else None

    # Filter all recommended users

    recommended_users = load_model('expertises_dataframe')
    recommended_users = recommended_users[recommended_users["clusters"] == recommended_cluster]

    # Get all data from recommended users

    recommended_users_ids = recommended_users["user_id"]
    recommended_users = db.query(user_models.UserProfile) \
        .filter(user_models.UserProfile.user_id.in_(recommended_users_ids)) \
        .order_by(user_models.UserProfile.total_conn_as_mentor.asc()) \
        .all()

    return recommended_users


def create_training(db: Session):
    terms = [r.label for r in db.query(models.MatchTerm.label).all()]
    user_profiles_df = pd.read_sql(db.query(user_models.UserProfile).statement, Session.bind)

    expertises_df = user_profiles_df[["expertises"]]
    expertises_df["expertises"] = [','.join(map(str, l)) for l in
                                   expertises_df['expertises']]  # Remove square brackets from rows
    expertises_df = expertises_df['expertises'].str.get_dummies(sep=',')  # Turn rows into columns
    expertises_df = expertises_df.reindex(columns=terms)  # Reorder columns
    expertises_df.fillna(value=0,
                         inplace=True)

    # Create the ML model
    model_recommendation = create_model(data_frame=expertises_df)
    save_model(model=model_recommendation, file_name='expertises_model')

    # Create a dataframe

    expertises_df["clusters"] = model_recommendation.predict(expertises_df)
    expertises_df["user_id"] = user_profiles_df["user_id"]

    save_model(model=expertises_df, file_name='expertises_dataframe')

    # Update the training logs

    save_or_update_training(db=db, total_prev_entries=len(user_profiles_df), total_new_entries=0)

    return model_recommendation


def save_or_update_training(db: Session, total_prev_entries: int, total_new_entries: int):
    last_training = db.query(models.MatchTraining).order_by(models.MatchTraining.created_at.desc()).first()

    if not last_training:
        last_training = models.MatchTraining()

    last_training.total_prev_entries = total_prev_entries
    last_training.total_new_entries = total_new_entries

    db.add(last_training)
    db.commit()
    db.refresh(last_training)

    return last_training

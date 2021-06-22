import json
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from core.database.deps import get_db
from core.errors.exceptions import MatchNotFoundError, Error
from core.http_session import get_current_active_user, get_current_active_superuser
from match import schemas, services, models, emails
from user.models import User

router = APIRouter()


# Terms

@router.get("/terms/")
def read_all_terms(*, search: str = None, db: Session = Depends(get_db)):
    try:
        all_terms = services.get_all_terms(db, search_sentence=search)
        return all_terms
    except Error as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/terms/{term_id}", response_model=List[schemas.MatchTermRead],
            dependencies=[Depends(get_current_active_superuser)])
def approve_term(*, term_id: str, db: Session = Depends(get_db)):
    try:
        services.approve_term(db, term_id=term_id)

        return JSONResponse(status_code=200, content={"data": "The term has been successfully approved."})
    except Error as e:
        raise HTTPException(status_code=400, detail=e.message)


# Connections

@router.get("/my_connections", description="Get all connections from connected user",
            response_model=schemas.MatchMyConnections)
def read_my_all_connections(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        next_connections = services.get_next_connections_by_user_id(db=db, user_id=current_user.id)
        past_connections = services.get_past_connections_by_user_id(db=db, user_id=current_user.id)

        return {
            "next_connections": next_connections,
            "past_connections": past_connections
        }
    except Error as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/request_conn")
def request_connection(*, entry: schemas.MatchRequestCreate, db: Session = Depends(get_db)):
    try:
        connection_request = schemas.MatchRequestInDB(
            data={
                "description": entry.description,
                "keyword": entry.keyword
            },
            priority=0,
            status=models.MatchRequestStatus.PENDING,
            user_id=entry.user_id
        )

        connection_request = services.create_connection_request(db=db, entry=connection_request)

        emails.send_connection_requested_email(
            email_to=connection_request.user.email,
            name=connection_request.user.name,
            challenge=entry.keyword.capitalize()
        )

        return JSONResponse(status_code=200, content={"message": "The request has been successfully created."})
    except Error as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/cancel_conn/{conn_id}")
def cancel_connection(*, conn_id: str, db: Session = Depends(get_db)):
    try:
        connection = services.cancel_connection_by_id(db=db, conn_id=conn_id)

        emails.send_connection_canceled_email(
            email_to=connection.mentor.email,
            name=connection.mentor.name
        )

        emails.send_connection_canceled_email(
            email_to=connection.learner.email,
            name=connection.learner.name
        )

        return JSONResponse(status_code=200, content={"message": "The connection has been successfully canceled."})
    except Error as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/schedule_conn/{conn_id}")
def reschedule_connection(*, conn_id: str, entry: schemas.MatchScheduleCreate, db: Session = Depends(get_db)):
    try:
        connection = services.schedule_connection_by_id(db=db, conn_id=conn_id, entry=entry)

        emails.send_connection_scheduled_email(
            email_to=connection.mentor.email,
            name=connection.mentor.name,
            date=str(connection.start_datetime.date()),
            time=str(connection.start_datetime.time()),
            is_mentor=True,
            challenge="____"
        )

        emails.send_connection_scheduled_email(
            email_to=connection.learner.email,
            name=connection.mentor.name,
            date=str(connection.start_datetime.date()),
            time=str(connection.start_datetime.time()),
            is_mentor=False,
            challenge="____"
        )

        return JSONResponse(status_code=200, content={"message": "The connection has been successfully scheduled."})
    except Error as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/{conn_id}", description="Read a connection by ID")
def read_connection(*, conn_id: str, db: Session = Depends(get_db)):
    try:
        connection = services.get_connection_by_id(db, conn_id=conn_id)

        if not connection:
            raise MatchNotFoundError

        return JSONResponse(status_code=200, content={"data": json.dumps(connection)})
    except Error as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/approve_conn/{conn_id}", description="Approves a connection recommended by the AI",
            dependencies=[Depends(get_current_active_superuser)])
def approve_connection(*, conn_id: str, db: Session = Depends(get_db)):
    try:
        services.approve_connection(db=db, conn_id=conn_id)
        return JSONResponse(status_code=200, content={"message": "The connection has been successfully approved."})
    except Error as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/create_review/")
def create_review(*, entry: schemas.MatchReviewCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_active_user)):
    try:
        services.create_review(db=db, entry=entry, user_id=current_user.id)
        return JSONResponse(status_code=200, content={"message": "The review has been successfully created."})
    except Error as e:
        raise HTTPException(status_code=400, detail=e.message)


# Machine Learning

@router.get("/reset_training/", dependencies=[Depends(get_current_active_superuser)])
def reset_training(*, db: Session = Depends(get_db)):
    try:
        services.create_training(db=db)
        return JSONResponse(status_code=200, content={"message": "The model has been successfully reset."})
    except:
        raise HTTPException(status_code=400, detail="Oops! Something went wrong. It was not possible to reset the "
                                                    "training.")

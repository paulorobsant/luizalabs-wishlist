import json
import uuid

from core.database.session import Session
from match import services as match_services
from user import services as user_services, schemas
from random import choices, randint
from faker import Faker

fake = Faker()


def get_random_terms(terms_list: list, n=1, selected_terms=None):
    if not selected_terms:
        selected_terms = []

    if len(selected_terms) < n:
        next_term = choices(terms_list)
        selected_terms.append(next_term[0])

        return get_random_terms(terms_list=terms_list, n=n, selected_terms=selected_terms)
    else:
        return selected_terms


def get_terms(terms_list):
    total_terms = randint(1, 3)
    items = get_random_terms(terms_list=terms_list, n=total_terms)

    return items


def add_all_users(n=10):
    db = Session()
    terms = match_services.get_all_terms(db=db)
    terms = [term.label for term in terms]
    users_count = user_services.get_total_of_users(db=db)

    if users_count >= n:
        return

    for x in range(n):
        user_name = fake.name()

        user = {
            "name": user_name,
            "email": fake.email(),
            "password": uuid.uuid4().hex.upper()[0:6],
            "username": user_name
        }

        user = schemas.UserCreate(**user)
        user = user_services.create_user(db=Session(), user=user)

        user_profile = {
            "challenges": get_terms(terms_list=terms),
            "expertises": get_terms(terms_list=terms),
            "data": json.dumps({"last_job": ""})
        }

        user_profile = schemas.UserProfileCreate(**user_profile)
        user_services.create_user_profile(db=Session(), user_id=user.id, entry=user_profile)


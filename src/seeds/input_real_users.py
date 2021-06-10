import json
import uuid
from csv import reader

from core.database.session import Session
import settings
from user import services as user_services, schemas


def add_real_users():
    with open(settings.BASE_PATH + '/seeds/input_real_users.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)

        for row in csv_reader:
            user_name = row[0]
            user_email = row[1]
            challenges = row[2].split(',')
            expertises = row[3].split(',')

            user = {
                "name": user_name,
                "email": user_email,
                "password": uuid.uuid4().hex.upper()[0:6],
                "username": user_name
            }

            user = schemas.UserCreate(**user)
            user = user_services.create_user(db=Session(), user=user)

            user_profile = {
                "challenges": challenges,
                "expertises": expertises,
                "data": json.dumps({"last_job": ""})
            }

            user_profile = schemas.UserProfileCreate(**user_profile)
            user_services.create_user_profile(db=Session(), user_id=user.id, entry=user_profile)

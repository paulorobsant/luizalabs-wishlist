from csv import reader

import settings
from core.database.session import Session
from match import schemas, services


def add_all_terms():
    with open(settings.BASE_PATH + '/seeds/input_terms.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)

        for row in csv_reader:
            term_label = row[0]
            term_value = row[1]

            term = services.get_term_by_label(db=Session(), label=term_label)

            if not term:
                term = {"label": term_label.lower(), "value": int(term_value), "is_approved": True}
                term = schemas.MatchTermCreate(**term)
                services.create_term(db=Session(), entry=term)
from csv import reader
import settings
from core.database.session import Session
from company import schemas, services


def add_all_companies():
    with open(settings.BASE_PATH + '/seeds/input_companies.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)

        for row in csv_reader:
            company_name = row[0]
            company_suffix = row[1]

            company = services.get_company_by_email_suffix(db=Session(), email_suffix=company_suffix)

            if not company:
                company = {"name": company_name, "email_suffix": company_suffix}
                company = schemas.CompanyCreate(**company)
                services.create_company(db=Session(), entry=company)
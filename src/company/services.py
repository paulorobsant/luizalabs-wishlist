from company import models, schemas
from core.database.session import Session


def get_company_by_email_suffix(db: Session, email_suffix: str):
    return db.query(models.Company).filter(models.Company.email_suffix == email_suffix).first()


def create_company(db: Session, entry: schemas.CompanyCreate):
    new_entry = models.Company(
        email_suffix=entry.email_suffix,
        name=entry.name,
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


def attach_user_to_company(db: Session, user_id: str, company_id: str):
    new_entry = models.UserCompany(
        company_id=company_id,
        user_id=user_id,
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

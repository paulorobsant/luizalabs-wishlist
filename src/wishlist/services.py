from core.database.session import Session
from core.utils import from_schema_to_model
from wishlist import models, schemas


def get_wishlist_by_user_id(db: Session, user_id: str):
    return db.query(models.Wishlist).filter(models.Wishlist.user_id == user_id).first()


def create_wishlist(db: Session, entry: schemas.WishlistCreate):
    new_entry = models.Wishlist(
        products_id=[entry.product_id],
        user_id=entry.user_id,
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


def update_wishlist(db: Session, entry: schemas.WishlistUpdate):
    current_entry = db.query(models.Wishlist).filter(models.Wishlist.user_id == entry.user_id).first()

    if not current_entry:
        raise Exception("Wishlist not found.")

    new_entry = from_schema_to_model(schema=entry, model=current_entry)

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

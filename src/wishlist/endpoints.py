from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from core.database.deps import get_db
from core.http_session import get_current_user
from wishlist import schemas, services
from user import services as user_services
from starlette import status
import requests
import requests_cache

router = APIRouter()

# Use cache mechanism to avoid multiple API calls to LuizaLabs
requests_cache.install_cache(cache_name='luizalabs_cache', backend='sqlite', expire_after=180)


@router.post("/", dependencies=[Depends(get_current_user)])
def add_product_to_wishlist(*, entry: schemas.WishlistCreate, db: Session = Depends(get_db)):
    try:
        db_user = user_services.get_user_by_id(db, user_id=entry.user_id)

        if not db_user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User not found."})

        db_wishlist = services.get_wishlist_by_user_id(db, user_id=entry.user_id)

        if not db_wishlist:
            services.create_wishlist(db=db, entry=entry)

            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Product successfully added to "
                                                                                    "wishlist."})

        if entry.product_id in db_wishlist.products_id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "The product is already "
                                                                                             "on the user's wishlist"})

        products_id = db_wishlist.products_id.copy()
        products_id.append(entry.product_id)

        new_entry = schemas.WishlistUpdate(
            id=db_wishlist.id,
            user_id=db_wishlist.user_id,
            products_id=products_id
        )

        services.update_wishlist(db=db, entry=new_entry)

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Product successfully added to wishlist."})

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"{e}"})


@router.post("/remove", dependencies=[Depends(get_current_user)])
def remove_product_to_wishlist(*, entry: schemas.WishlistCreate, db: Session = Depends(get_db)):
    try:
        db_user = user_services.get_user_by_id(db, user_id=entry.user_id)

        if not db_user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User not found."})

        db_wishlist = services.get_wishlist_by_user_id(db, user_id=entry.user_id)

        if not db_wishlist:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Wishlist is empty."})

        if entry.product_id not in db_wishlist.products_id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "The product is not on "
                                                                                             "the wishlist."})

        products_id = db_wishlist.products_id.copy()
        products_id.remove(entry.product_id)

        new_entry = schemas.WishlistUpdate(
            id=db_wishlist.id,
            user_id=db_wishlist.user_id,
            products_id=products_id
        )

        services.update_wishlist(db=db, entry=new_entry)

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Product successfully removed from wishlist."})

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"{e}"})


@router.get("/{user_id}", response_model=schemas.WishlistRead, dependencies=[Depends(get_current_user)])
def read_wishlist_by_user_id(user_id: str, db: Session = Depends(get_db)):
    try:
        db_wishlist = services.get_wishlist_by_user_id(db, user_id=user_id)

        if db_wishlist is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Wishlist not found."})

        products_id = []

        for product_id in db_wishlist.products_id:
            response = requests.get(f"http://challenge-api.luizalabs.com/api/product/{product_id}/")
            products_id.append(response.json())

        wishlist = schemas.WishlistRead(
            id=db_wishlist.id,
            user_id=db_wishlist.user_id,
            products_id=products_id
        )

        return wishlist

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"{e}"})

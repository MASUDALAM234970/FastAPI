
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, utils, schemas
from .. database import get_db

from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post(
    "/api/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
def test_user(user: schemas.UserCrete, db: Session = Depends(get_db)):

    try:
        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password
        new_user = models.User(**user.model_dump())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

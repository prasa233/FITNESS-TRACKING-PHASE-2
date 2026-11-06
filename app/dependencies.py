from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .auth import get_current_user


def get_authenticated_user(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    return current_user
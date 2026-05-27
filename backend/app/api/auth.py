from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import current_user
from app.auth.security import create_access_token, create_refresh_token, verify_password, hash_password
from app.database.session import get_db
from app.models.entities import Role, User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenPair, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])


def serialize_user(user: User) -> UserOut:
    return UserOut(id=user.id, email=user.email, full_name=user.full_name, roles=[role.name for role in user.roles])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=payload.email, full_name=payload.full_name, hashed_password=hash_password(payload.password))
    default_role = db.query(Role).filter_by(name="Client").first()
    if default_role:
        user.roles.append(default_role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return serialize_user(user)


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenPair(access_token=create_access_token(str(user.id)), refresh_token=create_refresh_token(str(user.id)))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return serialize_user(user)

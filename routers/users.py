import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_active_user, create_access_token, authenticate_user
from models import User, UserRole
from schemas import UserCreate, UserResponse, UserUpdate, Token, UserLogin
from datetime import timedelta
from crud import create_user
from jose import JWTError, jwt
from auth import security
from auth import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Простой тестовый токен
    test_payload = {"sub": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)}
    access_token = jwt.encode(test_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/me", response_model=UserResponse)
def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if user_update.name:
        current_user.name = user_update.name
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/check-auth")
def check_auth(current_user: User = Depends(get_current_active_user)):
    return {"message": "Authenticated", "user": current_user.email, "role": current_user.role}


@router.post("/verify-token")
def verify_token(token_data: dict, db: Session = Depends(get_db)):
    try:
        token = token_data.get("token")
        if not token:
            return {"valid": False, "error": "No token provided"}

        payload = jwt.decode(token, "your-secret-key-very-secure-and-long", algorithms=["HS256"])
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if user:
            return {"valid": True, "user": user.email, "role": user.role}
        return {"valid": False, "error": "User not found"}
    except JWTError as e:
        return {"valid": False, "error": str(e)}

@router.get("/debug-auth")
def debug_auth(credentials = Depends(security), db: Session = Depends(get_db)):
    if credentials:
        return {"status": "has_credentials", "token": credentials.credentials}
    else:
        return {"status": "no_credentials"}
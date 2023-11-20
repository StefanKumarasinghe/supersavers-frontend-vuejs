from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

class User(BaseModel):
    username: str
    email: str
    hashed_password: str


users_db = []

class SecurityConfig:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    SECRET_KEY = "YOUR_SECRET_KEY"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

class PasswordHashing:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    @staticmethod
    def hash_password(password: str) -> str:
        return PasswordHashing.pwd_context.hash(password)
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordHashing.pwd_context.verify(plain_password, hashed_password)
class TokenGenerator:
    # Generate access token
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SecurityConfig.SECRET_KEY, algorithm=SecurityConfig.ALGORITHM)
        return encoded_jwt
class UserManager:
    
    def is_valid_email(email: str) -> bool:
     
     email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
     return bool(re.match(email_pattern, email))
    @staticmethod
    async def register_user(user: User) -> dict:
    # Check if username only includes characters with no spacing
        if not user.username.isalnum():
            raise HTTPException(status_code=400, detail="Username should only include alphanumeric characters.")

        # Check if the username is not existing
        if any(existing_user["username"] == user.username for existing_user in users_db):
            raise HTTPException(status_code=400, detail="Username already exists.")
        import re
        # Check if email is valid
        if not bool(re.match(re.compile(r"[^@]+@[^@]+\.[^@]+"), user.email)):
            raise HTTPException(status_code=400, detail="Invalid email format.")

        # Check if the password is at least 8 characters
        if len(user.hashed_password) < 8:
            raise HTTPException(status_code=400, detail="Password should be at least 8 characters.")

        hashed_password = PasswordHashing.hash_password(user.hashed_password)
        user_data = {"username": user.username, "email": user.email, "hashed_password": hashed_password}
        users_db.append(user_data)

        access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenGenerator.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        return {"message": "User registered successfully", "access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def get_current_user(token: str = Depends( SecurityConfig.oauth2_scheme)):
     credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
     )
     try:
        payload = jwt.decode(token, SecurityConfig.SECRET_KEY, algorithms=[SecurityConfig.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
     except JWTError:
        raise credentials_exception
     return username
    @staticmethod
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
        user = next((x for x in users_db if x["username"] == form_data.username), None)
        if user is None or not PasswordHashing.verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenGenerator.create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
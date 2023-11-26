from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets
from email.mime.text import MIMEText
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import re
from validate_email_address import validate_email

class User(BaseModel):
    username: str
    email: str
    hashed_password: str

users_db = []

class PasswordHashing:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash_password(password: str) -> str:
        return PasswordHashing.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordHashing.pwd_context.verify(plain_password, hashed_password)

class SecurityConfig:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    SECRET_KEY = secrets.token_urlsafe(32)  # Use a more secure method to load the secret key
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenGenerator:
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
    @staticmethod
    async def register_user(user: User) -> dict:
        # Check if username only includes characters with no spacing
        if not user.username.isalnum():
            raise HTTPException(status_code=400, detail="Username should only include alphanumeric characters.")

        # Check if the username is not existing
        if any(existing_user["username"] == user.username for existing_user in users_db):
            raise HTTPException(status_code=400, detail="Username already exists.")

        # Check if email is valid
        if not bool(re.match(re.compile(r"[^@]+@[^@]+\.[^@]+"), user.email)):
            raise HTTPException(status_code=400, detail="Invalid email format.")

        # Check if the email is unique
        if any(existing_user["email"] == user.email for existing_user in users_db):
            raise HTTPException(status_code=400, detail="Email already registered.")

        # Check if the password is at least 8 characters
        if len(user.hashed_password) < 8:
            raise HTTPException(status_code=400, detail="Password should be at least 8 characters.")

        hashed_password = PasswordHashing.hash_password(user.hashed_password)
        user_data = {"username": user.username, "email": user.email, "hashed_password": hashed_password}
        users_db.append(user_data)

        access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenGenerator.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        verification_token = secrets.token_urlsafe(32)
        user_data["verification_token"] = verification_token

        # Send verification email
        await UserManager.send_verification_email(user.email, verification_token)

        return {"message": "User registered successfully", "access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def send_verification_email(email: str, verification_token: str):
        verification_link = f"http://localhost:8080/verify-email?token={verification_token}"
        email_subject = "Verify Your Email"
        email_body = f"Click the following link to verify your email: {verification_link}"

        # Use your email sending logic here
        # For example, you can use the Gmail API or an SMTP server

        # Set up the Gmail service
        service = PasswordRecoveryManager.get_gmail_service()

        # Create the email message
        message = MIMEText(email_body)
        message["to"] = email
        message["subject"] = email_subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        # Send the email
        try:
            message = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
            print("Verification email sent successfully:", message)
        except Exception as error:
            print("An error occurred while sending verification email:", error)

    @staticmethod
    async def get_current_user(token: str = Depends(SecurityConfig.oauth2_scheme)):
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
        # Check if the provided username is a valid email
        is_email = validate_email(form_data.username)
        if is_email:
            # If it's an email, try to find the user by email
            user = next((x for x in users_db if x["email"] == form_data.username), None)
        else:
            # If it's not an email, find the user by username
            user = next((x for x in users_db if x["username"] == form_data.username), None)
        if user is None or not PasswordHashing.verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenGenerator.create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}

class PasswordRecoveryManager:
    recovery_tokens: Dict[str, str] = {}

    @staticmethod
    def is_email_verified(username: str = Depends(UserManager.get_current_user)):
        user = next((x for x in users_db if x["username"] == username), None)
        if user is None or not user.get("is_verified", False):
            raise HTTPException(status_code=403, detail="Email not verified")
        return user

    @staticmethod
    async def request_password_reset(email: str):
        user = next((x for x in users_db if x["email"] == email), None)
        if user is None:
            raise HTTPException(status_code=404, detail="Email not found.")

        recovery_token = secrets.token_urlsafe(32)
        PasswordRecoveryManager.recovery_tokens[recovery_token] = user["username"]

        email_subject = "Password Reset Request"
        email_body = f"Dear {user['username']},\n\nPlease use the following link to reset your password:\n\n" \
                      f"Reset Link: https://your-website.com/reset-password?token={recovery_token}\n\n" \
                      "If you didn't request this, please ignore this email.\n\nBest regards,\nYour Website Team"

        try:
            await PasswordRecoveryManager.send_email(user["email"], email_subject, email_body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

        return {"message": "Password reset requested. Check your email for instructions."}

    @staticmethod
    async def verify_email(verification_token: str):
        user = next((x for x in users_db if x.get("verification_token") == verification_token), None)
        if user:
            user["is_verified"] = True
            user.pop("verification_token")

            return {"message": "Email verification successful."}
        else:
            raise HTTPException(status_code=400, detail="Invalid verification token.")

    @staticmethod
    def get_gmail_service():
        CREDENTIALS_FILE = 'key.json'
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json')

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        return service

    @staticmethod
    async def send_email(to_email: str, subject: str, body: str):
        service = PasswordRecoveryManager.get_gmail_service()

        message = MIMEText(body)
        message["to"] = to_email
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        try:
            message = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
            print("Message sent successfully:", message)
        except Exception as error:
            print("An error occurred:", error)

    @staticmethod
    async def reset_password(recovery_token: str, new_password: str):
        username = PasswordRecoveryManager.recovery_tokens.get(recovery_token)
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid recovery token.")

        user = next((x for x in users_db if x["username"] == username), None)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")

        user["hashed_password"] = PasswordHashing.hash_password(new_password)

        del PasswordRecoveryManager.recovery_tokens[recovery_token]

        return {"message": "Password reset successfully."}

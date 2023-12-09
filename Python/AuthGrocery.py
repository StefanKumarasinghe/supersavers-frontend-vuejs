from typing import Optional, Dict
from fastapi import HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import secrets
from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from validate_email_address import validate_email
from pydantic import BaseModel
from botocore.exceptions import ClientError
import boto3
import Data


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
    SECRET_KEY = secrets.token_urlsafe(32)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

class TokenGenerator:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=24*60)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SecurityConfig.SECRET_KEY, algorithm=SecurityConfig.ALGORITHM)
        return encoded_jwt

Base = declarative_base()

class UserModel(BaseModel):
    username: str
    email: str
    hashed_password:str

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    verification_token = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)

aws_mysql_config = {
    "username": "supersavers",
    "password": "Superdoc69*",
    "host": "supersaver.cbbcfmfp6t7q.us-east-1.rds.amazonaws.com",
    "port": "3306",
    "database": "supersaver",
}

connection_string = f"mysql+mysqlconnector://{aws_mysql_config['username']}:{aws_mysql_config['password']}@{aws_mysql_config['host']}:{aws_mysql_config['port']}/{aws_mysql_config['database']}"

engine = create_engine(connection_string, pool_pre_ping=True)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserManager:

    @staticmethod
    async def register_user(user: User) -> dict:
        if not user.username.isalnum():
            raise HTTPException(status_code=400, detail="Username should only include alphanumeric characters.")

        if UserManager.is_username_exists(user.username):
            raise HTTPException(status_code=400, detail="Username already exists.")

        if not validate_email(user.email):
            raise HTTPException(status_code=400, detail="Invalid email format.")

        if UserManager.is_email_exists(user.email):
            raise HTTPException(status_code=400, detail="Email already registered.")

        if len(user.hashed_password) < 8:
            raise HTTPException(status_code=400, detail="Password should be at least 8 characters.")

        hashed_password = PasswordHashing.hash_password(user.hashed_password)
        verification_token = secrets.token_urlsafe(32)
        user_data = User(username=user.username, email=user.email, hashed_password=hashed_password,verification_token=verification_token)
        
        db = SessionLocal()
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        db.close()

        access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenGenerator.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        await UserManager.send_verification_email(user.email, verification_token)

        return {"message": "User registered successfully", "access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def is_username_exists(username: str) -> bool:
        db = SessionLocal()
        return db.query(User).filter(User.username == username).first() is not None

    @staticmethod
    def is_email_exists(email: str) -> bool:
        db = SessionLocal()
        return db.query(User).filter(User.email == email).first() is not None

    @staticmethod
    def get_user_by_username(username: str) -> User:
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()
        return user
    @staticmethod
    def get_user_by_token(token: str) -> User:
        db = SessionLocal()
        user = db.query(User).filter(User.verification_token == token).first()
        db.close()
        return user

    @staticmethod
    def get_user_by_email(email: str) -> User:
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        db.close()
        return user
    
    @staticmethod
    def get_current_user(token: str = Depends(SecurityConfig.oauth2_scheme)):
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

            # Use SQLAlchemy to get the user from the database by username
            user = UserManager.get_user_by_username(username)
            if user is None:
                raise credentials_exception

        except JWTError:
            raise credentials_exception

        return username


    @staticmethod
    async def send_verification_email(email: str, verification_token: str):
        user = UserManager.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")

        verification_link = f"{Data.endpoint}/verify?token={verification_token}"
        email_subject = "Verify Your Email"

        email_body = f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: 'Arial', sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f4f4f4;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: auto;
                            padding: 20px;
                            background-color: #ffffff;
                            border-radius: 10px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        }}
                        p {{
                            font-size: 16px;
                            line-height: 1.6;
                            color: #333333;
                        }}
                        a {{
                            color: #3498db;
                            text-decoration: none;
                        }}
                        a:hover {{
                            color: #1e87c5;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                    <h1>GroceryAPI</h1>
                        <p>Click the following link to verify your email:</p>
                        <p><a href="{verification_link}">Verify</a></p>
                        <small>Make sure you verify your email within 1 hour as the token will expire</small>
                    </div>
                </body>
            </html>
        """

        ses_client = PasswordRecoveryManager.get_ses_client()

        email_message = {
            'Destination': {
                'ToAddresses': [email],
            },
            'Message': {
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': email_body,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': email_subject,
                },
            },
            'Source': 'verify@supersavers.au',  # Replace with your verified sender email address
        }

        try:
            response = ses_client.send_email(**email_message)
            print("Email sent successfully:", response)
        except ClientError as e:
            print("An error occurred:", e)

    @staticmethod
    async def resend_verification_email(username: str):
        db = SessionLocal()

        # Fetch the user within the same session
        user = db.query(User).filter(User.username == username).first()

        if user is None:
            db.close()
            raise HTTPException(status_code=404, detail="User not found.")

        if user.is_verified:
            db.close()
            raise HTTPException(status_code=400, detail="User already verified.")

        # Generate a new access token
        new_access_token = secrets.token_urlsafe(32)

        # Update the verification_token
        user.verification_token = new_access_token

        # Commit the changes to the database
        db.commit()

        # Send the verification email
        await UserManager.send_verification_email(user.email, new_access_token)

        # Close the session after all operations are done
        db.close()

    @staticmethod
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        is_email = validate_email(form_data.username)
        if is_email:
            user = UserManager.get_user_by_email(form_data.username)
        else:
            user = UserManager.get_user_by_username(form_data.username)

        if user is None or not PasswordHashing.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenGenerator.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        return {"access_token": access_token, "token_type": "bearer"}

class PasswordRecoveryManager:
    recovery_tokens: Dict[str, str] = {}


    @staticmethod
    async def is_email_verified(username: str = Depends(UserManager.get_current_user)) -> Dict[str, str]:
        user = UserManager.get_user_by_username(username)
        if user is None or not user.is_verified:
            raise HTTPException(status_code=403, detail="Email not verified")
        else:
            return  username
        
       

    @staticmethod
    async def request_password_reset(email: str):
        user = UserManager.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="Email not found.")

        recovery_token = secrets.token_urlsafe(32)
        PasswordRecoveryManager.recovery_tokens[recovery_token] = user.username

        email_subject = "Password Reset Request"
        email_body = f"Dear {user.username},\n\nPlease use the following link to reset your password:\n\n" \
                      f"Reset Link: https://your-website.com/reset-password?token={recovery_token}\n\n" \
                      "If you didn't request this, please ignore this email.\n\nBest regards,\nYour Website Team"

        try:
            await PasswordRecoveryManager.send_email(user.email, email_subject, email_body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
        return {"message": "Password reset requested. Check your email for instructions."}

    @staticmethod
    async def verify_email(token: str):
        user = UserManager.get_user_by_token(token)
        if user:
            db = SessionLocal()
            user = db.query(User).filter(User.username == user.username).first()
            user.is_verified = True
            user.verification_token = None
# Commit the changes to the database
            db.commit()
            db.close()
            return {"message": "Email verification successful."}
        else:
            raise HTTPException(status_code=400, detail="Invalid verification token.")

    @staticmethod
    def get_ses_client(region_name='ap-southeast-2'):
        ses_client = boto3.client('ses', region_name=region_name)
        return ses_client

    @staticmethod
    async def send_email(to_email: str, subject: str, body: str):
        ses_client = PasswordRecoveryManager.get_ses_client()

        email_message = {
            'Destination': {
                'ToAddresses': [to_email],
            },
            'Message': {
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            'Source': 'verify@supersavers.au',  # Replace with your verified sender email address
        }

        try:
            response = ses_client.send_email(**email_message)
            print("Email sent successfully:", response)
        except ClientError as e:
            print("An error occurred:", e)

    @staticmethod
    async def reset_password(recovery_token: str, new_password: str):
        username = PasswordRecoveryManager.recovery_tokens.get(recovery_token)
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid recovery token.")

        user = UserManager.get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")

        user.hashed_password = UserManager.hash_password(new_password)

        del PasswordRecoveryManager.recovery_tokens[recovery_token]

        return {"message": "Password reset successfully."}

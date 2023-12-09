from typing import List, Optional
from fastapi import HTTPException, Depends, Body, status
from pydantic import BaseModel
import AuthGrocery
import DealsBulk
import threading
from time import sleep
import firebase_admin
from firebase_admin import credentials, messaging
import logging
import random
import re
from sqlalchemy import create_engine, Column, Integer, String, DateTime, or_
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import DeclarativeMeta

# Initialize Firebase Admin SDK (replace 'path/to/your/serviceAccountKey.json' with your own service account key)
try:
    cred = credentials.Certificate('firebase.json')
    firebase_admin.initialize_app(cred)
except Exception as e:
    logging.error(f"Error initializing Firebase: {e}")
    # Handle the error appropriately, such as exiting the application or logging an error.


Base = declarative_base()
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(255), index=True)  # Adjust the length as needed
    item_name = Column(String(255))  # Adjust the length as needed
    item_description = Column(String(255))  # Adjust the length as needed
    image = Column(String(255))  # Adjust the length as needed
    woolworths_code = Column(String(50))  # Adjust the length as needed
    coles_code = Column(String(50))  # Adjust the length as needed
    iga_code = Column(String(50))  # Adjust the length as needed
    registration_token = Column(String(255))  # Adjust the length as needed
    timestamp = Column(DateTime(timezone=True), server_default=func.now())



aws_mysql_config = {
    "username": "supersavers",
    "password": "Superdoc69*",
    "host": "supersaver.cbbcfmfp6t7q.us-east-1.rds.amazonaws.com",
    "port": "3306",
    "database": "supersaver",
}

connection_string = f"mysql+mysqlconnector://{aws_mysql_config['username']}:{aws_mysql_config['password']}@{aws_mysql_config['host']}:{aws_mysql_config['port']}/{aws_mysql_config['database']}"

engine = create_engine(connection_string, pool_pre_ping=True)
print(engine)

# This line should be placed here after creating the engine
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()

class Item(BaseModel):
    user: Optional[str] = None
    name: str
    woolworths_code: str
    coles_code: str
    iga_code: str
    registration_token: str
    image: str
    description: str

class Item_Remove(BaseModel):  # Renamed Item_Remove to follow Python naming conventions
    woolworths_code: str
    coles_code: str
    iga_code: str

async def add_item(item: Item = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    db = SessionLocal()
    try:
        # Check if the item already exists
        existing_item = db.query(Notification).filter(Notification.user == current_user, Notification.item_name == item.name).first()
        if existing_item:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Item {item.name} already exists for user {current_user}.")

        # If not, add the item to the notification table
        new_notification = Notification(
            user=current_user,
            item_name=item.name,
            item_description=item.description,
            image=item.image,
            woolworths_code=item.woolworths_code,
            coles_code=item.coles_code,
            iga_code=item.iga_code,
            registration_token=item.registration_token,  # You need to replace this with a valid registration token
        )
        db.add(new_notification)
        db.commit()

        return {'message': f'Item {item.name} added by user {current_user}.'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {e}')
    finally:
        db.close()

async def retrieve_all_item(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    db = SessionLocal()
    try:
        # Fetch items from the database for the specified user
        user_items = db.query(Notification).filter(Notification.user == current_user).all()

        # Convert Notification models to Item models
        items = [
            Item(
                user=item.user,
                name=item.item_name,
                woolworths_code=item.woolworths_code,
                coles_code=item.coles_code,
                iga_code=item.iga_code,
                registration_token=item.registration_token,
                image=item.image,
                description=item.item_description,
            )
            for item in user_items
        ]

        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {e}')
    finally:
        db.close()


async def remove_item(item: Item_Remove = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    db = SessionLocal()
    try:
        # Try to find the item in the database
        db_item = db.query(Notification).filter(
            or_(
                Notification.woolworths_code == item.woolworths_code,
                Notification.coles_code == item.coles_code,
                Notification.iga_code == item.iga_code
            ),
            Notification.user == current_user
        ).first()

        if db_item:
            # Check if the user has permission to remove this item
            if db_item.user == current_user:
                # Remove the item from the database
                db.delete(db_item)
                db.commit()
                return {'message': f'Item {db_item.item_name} removed successfully by user {current_user}.'}
            else:
                raise HTTPException(status_code=403, detail=f'User {current_user} does not have permission to remove this item.')
        else:
            raise HTTPException(status_code=404, detail=f'Item not found for user {current_user}.')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {e}')
    finally:
        db.close()

async def check_and_notify():
    products = []
    try:
        woolies_products = await DealsBulk.half_price_deals_woolies_bulk()
        products.extend(woolies_products)
    except Exception as e:
        logging.error(f"Error during Woolworths product retrieval: {e}")

    try:
        iga_products = await DealsBulk.half_price_deals_iga_bulk()
        products.extend(iga_products)
    except Exception as e:
        logging.error(f"Error during IGA product retrieval: {e}")

    try:
        coles_products = await DealsBulk.half_price_deals_coles_bulk()
        products.extend(coles_products)
    except Exception as e:
        logging.error(f"Error during Coles product retrieval: {e}")
    
    db = SessionLocal()
    db_products = db.query(Notification).all()
    db.close()

    for stored_item in db_products:
        for product in products:
            product_code_str = str(product.stockcode)
            if stored_item.woolworths_code == product_code_str:
                threading.Thread(target=send_notification_delayed, args=(stored_item, "Woolies", 0)).start()
            elif stored_item.coles_code == product_code_str:
                threading.Thread(target=send_notification_delayed, args=(stored_item, "Coles", 60)).start()
            elif stored_item.iga_code == product_code_str:
                threading.Thread(target=send_notification_delayed, args=(stored_item, "IGA", 120)).start()

def send_notification_delayed(stored_item, store, delay_in_seconds):
    sleep(delay_in_seconds)
    send_notification(stored_item, store)

def is_valid_registration_token(token):
    return re.match(r'^[a-zA-Z0-9_-]+$', token) is not None

def send_notification(stored_item, store):
    registration_token = stored_item.registration_token

    title_phrases = [
        "Price Alert",
        "Amazing Deals",
        "Special Offer",
        "Limited Time Sale",
        "Exclusive Discounts",
        "Don't Miss Out!",
        "Down Down: Unbeatable Prices!",
        "You're in Luck!",
    ]

    body_phrases = [
        "Do not miss out on this amazing deal!",
        "Limited time offer just for you!",
        "Exclusive discounts on your favorite items!",
        "Hurry, special prices for a limited time!",
        "Unbeatable prices you can't resist!",
        "You wanted this, so don't miss out!",
    ]

    selected_title = random.choice(title_phrases)
    selected_body = random.choice(body_phrases)

    message = messaging.Message(
        notification=messaging.Notification(
            title=selected_title,
            body=f"{selected_body} {stored_item.name} is now on sale! at {store}",
        ),
        token=registration_token,
        android=messaging.AndroidConfig(ttl=86400),
    )

    try:
        response = messaging.send(message)
        logging.info("Successfully sent message: %s", response)
    except Exception as e:
        logging.error("Error sending message: %s", e)

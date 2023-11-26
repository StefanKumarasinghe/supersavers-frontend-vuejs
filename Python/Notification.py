from typing import List, Optional
from fastapi import HTTPException, Depends, Body
from pydantic import BaseModel
import AuthGrocery
import Deals
import firebase_admin
from firebase_admin import credentials, messaging
import logging
import random
import re
from werkzeug.utils import secure_filename

# Initialize Firebase Admin SDK (replace 'path/to/your/serviceAccountKey.json' with your own service account key)
try:
    cred = credentials.Certificate('firebase.json')
    firebase_admin.initialize_app(cred)
except Exception as e:
    logging.error(f"Error initializing Firebase: {e}")
    # Handle the error appropriately, such as exiting the application or logging an error.

class Item(BaseModel):
    user: Optional[str] = None
    name: str
    registration_token: str
    woolworths_code: str
    coles_code: str
    iga_code: str
    image: str
    description: str

codes_storage: List[Item] = []

async def add_item(item: Item = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    item.user = current_user
    codes_storage.append(item)
    return {'message': f'Item {item.name} added by user {current_user}.'}

async def retrieve_all_item(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    user_items = [item for item in codes_storage if item.user == current_user]
    return user_items

async def remove_item(item: Item = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    try:
        index_to_remove = next((i for i, stored_item in enumerate(codes_storage) if stored_item.woolworths_code == item.woolworths_code), None)
        
        if index_to_remove is not None:
            if codes_storage[index_to_remove].user == current_user:
                removed_item = codes_storage.pop(index_to_remove)
                return {'message': f'Item {removed_item.name} removed successfully by user {current_user}.'}
            else:
                raise HTTPException(status_code=403, detail=f'User {current_user} does not have permission to remove this item.')
        else:
            index_to_remove = next((i for i, stored_item in enumerate(codes_storage) if stored_item.coles_code == item.coles_code), None)
            
            if index_to_remove is not None and codes_storage[index_to_remove].user == current_user:
                removed_item = codes_storage.pop(index_to_remove)
                return {'message': f'Item {removed_item.name} removed successfully by user {current_user}.'}
                
            index_to_remove = next((i for i, stored_item in enumerate(codes_storage) if stored_item.iga_code == item.iga_code), None)
            
            if index_to_remove is not None and codes_storage[index_to_remove].user == current_user:
                removed_item = codes_storage.pop(index_to_remove)
                return {'message': f'Item {removed_item.name} removed successfully by user {current_user}.'}
            
            raise HTTPException(status_code=404, detail=f'Item not found for user {current_user}.')
    except (ValueError, IndexError, KeyError) as e:
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {e}')

async def check_and_notify():
    products = []
    try:
        woolies_products = await Deals.half_price_deals_woolies()
        products.extend(woolies_products)
    except Exception as e:
        logging.error(f"Error during Woolworths product retrieval: {e}")

    try:
        iga_products = await Deals.half_price_deals_iga()
        products.extend(iga_products)
    except Exception as e:
        logging.error(f"Error during IGA product retrieval: {e}")

    try:
        coles_products = await Deals.half_price_deals_coles()
        products.extend(coles_products)
    except Exception as e:
        logging.error(f"Error during Coles product retrieval: {e}")

    for stored_item in codes_storage:
        for product in products:
            product_code_str = str(product.stockcode)
            if (
                stored_item.woolworths_code == product_code_str
                or stored_item.coles_code == product_code_str
                or stored_item.iga_code == product_code_str
            ):
                send_notification(stored_item)

def is_valid_registration_token(token):
    return re.match(r'^[a-zA-Z0-9_-]+$', token) is not None

def send_notification(stored_item):
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
            body=f"{selected_body} {stored_item.name} is now on sale!",
        ),
        token=registration_token,
    )

    try:
        response = messaging.send(message)
        logging.info("Successfully sent message: %s", response)
    except Exception as e:
        logging.error("Error sending message: %s", e)



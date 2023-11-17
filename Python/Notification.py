from typing import List, Optional
import AuthGrocery
import Deals
from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

codes_storage={} 

class Item(BaseModel):
    item: str
    woolworths_code: str
    coles_code: str
    iga_code: str


async def add_item(item: Item = Body(...),current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    codes_storage.append({
        'user': current_user,
        'item': item.item,
        'woolworths_code': item.woolworths_code,
        'coles_code': item.coles_code,
        'iga_code': item.iga_code
    })
    return {'message': f'Item {item.item} removed added by user {current_user}.'}
async def remove_item(item: Item = Body(...),current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    codes_storage.remove({
        'user': current_user,
        'item': item.item
    })
    return {'message': f'Item {item.item} removed successfully by user {current_user}.'}
async def check_and_notify():
    products=[]
    products.append(await Deals.half_price_deals_woolies())
    products.append(await Deals.half_price_deals_iga())
    for stored_item in codes_storage:
        for product in products:
            if (
                stored_item['woolworths_code'] == product.stockcode_w
                or stored_item['coles_code'] == product.stockcode_c
                or stored_item['iga_code'] == product.stockcode_i
            ):
                send_notification(stored_item, product)
def send_notification(stored_item, matching_product):
    print(f"Notification: Item {stored_item['item']} matched with {matching_product.source} deal!")


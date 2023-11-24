from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Body
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
import AuthGrocery
import Deals

app = FastAPI()

class Item(BaseModel):
    user: Optional[str] = None
    name: str
    woolworths_code: str
    coles_code: str
    iga_code: str
    image:str
    description:str
   

codes_storage: List[Item] = []



async def add_item(item: Item = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    item.user=current_user
    codes_storage.append(item)
    return {'message': f'Item {item.name} added by user {current_user}.'}

async def retrieve_all_item(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    user_items = [item for item in codes_storage if item.user == current_user]
    return user_items

async def remove_item(item: Item = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    try:
        # Find the index of the item in codes_storage based on Woolworths code
        index_to_remove = next((i for i, stored_item in enumerate(codes_storage) if stored_item.woolworths_code == item.woolworths_code), None)
        
        if index_to_remove is not None:
            # Check if the user matches the one who added the item
            if codes_storage[index_to_remove].user == current_user:
                # Remove the item
                removed_item = codes_storage.pop(index_to_remove)
                return {'message': f'Item {removed_item.name} removed successfully by user {current_user}.'}
            else:
                raise HTTPException(status_code=403, detail=f'User {current_user} does not have permission to remove this item.')
        else:
            # Check for a match based on Coles code
            index_to_remove = next((i for i, stored_item in enumerate(codes_storage) if stored_item.coles_code == item.coles_code), None)
            
            if index_to_remove is not None and codes_storage[index_to_remove].user == current_user:
                removed_item = codes_storage.pop(index_to_remove)
                return {'message': f'Item {removed_item.name} removed successfully by user {current_user}.'}
                
            # Check for a match based on IGA code
            index_to_remove = next((i for i, stored_item in enumerate(codes_storage) if stored_item.iga_code == item.iga_code), None)
            
            if index_to_remove is not None and codes_storage[index_to_remove].user == current_user:
                removed_item = codes_storage.pop(index_to_remove)
                return {'message': f'Item {removed_item.name} removed successfully by user {current_user}.'}
            
            # If no matches found, raise a 404 exception
            raise HTTPException(status_code=404, detail=f'Item not found for user {current_user}.')
    except ValueError:
        raise HTTPException(status_code=500, detail='Internal Server Error')

async def check_and_notify():
    products = []

    try:
        woolies_products = await Deals.half_price_deals_woolies()
        products.extend(woolies_products)
    except Exception as e:
        print(f"Error during Woolworths product retrieval: {e}")

    try:
        iga_products = await Deals.half_price_deals_iga()
        products.extend(iga_products)
    except Exception as e:
        print(f"Error during IGA product retrieval: {e}")

    try:
        coles_products = await Deals.half_price_deals_coles()
        products.extend(coles_products)
    except Exception as e:
        print(f"Error during Coles product retrieval: {e}")


    for stored_item in codes_storage:
        for product in products:
            # Convert stockcode to str for comparison
            product_code_str = str(product.stockcode)
            if (
                stored_item.woolworths_code == product_code_str
                or stored_item.coles_code == product_code_str
                or stored_item.iga_code == product_code_str
            ):
                send_notification(stored_item)

def send_notification(stored_item):
    print(f"Notification: Item {stored_item.name} matched")

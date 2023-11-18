from typing import List
import AuthGrocery
import Connect
import Deals
import Notification
import Cache
import PAI
from fastapi import FastAPI, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
app = FastAPI()

Connect.middleware(app)
@app.post("/register")
async def register(user: AuthGrocery.User):
 user_manager = AuthGrocery.UserManager()
 await user_manager.register_user(user)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    AuthGrocery.login_for_access_token(form_data)
@app.get("/protected")
async def protected(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
 return {"message": "This is a protected route", "user": current_user}
@app.post('/add_item_notify')
async def add_item(item: Notification.Item = Body(...),current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
 Notification.add_item(item,current_user)
@app.post('/remove_item_notify')
async def remove_item( item: Notification.Item = Body(...),current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
 Notification.remove_item(item,current_user)
@app.get("/run_notification")
async def check_and_notify():
 Notification.check_and_notify()
@app.get("/search/{query}/{code}", response_model=List[PAI.Product])
async def search(query: str,code:str):
 return await PAI.search_products(query,code)
@app.get("/half-price-deals_woolies", response_model=List[PAI.Product])
async def woolies():
 return await Deals.half_price_deals_woolies()
@app.get("/half-price-deals_iga", response_model=List[PAI.Product])
async def iga():
 return await Deals.half_price_deals_iga()
@app.get("/half-price-deals_coles", response_model=List[PAI.Product])
async def coles():
 return await Deals.half_price_deals_coles()
@app.get("/search_suggestions")
async def get_popular_searches(limit: int = 10):
 popular = sorted(Cache.CACHE.items(), key=lambda x: x[1]['count'], reverse=True)[:limit]
 return [{"query": item[0], "count": item[1]['count']} for item in popular]
if __name__ == "__main__":
 import uvicorn
 uvicorn.run(app, host="0.0.0.0", port=8000)

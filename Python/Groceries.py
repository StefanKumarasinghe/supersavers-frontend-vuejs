from fastapi import FastAPI, Depends, Body, Form, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from typing import List
import AuthGrocery
import Connect
import Deals
import Notification
import PAI
import Cart



limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add TrustedHostMiddleware for security headers
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

Connect.middleware(app)

# Routes for user management and authentication
@app.post("/register",  response_model=None)
@limiter.limit("10/60minute")
async def register(request: Request,user:  AuthGrocery.UserModel):
    user_manager = AuthGrocery.UserManager()
    return await user_manager.register_user(user)

@app.post("/login")
@limiter.limit("10/60minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user_manager = AuthGrocery.UserManager()
    return await user_manager.login_for_access_token(form_data)

@app.get("/protected")
async def protected(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    return {"message": "This is an authenticated route", "user": current_user}


# Routes for password recovery
@app.get("/verified")
async def verified(current_user: str = Depends(AuthGrocery.PasswordRecoveryManager.is_email_verified)):
    return {"message": "This user is verified", "user" : current_user }

@app.get("/verify-email")
async def verify_email_endpoint(token: str):
    return await AuthGrocery.PasswordRecoveryManager.verify_email(token)

@app.get("/resend-email")
async def resend(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    

    return await AuthGrocery.UserManager.resend_verification_email(current_user)
@app.post("/forgot-password")
@limiter.limit("5/60minute")
async def forgot_password(request: Request, email: str = Form(...)):
    user_manager = AuthGrocery.PasswordRecoveryManager()
    return await user_manager.request_password_reset(email)

@app.post("/reset-password")
async def reset_password(token: str = Form(...), password: str = Form(...)):
    user_manager = AuthGrocery.PasswordRecoveryManager()
    return await user_manager.reset_password(token, password)

# Routes for notification management
@app.post('/add_item_notify')
async def add_item(item: Notification.Item = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    return await Notification.add_item(item, current_user)

@app.post('/remove_item_notify')
async def remove_item(item: Notification.Item_Remove = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    return await Notification.remove_item(item, current_user)

@app.post('/retrieve_notify')
async def get_item(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    return await Notification.retrieve_all_item(current_user)

@app.get("/run_notification")
async def check_and_notify():
    return await Notification.check_and_notify()



@app.post('/retrieve_bought')
async def get_bought_items(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    try:
        bought_items = await Cart.get_cart_items_bought(current_user)
        return bought_items
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post('/retrieve_unbought')
async def get_unbought_items(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
        unbought_items = await Cart.get_cart_items_unbought(current_user)
        return unbought_items

@app.post('/retrieve_saving_user')
async def saving(current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
        saving = await Cart.saving(current_user)
        return saving


@app.post('/add_item_cart')
async def add_item_to_cart(item: Cart.ItemCart = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    try:
     response = await Cart.add_to_cart(item, current_user)
     return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post('/remove_cart')
async def remove_item_from_cart(item: Cart.ItemIdentity = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    try:
        response = await Cart.remove_from_cart(item, current_user)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post('/increase_cart_quantity')
async def increment(item: Cart.ItemIdentity = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    try:
        response = await Cart.increment(item, current_user)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post('/reduce_cart_quantity')
async def increment(item: Cart.ItemIdentity = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    try:
        response = await Cart.decrement(item, current_user)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@app.post('/update_cart')
async def update_cart_item(item: Cart.ItemIdentity = Body(...), current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    try:
        response = await Cart.change_bought(item, current_user)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")



# Routes for product search and deals
@app.get("/search/{query}/{code}", response_model=List[PAI.Product])
@limiter.limit("30/minute")
async def search(request: Request, query: str, code: str, current_user: dict = Depends(AuthGrocery.PasswordRecoveryManager.is_email_verified)):
    return await PAI.search_products(query, code)

@app.get("/half-price-deals_woolies", response_model=List[Deals.Product])
@limiter.limit("10/minute")
async def woolies(request: Request, current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    return await Deals.half_price_deals_woolies()

@app.get("/half-price-deals_iga", response_model=List[Deals.Product])
@limiter.limit("10/minute")
async def iga(request: Request, current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    return await Deals.half_price_deals_iga()

@app.get("/half-price-deals_coles", response_model=List[Deals.Product])
@limiter.limit("10/minute")
async def coles(request: Request, current_user: str = Depends(AuthGrocery.UserManager.get_current_user)):
    return await Deals.half_price_deals_coles()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

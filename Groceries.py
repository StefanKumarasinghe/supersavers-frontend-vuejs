from typing import List, Union , Optional
import httpx
import json
import spacy
import asyncio
import time
from passlib.context import CryptContext
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher

from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta  # Add this line for timedelta and datetime

from fuzzywuzzy import fuzz
from difflib import SequenceMatcher

from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor


from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# Define your User model
class User(BaseModel):
    username: str
    email: str
    hashed_password: str

# Your user database
users_db = []

# FastAPI app instance
app = FastAPI()

# Security configurations
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to verify token and get current user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

# User registration endpoint
@app.post("/register")
async def register_user(user: User):
    hashed_password = pwd_context.hash(user.hashed_password)
    user_data = {"username": user.username,"email": user.email, "hashed_password": hashed_password}
    users_db.append(user_data)

    # Generate access token for the registered user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"message": "User registered successfully", "access_token": access_token, "token_type": "bearer"}

# Login endpoint to generate access token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((x for x in users_db if x["username"] == form_data.username), None)
    if user is None or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route
@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}

codes_storage={} 

class Item(BaseModel):
    item: str
    woolworths_code: str
    coles_code: str
    iga_code: str

@app.post('/add_item_notify')
async def add_item(
    item: Item = Body(...),
    current_user: str = Depends(get_current_user)
):
    # Store the codes in memory along with the user information
    codes_storage.append({
        'user': current_user,
        'item': item.item,
        'woolworths_code': item.woolworths_code,
        'coles_code': item.coles_code,
        'iga_code': item.iga_code
    })
    return {'message': f'Item {item.item} removed added by user {current_user}.'}

@app.post('/remove_item_notify')
async def add_item(
    item: Item = Body(...),
    current_user: str = Depends(get_current_user)
):
    # Store the codes in memory along with the user information
    codes_storage.remove({
        'user': current_user,
        'item': item.item
    })
    return {'message': f'Item {item.item} removed successfully by user {current_user}.'}

@app.get("/run_notification")
async def check_and_notify():
    products=[]
    products.append(await half_price_deals())
    products.append(await half_price_deals_iga())
  

    for stored_item in codes_storage:
        for product in products:
            if (
                stored_item['woolworths_code'] == product.stockcode_w
                or stored_item['coles_code'] == product.stockcode_c
                or stored_item['iga_code'] == product.stockcode_i
            ):
                # Send a notification (you need to implement this part)
                send_notification(stored_item, product)

              
# Function to send a notification (you need to implement this part)
def send_notification(stored_item, matching_product):
    print(f"Notification: Item {stored_item['item']} matched with {matching_product.source} deal!")



# Define the in-memory cache and the maximum cache duration
CACHE = {}
product_database = {}
CACHE_DURATION = 3600  # seconds or 5 minutes




def is_cache_valid(query: str) -> bool:
    """Check if cache for a query is still valid."""
    return query in CACHE and time.time() - CACHE[query]['timestamp'] < CACHE_DURATION


WOOLWORTHS_COOKIES = None

origins = [
    "http://localhost:8081",
    "http://localhost:8080"
    # Add any other origins you want to allow here
]


nlp = spacy.load("en_core_web_md")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Woolworths_URL = "https://www.woolworths.com.au/apis/ui/Search/products"
Coles_URL = "https://www.coles.com.au/_next/data/20231115.01_v3.59.0/en/search.json?q={}"
CHEMIST_WAREHOUSE_URL = "https://pds.chemistwarehouse.com.au/suggest?identifier=AU&search={}"

IGA_URL = "https://www.igashop.com.au/api/storefront/stores/52511/search?misspelling=true&q={query}&take=5"



class Product(BaseModel):
    name: Optional[str] = "Default Name"
    stockcode_w: Optional[float] = None
    stockcode_i: Optional[float] = None
    stockcode_c: Optional[float] = None
    image: Optional[str] = "Default Image URL"
    woolworths_price: Union[float, None]
    coles_price: Union[float, None]
    aldi_price: Union[float, None] = None
    chemist_price: Union[float, None] = None  # Add this line
    iga_price: Union[float, None] = None  # Add this line
    source: str
    description: str
    size: Union[str, None]
    brand: Union[str, None]


    




PRICE_TOLERANCE = 0.20  # Define your price tolerance here



def update_product_database(w_product,coles_code=None,iga_code=None):
    barcode = w_product['Products'][0]["Stockcode"]
    if barcode:
        product_database[barcode] = {

            'name': w_product['Name'],
            'size': w_product['Products'][0].get("PackageSize", "N/A"),
            'brand':  w_product['Products'][0].get("Brand", "Woolworths"),
            'coles_code': coles_code,
            'iga_code': iga_code,
            'verified': False,
            'visibility':False
        }


def semantic_similarity(str1, str2):
    return fuzz.ratio(str1, str2)

def fuzzy_match(str1, str2):
    # Implement fuzzy string matching logic here
    return fuzz.token_sort_ratio(str1, str2) > 80

def is_similarwc(woolworths_product: dict, coles_product: dict) -> bool:
    try:
        brand1 = woolworths_product['Products'][0]['Brand']
        brand2 = coles_product.get('brand', '')

        woolworths_undiscounted_price = woolworths_product.get("Products", [{}])[0].get("WasPrice", 0)
        coles_was_price = coles_product.get('pricing', {}).get('was', 0)

        if coles_was_price == 0:
            coles_undiscounted_price = coles_product.get('pricing', {}).get('now', 0)
        else:
            coles_undiscounted_price = coles_was_price

        name1 = (woolworths_product.get('Name', '') + woolworths_product['Products'][0]['Description'])
        name2 = (coles_product.get('name', '') + coles_product.get('description', ''))
        similarity_score = semantic_similarity(name1, name2)

        if similarity_score < 0.70:
            return False
        
        woolworths_category = woolworths_product["Products"][0]["AdditionalAttributes"].get("sapsubcategoryname")
        coles_category = coles_product.get("merchandiseHeir", {}).get("category", None)

        # Check if both categories exist before comparing
        if woolworths_category is not None and coles_category is not None:
            similarity_score = semantic_similarity(woolworths_category, coles_category)

            # Adjust the threshold based on your preference
            if similarity_score < 0.30:
                return False
        else:
            # Handle the case where one or both categories are missing
            return False

        



        size_w = woolworths_product['Products'][0].get("PackageSize", "N/A").lower()
        size_c = coles_product.get('size', '').lower()

        if not (size_w in coles_product.get('name', '').lower() or size_w in coles_product.get('description', '').lower() or semantic_similarity(size_w, size_c)>0.95):
            if not (1 - PRICE_TOLERANCE) * woolworths_undiscounted_price <= coles_undiscounted_price <= (1 + PRICE_TOLERANCE) * woolworths_undiscounted_price:
                return False
        if brand1 and brand2:
         if not fuzzy_match(brand1, brand2):
            if (brand1.lower() not in {"woolworths", "coles"} ) or (brand2.lower() not in {"woolworths", "coles"}):
                return False
         

        
        similarity_score = semantic_similarity(size_w, size_c)
        if similarity_score < 0.90:
            return False
        else:
            if brand1 and brand2:
             if (brand1.lower() not in {"woolworths", "coles"} ) or (brand2.lower() not in {"woolworths", "coles"}):
              if not (1 - 0.01) * woolworths_undiscounted_price <= coles_undiscounted_price <= (1 + 0.01) * woolworths_undiscounted_price:
               return False
             else:
                if not (1 - 0.1) * woolworths_undiscounted_price <= coles_undiscounted_price <= (1 + 0.1) * woolworths_undiscounted_price:
                 return False
            else:
                if not (1 - 0.2) * woolworths_undiscounted_price <= coles_undiscounted_price <= (1 + 0.2) * woolworths_undiscounted_price:
                 return False


     

        return True

    except Exception as e:
        return False


def is_similarwi(woolworths_product: dict, iga_product: dict) -> bool:
    try:
        brand1 = woolworths_product['Products'][0]['Brand']
        brand2 = iga_product['brand']

        name1 = woolworths_product.get('Name', '')
        name2 = iga_product['name']

        woolworths_undiscounted_price = woolworths_product.get("Products", [{}])[0].get("WasPrice", 0)
        iga_price = iga_product['wasPrice']

        if not iga_price:
            iga_price = iga_product['price']

        similarity_score = semantic_similarity(name1, name2)

        if similarity_score < 0.75:
            return False

        if not (1 - PRICE_TOLERANCE) * woolworths_undiscounted_price <= iga_price <= (1 + PRICE_TOLERANCE) * woolworths_undiscounted_price:
            return False

        size_w = woolworths_product['Products'][0].get("PackageSize", "N/A")
        size_i = iga_product['size']

        if semantic_similarity(str(size_w), str(size_i)) < 0.75:
            return False

        if brand1.lower() != "woolworths" and brand1.lower() != "iga":
            if brand2.lower() != "woolworths" and brand2.lower() != "iga":
                if not fuzzy_match(brand1, brand2):
                    return False

        return True

    except Exception as e:
        print(e)
        return False



@app.get("/search/{query}/{code}", response_model=List[Product])
async def search_products(query: str,code:str):
    query = query.lower().strip()
    code = code.strip()
    #if is_cache_valid(query):
    #    return CACHE[query]['result']
    woolworths_headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.woolworths.com.au",
        "Referer": "https://www.woolworths.com.au/shop/search/products?searchTerm={query}&store_code=woolworths_supermarkets_{code}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cookie": ""
    }

    iga_headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 ..."
    }
    woolworths_response = None
    coles_response = None
    chemist_response = None

    iga_response = None



    woolworths_payload = {
        "EnableAdReRanking": False,
        "ExcludeSearchTypes": ["UntraceableVendors"],
        "Filters": [],
        "GpBoost": 0,
        "PageSize": 15,
        "GroupEdmVariants": True,
        "IsRegisteredRewardCardPromotion": None,
        "IsSpecial": False,
        "Location": f"/shop/search/products?searchTerm={query}",
        "SearchTerm": query,
        "SortType": "TraderRelevance"
    }
    
    async with httpx.AsyncClient(timeout=300,verify=False) as client:
        # Initial request to Woolworths homepage to get cookies
        global WOOLWORTHS_COOKIES
        if not WOOLWORTHS_COOKIES:
         response_homepage = await client.get('https://www.woolworths.com.au/')
         WOOLWORTHS_COOKIES = '; '.join([f"{name}={value}" for name, value in response_homepage.cookies.items()])
         
        woolworths_headers["Cookie"] = WOOLWORTHS_COOKIES
        
        

        results = await asyncio.gather(
            client.post(Woolworths_URL, headers=woolworths_headers, json=woolworths_payload),
            client.get(Coles_URL.format(query)),
            client.get(CHEMIST_WAREHOUSE_URL.format(query)),
            client.get(IGA_URL.format(query=query), headers=iga_headers)
        )
        woolworths_response, coles_response, chemist_response, iga_response = results
    
        
    if woolworths_response is None or woolworths_response.status_code != 200:
        raise HTTPException(status_code=woolworths_response.status_code if woolworths_response else 500, detail="Failed to fetch data from Woolworths")
    
    if coles_response.status_code != 200:
        raise HTTPException(status_code=coles_response.status_code, detail="Failed to fetch data from Coles")


    try:
        woolworths_products = woolworths_response.json()["Products"]
    except json.decoder.JSONDecodeError:
        woolworths_products = []

    try:
        coles_products = coles_response.json()["pageProps"]["searchResults"]["results"]
    except json.decoder.JSONDecodeError:
        coles_products = []
    try:
        data = chemist_response.json()
        chemist_products = [{
            'name': prod['name'],
            'price': prod['price'],
            'image': prod['_thumburl'],
            'brand': prod['brand']
        } for prod in data['suggestionGroups'][2]['suggestions']]
    except (IndexError, KeyError, ValueError):
        chemist_products = []

    try:
        iga_data = iga_response.json()
        iga_products = [{
            'id': item['barcode'],
            'name': item['name'],
            'wasPrice': float(item.get('wasPriceNumeric', 0)),  # Use get to handle missing key
            'price': float(item.get('priceNumeric', 0)),  # Use get to handle missing key
            'image': item['image']['default'],
            'brand': item['brand'],
            'size': item.get('unitOfSize', {}).get('size', 0),  # Use get to handle missing key
        } for item in iga_data['items']]
    except (json.decoder.JSONDecodeError, KeyError, ValueError):
        iga_products = []




    return merge_results(woolworths_products, coles_products, chemist_products, iga_products,query)


from itertools import combinations

def merge_results(woolworths: List[dict], coles: List[dict], chemist: List[dict], iga_products: List[dict], query :str) -> List[Product]:
    combined_products = []
    # Define a set to keep track of unique product names
    unique_product_names = set()


   
    for w_product in woolworths:
        barcode = w_product['Products'][0]["Stockcode"]
        # Check if the product is in the in-memory database
        if barcode in product_database:
            
            product_info = product_database[barcode]
            if (product_info['visibility']):
                continue
            
                
            # Check if the product name is already in the set
            if product_info['name'] not in unique_product_names:
                # Find the corresponding product in Coles using the stored code
                coles_price = None
        
                if product_info['coles_code']:
                
                    for c_product in coles:
                        
                       
                        if c_product.get('name') == product_info['coles_code']:
                            
                            coles_price = c_product.get('pricing', {}).get('now') if c_product.get('pricing') else None
                            break

                # Find the corresponding product in IGA using the stored code
                iga_price = None
                if product_info['iga_code']:
                    for i_product in iga_products:
                        if i_product['name'] == product_info['iga_code']:
                            iga_price = i_product['price']
                            break
              
                combined_products.append(Product(
                    name=product_info['name'],
                    woolworths_price=w_product['Products'][0]['Price'],
                    coles_price=coles_price,
                    chemist_price=None,
                    aldi_price=None,
                    iga_price=iga_price,
                    image=w_product['Products'][0]['LargeImageFile'],
                    source="Combined",
                    description=f"Available at Woolworths, Coles, and IGA",
                    size=product_info['size'],
                    brand=product_info['brand']
                ))
                
                # Add the product name to the set
    if  len(combined_products) > 3: 
     print('Fetched from ASX')    
     return combined_products

   
    for w_product in woolworths:
        for c_product in coles:
            for i_product in iga_products:
                if is_similarwc(w_product, c_product) and is_similarwi(w_product, i_product):
                    product_name = w_product['Name']

                    # Check if the product name is already in the set
                    if product_name not in unique_product_names:
                        # Combine products from Woolworths, Coles, and IGA
                        
                        woolworths_price = w_product['Products'][0]['Price']
                        coles_price = c_product.get('pricing', {}).get('now') if c_product.get('pricing') else None
                        iga_price = i_product['price']
                        product_image = w_product['Products'][0]['LargeImageFile']
                        size = w_product['Products'][0].get("PackageSize", "N/A")
                        brand = w_product['Products'][0].get("Brand", "Woolworths")
                        update_product_database(w_product,  c_product.get('name'),i_product['name'])
                       
                        combined_products.append(Product(
                            name=product_name,
                            woolworths_price=woolworths_price,
                            coles_price=coles_price,
                            chemist_price=None,
                            aldi_price=None,
                            iga_price=iga_price,
                            image=product_image,
                            source="Combined",
                            description="Available across Woolies, Coles, and IGA",
                            size=size,
                            brand=brand
                        ))

                        # Add the product name to the set
                        unique_product_names.add(product_name)
                    coles.remove(c_product)
                    break

                    
    
    for w_product in woolworths:
 
        for c_product in coles:
           
             
        
            if is_similarwc(w_product, c_product):
                product_name = w_product['Name']

                # Check if the product name is already in the set
                if product_name not in unique_product_names:
                    # Combine products from Woolworths and Coles
                    woolworths_price = w_product['Products'][0]['Price']
                    coles_price = c_product.get('pricing', {}).get('now') if c_product.get('pricing') else None
                    product_image = w_product['Products'][0]['LargeImageFile']
                    size = w_product['Products'][0].get("PackageSize", "N/A")
                    brand = w_product['Products'][0].get("Brand", "Woolworths")
                    update_product_database(w_product,  c_product.get('name'))
                    combined_products.append(Product(
                        name=product_name,
                        woolworths_price=woolworths_price,
                        coles_price=coles_price,
                        chemist_price=None,
                        aldi_price=None,
                        image=product_image,
                        source="Combined",
                        description="Available across Woolies and Coles",
                        size=size,
                        brand=brand
                    ))

                    # Add the product name to the set
                    unique_product_names.add(product_name)
                coles.remove(c_product)
                break


    for w_product in woolworths:
        for i_product in iga_products:
            if is_similarwi(w_product, i_product):
                product_name = w_product['Name']

                # Check if the product name is already in the set
                if product_name not in unique_product_names:
                    # Combine products from Woolworths and IGA
                    woolworths_price = w_product['Products'][0]['Price']
                    iga_price = i_product['price']
                    product_image = w_product['Products'][0]['LargeImageFile']
                    size = w_product['Products'][0].get("PackageSize", "N/A")
                    brand = w_product['Products'][0].get("Brand", "Woolworths")
                    update_product_database(w_product,i_product['name'])
                    combined_products.append(Product(
                        name=product_name,
                        woolworths_price=woolworths_price,
                        coles_price=None,
                        chemist_price=None,
                        aldi_price=None,
                        iga_price=iga_price,
                        image=product_image,
                        source="Combined",
                        description="Available across Woolies and IGA",
                        size=size,
                        brand=brand
                    ))

                    # Add the product name to the set
                    unique_product_names.add(product_name)
               
                break

      

    # Other combinations if needed
    # ...

    # Save the result to cache before returning
    if query in CACHE:
        CACHE[query]['count'] += 1
    else:
        CACHE[query] = {
            'result': combined_products,
            'timestamp': time.time(),
            'count': 1  # initialize count
        }

    
    return combined_products

@app.get("/half-price-deals_woolies", response_model=List[Product])
async def half_price_deals():
    woolworths_headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.woolworths.com.au",
        "Referer": "https://www.woolworths.com.au/shop/search/products?searchTerm={query}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cookie": ""
    }

    # Define the payload for half price deals
    woolworths_payload_half_price = {
        "categoryId": "specialsgroup.3676",
        "categoryVersion": "v2",
        "enableAdReRanking": False,
        "filters": [],
        "formatObject": "{\"name\":\"Half Price\"}",
        "gpBoost": 0,
        "groupEdmVariants": True,
        "isBundle": False,
        "isHideUnavailableProducts": False,
        "isMobile": True,
        "isRegisteredRewardCardPromotion": False,
        "isSpecial": True,
        "location": "/shop/browse/specials/half-price",
        "pageNumber": 1,
        "pageSize": 24,
        "sortType": "TraderRelevance",
        "token": "",
        "url": "/shop/browse/specials/half-price"
    }

    async with httpx.AsyncClient(timeout=300, verify=False) as client:
    # Access the global WOOLWORTHS_COOKIES
     global WOOLWORTHS_COOKIES
     if not WOOLWORTHS_COOKIES:
        response_homepage = await client.get('https://www.woolworths.com.au/')
        WOOLWORTHS_COOKIES = '; '.join([f"{name}={value}" for name, value in response_homepage.cookies.items()])
    
     woolworths_headers["Cookie"] = WOOLWORTHS_COOKIES
    
     woolworths_response = await client.post("https://www.woolworths.com.au/apis/ui/browse/category", headers=woolworths_headers, json=woolworths_payload_half_price)

    if woolworths_response.status_code != 200:
        raise HTTPException(status_code=woolworths_response.status_code, detail="Failed to fetch half-price deals from Woolworths")

    try:
        bundles = woolworths_response.json()["Bundles"]
        woolworths_products = [product for bundle in bundles for product in bundle["Products"]]
    except (json.decoder.JSONDecodeError, KeyError):
        woolworths_products = []

    # Process the woolworths_products
    woolworths_products = [Product(
        name=product.get('Name', ''),
        stockcode_w=product.get('Stockcode', ''),
        woolworths_price=product.get('Price', 0),
        coles_price=product.get('WasPrice', 0),  # Not applicable for this route
        chemist_price=None,  # Not applicable for this route
        aldi_price=None,  # Not applicable for this route
        iga_price=None,  # Not applicable for this route
        image=product.get('LargeImageFile', ''),
        source="Woolworths",
        description=product.get('Description', ''),
        size=product.get("PackageSize", "N/A"),
        brand=product.get("Brand", "Woolworths")
    ) for product in woolworths_products]
    
 


    # Combine Woolworths and IGA products
    combined_products = woolworths_products
 

    return combined_products


@app.get("/half-price-deals_iga", response_model=List[Product])
async def half_price_deals_iga():

    iga_headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Referer": "https://www.igashop.com.au/specials/13",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
 
    }

    iga_params = {
     "misspelling": True,
     "skip": 240,
     "sort": "",
     "take": 20
    }
 

    async with httpx.AsyncClient(timeout=300, verify=False) as client:
 
     iga_response = await client.get("https://www.igashop.com.au/api/storefront/stores/52511/promotions/products", headers=iga_headers, params=iga_params)

    if iga_response.status_code != 200:
        raise HTTPException(status_code=iga_response.status_code, detail="Failed to fetch promotions from igashop")

    iga_products = iga_response.json().get("items", [])

    # Convert the IGA products to the Product format
    iga_formatted_products = [Product(
        name=product.get('name', ''),
        stockcode_i=product.get('barcode', None),
        woolworths_price=None,  # Not applicable for this product
        
        coles_price=product.get('wasPriceNumeric', 0),  # Using this as a placeholder, but might not be right for your needs
        chemist_price=None,  # Not applicable for this route
        aldi_price=None,  # Not applicable for this route
        iga_price=product.get('priceNumeric', 0),
        image=product.get('image')['default'],  # IGA API response does not seem to provide image URLs in the example you shared
        source="IGA",
        description=product.get('description', ''),
        size=str(product.get("unitOfSize", {}).get("size", "N/A")) + product.get("unitOfSize", {}).get("abbreviation", ""),
        brand=product.get("brand", "IGA")
    ) for product in iga_products]

    # Combine Woolworths and IGA products
    combined_products = iga_formatted_products

    return combined_products



@app.get("/half-price-deals_coles", response_model=List[Product])
async def half_price_deals_coles():


 

    async with httpx.AsyncClient(timeout=300, verify=False) as client:
 
     coles_response = await client.get("https://www.coles.com.au/_next/data/20231115.01_v3.59.0/en/on-special.json")

    if coles_response.status_code != 200:
        raise HTTPException(status_code=coles_response.status_code, detail="Failed to fetch promotions from Coles shop")

    coles_products = coles_response.json()["pageProps"]["searchResults"]["results"]
 

    # Convert the IGA products to the Product format
    
    coles_formatted_products = [
        Product(
            name=product['name'],
            stockcode_i=product.get('id', None),
            woolworths_price=None,
            coles_price=product.get('pricing', {}).get('was') if product.get('pricing') is not None else None,
            chemist_price=None,
            aldi_price=None,
            iga_price=product.get('pricing', {}).get('now') if product.get('pricing') is not None else None,
            image=f"https://productimages.coles.com.au/productimages{product.get('imageUris', [{}])[0].get('uri', 'default_image_url')}",
            source="Coles",
            description=product.get('description', ''),
            size=str(product.get("size", "N/A")),
            brand=product.get("brand", "Coles")
        ) for product in coles_products if product.get('name') is not None
    ]



    # Combine Woolworths and IGA products
    combined_products = coles_formatted_products

    return combined_products




@app.get("/search_suggestions")
async def get_popular_searches(limit: int = 10):
    # Sort by count and take top 'limit' results
    popular = sorted(CACHE.items(), key=lambda x: x[1]['count'], reverse=True)[:limit]
    return [{"query": item[0], "count": item[1]['count']} for item in popular]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
 

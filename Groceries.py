from typing import List, Union , Optional
import httpx
import json
import difflib
import re
import spacy
import asyncio
import time

from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache

# Define the in-memory cache and the maximum cache duration
CACHE = {}
CACHE_DURATION = 3600  # seconds or 5 minutes

def is_cache_valid(query: str) -> bool:
    """Check if cache for a query is still valid."""
    return query in CACHE and time.time() - CACHE[query]['timestamp'] < CACHE_DURATION


WOOLWORTHS_COOKIES = None

origins = [
    "http://localhost",
    "http://localhost:8082",
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
    # Add any other origins you want to allow here
]

app = FastAPI()
nlp = spacy.load("en_core_web_md")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Woolworths_URL = "https://www.woolworths.com.au/apis/ui/Search/products"
Coles_URL = "https://www.coles.com.au/_next/data/20231027.01_v3.57.0/en/search.json?q={}"
CHEMIST_WAREHOUSE_URL = "https://pds.chemistwarehouse.com.au/suggest?identifier=AU&search={}"
ALDI_URL = "https://www.stockcheck.aldi.com.au/api/products"
IGA_URL = "https://www.igashop.com.au/api/storefront/stores/52511/search?misspelling=true&q={query}&take=20"



class Product(BaseModel):
    name: Optional[str] = "Default Name"
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


    


def semantic_similarity(str1: str, str2: str) -> float:
    """Compute semantic similarity between two strings using spaCy."""
    doc1 = nlp(str1)
    doc2 = nlp(str2)
    return doc1.similarity(doc2)


def fuzzy_match(str1: str, str2: str) -> bool:
    """Return True if strings are similar, else False."""
    if not str1 or not str2:  # Check if any string is empty or None
        return False
    return difflib.SequenceMatcher(None, str1, str2).ratio() > 0.8
PRICE_TOLERANCE = 0.2  # 20%

def is_similar(woolworths_product: dict, coles_product: dict) -> bool:
    try:
        brand1 = woolworths_product['Products'][0]['Brand']
        brand2 = coles_product.get('brand', '')
       
        

        # Get the undiscounted prices
        woolworths_undiscounted_price = woolworths_product.get("Products", [{}])[0].get("WasPrice", 0)
        coles_was_price = coles_product.get('pricing', {}).get('was', 0)
        # If coles_was_price is 0, then calculate it using 'now' and 'saveAmount'
        if coles_was_price == 0:
            coles_undiscounted_price = coles_product.get('pricing', {}).get('now', 0)
        else:
            coles_undiscounted_price = coles_was_price
   
        
        # Compute name and description similarity
        name1 = (woolworths_product.get('Name', '') + woolworths_product['Products'][0]['Description'] )

        name2 = (coles_product.get('name', '') + coles_product.get('description', '') )

        similarity_score = semantic_similarity(name1, name2)

        

        if similarity_score < 0.45:
            return False
        

        # Check if size of Woolworths is in the name or description of Coles. If it is, return True immediately.
        size_w = woolworths_product['Products'][0].get("PackageSize", "N/A").lower()
        
        if size_w in coles_product.get('name', '').lower() or size_w in coles_product.get('description', '').lower():
            
                # Check if the undiscounted prices of both products are similar within a tolerance
                if not (1 - PRICE_TOLERANCE) * woolworths_undiscounted_price <= coles_undiscounted_price <= (1 + PRICE_TOLERANCE) * woolworths_undiscounted_price:
                    return False

   
                return True

        # If name similarity check passed, then check size similarity
        if brand1.lower() != "woolworths" or brand1.lower() != "coles":
            if brand2.lower()!="woolworths" or brand2.lower()!="coles":
                if not (fuzzy_match(brand1,brand2)):
                    return False;
        size_c = coles_product.get('size', '').lower()
        similarity_score = semantic_similarity(size_w, size_c)
        if similarity_score < 0.70:
            return False
        # Check if the undiscounted prices of both products are similar within a tolerance
        if not (1 - PRICE_TOLERANCE) * woolworths_undiscounted_price <= coles_undiscounted_price <= (1 + PRICE_TOLERANCE) * woolworths_undiscounted_price:
            return False
        print(size_w+" : "+coles_product.get('name', '').lower())

    
         
        return True

    except Exception as e:
        return False



@app.get("/search/{query}/{code}", response_model=List[Product])
async def search_products(query: str,code:str):
    query = query.lower().strip()
    code = code.strip()
    if is_cache_valid(query):
        return CACHE[query]['result']
    print("Function is being executed!")
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
    aldi_payload = {
    "query": query,
    "state": "VIC",
    "lat": "-37.8112",
    "lng": "144.9646"
    }
    iga_headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 ..."
    }
    woolworths_response = None
    coles_response = None
    chemist_response = None
    aldi_response = None
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
            client.post(ALDI_URL, json=aldi_payload),
            client.get(IGA_URL.format(query=query), headers=iga_headers)
        )
        woolworths_response, coles_response, chemist_response, aldi_response, iga_response = results
    
        
    if woolworths_response is None or woolworths_response.status_code != 200:
        raise HTTPException(status_code=woolworths_response.status_code if woolworths_response else 500, detail="Failed to fetch data from Woolworths")
    
    if coles_response.status_code != 200:
        raise HTTPException(status_code=coles_response.status_code, detail="Failed to fetch data from Coles")
    if aldi_response.status_code != 200:
        raise HTTPException(status_code=aldi_response.status_code, detail="Failed to fetch data from ALDI")


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
        aldi_products_raw = aldi_response.json()
        aldi_products = [{
            'name': prod['product_name'],
            'price': prod['price_float'],
            'image': prod['image'],
            'brand': prod['product_category'],  # Not exactly the brand but the closest thing we have
        } for prod in aldi_products_raw]
    except (json.decoder.JSONDecodeError, KeyError, ValueError):
        aldi_products = []

    try:
        iga_data = iga_response.json()
        iga_products = [{
            'name': item['name'],
            'price': float(item['priceNumeric']),
            'image': item['image']['default'],
            'brand': item['brand'],
            'size': item.get('unitOfSize', {}).get('size', None)
        } for item in iga_data['items']]
    except (json.decoder.JSONDecodeError, KeyError, ValueError):
        iga_products = []



    return merge_results(woolworths_products, coles_products, chemist_products, aldi_products, iga_products,query)


def merge_results(woolworths: List[dict], coles: List[dict], chemist: List[dict], aldi_products: List[dict], iga_products: List[dict], query :str) -> List[Product]:
    combined_products = []
    exclusive_woolworths = []
    exclusive_coles = []
    exclusive_chemist = []
    exclusive_aldi = []
    exclusive_iga = []

    for a_product in aldi_products:
        exclusive_aldi.append(Product(
            name=a_product['name'],
            woolworths_price=None,
            coles_price=None,
            chemist_price=None,
            aldi_price=a_product['price'],
            image=a_product['image'],
            source="ALDI",
            description="Available only at ALDI.",
            size=None,
            brand=a_product['brand']
        ))

    for i_product in iga_products:
        exclusive_iga.append(Product(
            name=i_product['name'],
            woolworths_price=None,
            coles_price=None,
            chemist_price=None,
            aldi_price=None,
            iga_price=i_product['price'],
            image=i_product['image'],
            source="IGA",
            description="Available only at IGA.",
            size=None,
            brand=i_product['brand']
        ))

    for w_product in woolworths:
        w_matched = False
        for c_index, c_product in enumerate(coles):
            if is_similar(w_product, c_product):
                woolworths_price = w_product['Products'][0]['Price']
                coles_price=c_product.get('pricing', {}).get('now') if c_product.get('pricing') else None
                product_name = w_product['Name']
                product_image = w_product['Products'][0]['LargeImageFile']
                size = w_product['Products'][0].get("PackageSize", "N/A")
                brand = w_product['Products'][0].get("Brand", "Woolworths")

                combined_products.append(Product(
                    name=product_name,
                    woolworths_price=woolworths_price,
                    coles_price=coles_price,
                    chemist_price=None,
                    aldi_price=None,
                    image=product_image,
                    source="Combined",
                    description="Available across multiple stores.",
                    size=size,
                    brand=brand
                ))
                coles.pop(c_index)
                w_matched = True
                break

        if not w_matched:
            size = w_product['Products'][0].get("PackageSize", "N/A")
            brand = w_product['Products'][0].get("Brand", "Woolworths")
            exclusive_woolworths.append(Product(
                name=w_product['Name'],
                woolworths_price=w_product['Products'][0]['Price'],
                coles_price=None,
                image=w_product['Products'][0]['LargeImageFile'],
                source="Woolworths",
                description=f"Available only at Woolworths.",
                size=size,
                brand=brand
            ))
    
    for c_product in coles:
        
        if not any(p.coles_price and p.name == c_product.get('name') for p in combined_products):
            exclusive_coles.append(Product(
                name=c_product.get('name'),
                woolworths_price=None,
                coles_price=c_product.get('pricing', {}).get('now') if c_product.get('pricing') else None,
                image=str("https://productimages.coles.com.au/productimages/")+c_product.get("imageUris")[0]["uri"] if 'imageUris' in c_product else None,
                source="Coles",
                description="Available only at Coles.",
                size=c_product.get("size", "N/A"),
                brand=c_product.get("brand", "Coles")
            ))

    for ch_product in chemist:
        if not any(p.chemist_price and p.name == ch_product.get('name') for p in combined_products):
            exclusive_chemist.append(Product(
                name=ch_product.get('name'),
                woolworths_price=None,
                coles_price=None,
                chemist_price=ch_product.get('price'),
                image=ch_product.get('image'),
                source="Chemist Warehouse",
                description=f"Available only at Chemist Warehouse.",
                size=None,
                brand=ch_product.get('brand')
            ))

    while exclusive_woolworths or exclusive_coles or exclusive_chemist or exclusive_aldi or exclusive_iga:
        if exclusive_woolworths:
            combined_products.append(exclusive_woolworths.pop(0))
        if exclusive_coles:
            combined_products.append(exclusive_coles.pop(0))
        if exclusive_chemist:
            combined_products.append(exclusive_chemist.pop(0))
        if exclusive_aldi:
            combined_products.append(exclusive_aldi.pop(0))
        if exclusive_iga:
            combined_products.append(exclusive_iga.pop(0))
        # Save the result to cache before returning
          # After
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

@app.get("/search_suggestions")
async def get_popular_searches(limit: int = 10):
    # Sort by count and take top 'limit' results
    popular = sorted(CACHE.items(), key=lambda x: x[1]['count'], reverse=True)[:limit]
    return [{"query": item[0], "count": item[1]['count']} for item in popular]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

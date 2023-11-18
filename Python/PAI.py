from typing import List, Union , Optional
import httpx
import json
import time
import Cache
import Data
import spacy
import asyncio
from fastapi import HTTPException, Depends, Body
from pydantic import BaseModel
from typing import List, Optional
from fuzzywuzzy import fuzz
from pydantic import BaseModel

WOOLWORTHS_COOKIES = None
nlp = spacy.load("en_core_web_md")

Woolworths_URL = "https://www.woolworths.com.au/apis/ui/Search/products"
Coles_URL = "https://www.coles.com.au/_next/data/20231115.01_v3.59.0/en/search.json?q={query}"
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
product_database = {}


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




async def search_products(query: str,code:str):
    query = query.lower().strip()
    code = code.strip()
    #if is_cache_valid(query):
    #    return CACHE[query]['result']
    woolworths_headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://www.woolworths.com.au",
    "Referer": "https://www.woolworths.com.au/shop/search/products?searchTerm={query}",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Cookie": "",
 }

    iga_headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Referer": "https://www.igashop.com.au/specials/13",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
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
    "PageSize": 8,
    "GroupEdmVariants": True,
    "IsRegisteredRewardCardPromotion": None,
    "IsSpecial": False,
    "Location": f"/shop/search/products?searchTerm={query}",
    "SearchTerm": query,
    "SortType": "TraderRelevance",
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
            client.get(Coles_URL.format(query=query)),
            client.get(IGA_URL.format(query=query), headers=iga_headers)
        )
        woolworths_response, coles_response, iga_response = results
    
        
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




    return merge_results(woolworths_products, coles_products, iga_products,query)


from itertools import combinations

def merge_results(woolworths: List[dict], coles: List[dict], iga_products: List[dict], query :str) -> List[Product]:
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
    if query in Cache.CACHE:
        Cache.CACHE[query]['count'] += 1
    else:
        Cache.CACHE[query] = {
            'result': combined_products,
            'timestamp': time.time(),
            'count': 1  # initialize count
        }

    
    return combined_products
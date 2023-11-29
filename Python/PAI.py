from typing import List, Union , Optional
import httpx
import json
import FuncTools
import Data
import asyncio
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel

WOOLWORTHS_COOKIES = None
Woolworths_URL = "https://www.woolworths.com.au/apis/ui/Search/products"
Coles_URL = "https://www.coles.com.au/_next/data/{build}/en/search.json?q={query}"
IGA_URL = "https://www.igashop.com.au/api/storefront/stores/52511/search?misspelling=true&q={query}&take=5"

class Product(BaseModel):
    name: Optional[str] = "Could'nt fetch name..."
    stockcode_w: Optional[int] = None
    stockcode_i: Optional[int] = None
    stockcode_c: Optional[int] = None
    image: Optional[str] = "Default Image URL"
    woolworths_price: Union[float, None]
    coles_price: Union[float, None]
    iga_price: Union[float, None] = None
    source: str
    description: str
    size: Union[str, None]
    brand: Union[str, None]


async def search_products(query: str,code:str):
    query = query.lower().strip()
    code = code.strip()

    build = FuncTools.get_coles_build()





    woolworths_headers = {"Accept": "application/json, text/plain, */*","Content-Type": "application/json","Origin": "https://www.woolworths.com.au","Referer": "https://www.woolworths.com.au/shop/search/products?searchTerm={query}","User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-origin", "Cookie": "",}
    iga_headers = Data.headers_iga_deals
    woolworths_response = None
    coles_response = None
    iga_response = None
    woolworths_payload = {"EnableAdReRanking": False,"ExcludeSearchTypes": ["UntraceableVendors"],"Filters": [],"GpBoost": 0,"PageSize": 8,"GroupEdmVariants": True,"IsRegisteredRewardCardPromotion": None,"IsSpecial": False,"Location": f"/shop/search/products?searchTerm={query}","SearchTerm": query,"SortType": "TraderRelevance", }  
    async with httpx.AsyncClient(timeout=300,verify=False) as client:
        # Initial request to Woolworths homepage to get cookies
        global WOOLWORTHS_COOKIES
        if not WOOLWORTHS_COOKIES:
         response_homepage = await client.get('https://www.woolworths.com.au/')
         WOOLWORTHS_COOKIES = '; '.join([f"{name}={value}" for name, value in response_homepage.cookies.items()]) 

        woolworths_headers["Cookie"] = WOOLWORTHS_COOKIES
        results = await asyncio.gather(
            client.post(Woolworths_URL, headers=woolworths_headers, json=woolworths_payload),
            client.get(Coles_URL.format(query=query,build=build)),
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
            'id': item['sku'],
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
    unique_product_names = set()   
    for w_product in woolworths:
        for c_product in coles:
            for i_product in iga_products:
                if FuncTools.is_similarwc(w_product, c_product) and FuncTools.is_similarwi(w_product, i_product):
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
                        combined_products.append(Product(
                            stockcode_w=w_product['Products'][0]["Stockcode"],
                            stockcode_i=i_product['id'],
                            stockcode_c=c_product.get('id'),
                            name=product_name,
                            woolworths_price=woolworths_price,
                            coles_price=coles_price,
                            iga_price=iga_price,
                            image=product_image,
                            source="Combined",
                            description=w_product['Products'][0]["Description"],
                            size=size,
                            brand=brand
                        ))
                        unique_product_names.add(product_name)
                    coles.remove(c_product)
                    break

                    
    
    for w_product in woolworths:
        for c_product in coles:
            if FuncTools.is_similarwc(w_product, c_product):
                product_name = w_product['Name']
                # Check if the product name is already in the set
                if product_name not in unique_product_names:
                    # Combine products from Woolworths and Coles
                    woolworths_price = w_product['Products'][0]['Price']
                    coles_price = c_product.get('pricing', {}).get('now') if c_product.get('pricing') else None
                    product_image = w_product['Products'][0]['LargeImageFile']
                    size = w_product['Products'][0].get("PackageSize", "N/A")
                    brand = w_product['Products'][0].get("Brand", "Woolworths")  
                    combined_products.append(Product(
                        stockcode_w=w_product['Products'][0]["Stockcode"],
                        stockcode_c=c_product.get('id'),
                        name=product_name,
                        woolworths_price=woolworths_price,
                        coles_price=coles_price,
                        image=product_image,
                        source="Combined",
                        description=w_product['Products'][0]["Description"],
                        size=size,
                        brand=brand
                    ))
                    # Add the product name to the set
                    unique_product_names.add(product_name)
                coles.remove(c_product)
                break

    for w_product in woolworths:
        for i_product in iga_products:
            if FuncTools.is_similarwi(w_product, i_product):
                product_name = w_product['Name']
                # Check if the product name is already in the set
                if product_name not in unique_product_names:
                    # Combine products from Woolworths and IGA
                    woolworths_price = w_product['Products'][0]['Price']
                    iga_price = i_product['price']
                    product_image = w_product['Products'][0]['LargeImageFile']
                    size = w_product['Products'][0].get("PackageSize", "N/A")
                    brand = w_product['Products'][0].get("Brand", "Woolworths")
                    combined_products.append(Product(
                        stockcode_w=w_product['Products'][0]["Stockcode"],
                        stockcode_i=i_product['id'],
                        name=product_name,
                        woolworths_price=woolworths_price,
                        coles_price=None,
                        chemist_price=None,
                        aldi_price=None,
                        iga_price=iga_price,
                        image=product_image,
                        source="Combined",
                        description=w_product['Products'][0]["Description"],
                        size=size,
                        brand=brand
                    ))
                    # Add the product name to the set
                    unique_product_names.add(product_name)
                break
    return combined_products
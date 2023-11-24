
import httpx
import json
from typing import  Union , Optional
from pydantic import BaseModel

from fastapi import HTTPException
Woolies_Cookies = None  # Initialize as None at the module level

class Product(BaseModel):
    name: Optional[str] = "Default Name"
    stockcode: Optional[int] = None
    image: Optional[str] = "Default Image URL"
    new_price: Union[float, None]
    old_price: Union[float, None]
    source: str
    description: str
    size: Union[str, None]
    brand: Union[str, None]

async def half_price_deals_woolies():
    global Woolies_Cookies  # Declare Woolies_Cookies as global

    woolworths_headers =  woolworths_headers = {
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
    
    woolworths_payload_half_price = {
    "categoryId": "specialsgroup.3676",
    "categoryVersion": "v2",
    "enableAdReRanking": False,
    "filters": [],
    "formatObject": '{"name":"Half Price"}',
    "gpBoost": 0,
    "groupEdmVariants": True,
    "isBundle": False,
    "isHideUnavailableProducts": False,
    "isMobile": True,
    "isRegisteredRewardCardPromotion": False,
    "isSpecial": True,
    "location": "/shop/browse/specials/half-price",
    "pageNumber": 1,
    "pageSize": 8,
    "sortType": "TraderRelevance",
    "token": "",
    "url": "/shop/browse/specials/half-price",
}

    async with httpx.AsyncClient(timeout=300, verify=False) as client:
        # Access the global WOOLWORTHS_COOKIES
     if not Woolies_Cookies:
            response_homepage = await client.get('https://www.woolworths.com.au/')
            Woolies_Cookies = '; '.join([f"{name}={value}" for name, value in response_homepage.cookies.items()])
        
     woolworths_headers["Cookie"] = Woolies_Cookies

     woolworths_response = await client.post("https://www.woolworths.com.au/apis/ui/browse/category", headers=woolworths_headers, json=woolworths_payload_half_price)
    if woolworths_response.status_code != 200:
        raise HTTPException(status_code=woolworths_response.status_code, detail="Failed to fetch half-price deals from Woolworths")
    try:
        bundles = woolworths_response.json()["Bundles"]
        woolworths_products = [product for bundle in bundles for product in bundle["Products"]]
    except (json.decoder.JSONDecodeError, KeyError):
        woolworths_products = []
    woolworths_products = [Product(
        name=product.get('Name', ''),
        stockcode=product.get('Stockcode', ''),
        new_price=product.get('Price', 0),
        old_price=product.get('WasPrice', 0),  # Not applicable for this route
        image=product.get('LargeImageFile', ''),
        source="Woolworths",
        description=product.get('Description', ''),
        size=product.get("PackageSize", "N/A"),
        brand=product.get("Brand", "Woolworths")
    ) for product in woolworths_products]
    combined_products = woolworths_products
    return combined_products


async def half_price_deals_iga():

    iga_headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Referer": "https://www.igashop.com.au/specials/13",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}


    async with httpx.AsyncClient(timeout=300, verify=False) as client:
 
     iga_response = await client.get("https://www.igashop.com.au/api/storefront/stores/52511/promotions/products?misspelling=true&skip=240&sort=&take=20", headers=iga_headers)

    if iga_response.status_code != 200:
        raise HTTPException(status_code=iga_response.status_code, detail="Failed to fetch promotions from igashop")

    iga_products = iga_response.json().get("items", [])

    # Convert the IGA products to the Product format
    iga_formatted_products = [Product(
        name=product.get('name', ''),
        stockcode=product.get('barcode', None),
        old_price=product.get('wasPriceNumeric', 0),  # Using this as a placeholder, but might not be right for your needs
        new_price=product.get('priceNumeric', 0),
        image=product.get('image')['default'],  # IGA API response does not seem to provide image URLs in the example you shared
        source="IGA",
        description=product.get('description', ''),
        size=str(product.get("unitOfSize", {}).get("size", "N/A")) + product.get("unitOfSize", {}).get("abbreviation", ""),
        brand=product.get("brand", "IGA")
    ) for product in iga_products]
    combined_products = iga_formatted_products
    return combined_products
async def half_price_deals_coles():
    async with httpx.AsyncClient(timeout=300, verify=False) as client:
     coles_response = await client.get("https://www.coles.com.au/_next/data/20231117.02_v3.60.0/en/on-special.json")
    if coles_response.status_code != 200:
        raise HTTPException(status_code=coles_response.status_code, detail="Failed to fetch promotions from Coles shop")
    coles_products = coles_response.json()["pageProps"]["searchResults"]["results"]
    coles_formatted_products = [Product(
            name=product['name'],
            stockcode=product.get('id', None),
            old_price=product.get('pricing', {}).get('was') if product.get('pricing') is not None else None,
            new_price=product.get('pricing', {}).get('now') if product.get('pricing') is not None else None,
            image=f"https://productimages.coles.com.au/productimages{product.get('imageUris', [{}])[0].get('uri', 'default_image_url')}",
            source="Coles",
            description=product.get('description', ''),
            size=str(product.get("size", "N/A")),
            brand=product.get("brand", "Coles")
        ) for product in coles_products if product.get('name') is not None]
    combined_products = coles_formatted_products
    return combined_products

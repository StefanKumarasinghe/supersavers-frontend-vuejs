from typing import List, Union
import httpx
import json
import difflib
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
    # Add any other origins you want to allow here
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Woolworths_URL = "https://www.woolworths.com.au/apis/ui/Search/products"
Coles_URL = "https://www.coles.com.au/_next/data/20231016.01_v3.55.0/en/search.json?q={}"

class Product(BaseModel):
    name: str
    woolworths_price: Union[float, None]
    coles_price: Union[float, None]
    image: str
    source: str
    description: str
    size: Union[str, None]
    brand: Union[str, None]
    


def extract_size(product_name: str) -> str:
    sizes = re.findall(r'(\d+\.*\d*\s*[mlMLL]{1,2})', product_name)
    return sizes[0] if sizes else None
def is_similar(woolworths_product: dict, coles_product: dict) -> bool:
    name1 = woolworths_product['Name'].lower() if 'Name' in woolworths_product else ""
    name2 = coles_product['name'].lower() if 'name' in coles_product else ""
    
    size1 = extract_size(woolworths_product.get("Products", [{}])[0].get("PackageSize", ""))
    size2 = extract_size(coles_product.get("size", ""))

    if size1 and size2 and size1 != size2:
        return False

    # Compare brands
    brand1 = woolworths_product.get("Products", [{}])[0].get("Brand", None)
    brand1 = brand1.lower() if brand1 else ""  # Ensure the value is not None before calling .lower()

    brand2 = coles_product.get("brand", "").lower()

    if brand1 and brand2 and brand1 != brand2:
        return False

    similarity_ratio = difflib.SequenceMatcher(None, name1, name2).ratio()
    return similarity_ratio > 0.75  # Refining the similarity ratio to a bit higher threshold

@app.get("/search/{query}", response_model=List[Product])
async def search_products(query: str):
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


    woolworths_payload = {
        "EnableAdReRanking": False,
        "ExcludeSearchTypes": ["UntraceableVendors"],
        "Filters": [],
        "GpBoost": 0,
        "PageSize": 24,
        "GroupEdmVariants": True,
        "IsRegisteredRewardCardPromotion": None,
        "IsSpecial": False,
        "Location": f"/shop/search/products?searchTerm={query}",
        "SearchTerm": query,
        "SortType": "TraderRelevance"
    }

    async with httpx.AsyncClient(timeout=300,verify=False) as client:
        # Initial request to Woolworths homepage to get cookies
        response_homepage = await client.get('https://www.woolworths.com.au/')
        cookies_from_homepage = '; '.join([f"{name}={value}" for name, value in response_homepage.cookies.items()])
        woolworths_headers["Cookie"] = cookies_from_homepage

        # Proceed with original requests
        woolworths_response = await client.post(Woolworths_URL, headers=woolworths_headers, json=woolworths_payload)
        coles_response = await client.get(Coles_URL.format(query))
        
    if woolworths_response.status_code != 200:
        raise HTTPException(status_code=woolworths_response.status_code, detail="Failed to fetch data from Woolworths")
    
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

    print(woolworths_products)

    return merge_results(woolworths_products, coles_products)
def merge_results(woolworths: List[dict], coles: List[dict]) -> List[Product]:
    combined_products = []
    exclusive_woolworths = []
    exclusive_coles = []
    matched_indexes_coles = []
    matched_indexes_woolworths = []

    for w_idx, w_product in enumerate(woolworths):
        matched = False
        for c_idx, c_product in enumerate(coles):
            if is_similar(w_product, c_product) and c_idx not in matched_indexes_coles:
                
                woolworths_price = w_product['Products'][0]['Price']
                coles_price = c_product.get('pricing', {}).get('now', None)
                product_name = w_product['Name']
                product_image = w_product['Products'][0]['LargeImageFile']
                product_source = "Combined"
                size = w_product['Products'][0].get("PackageSize", "N/A")
                brand = w_product['Products'][0].get("Brand", "Woolworths")

                if coles_price:
                    savings = woolworths_price - coles_price
                    if savings > 0:
                        description = f"Cheaper at Coles by ${savings:.2f}."
                    elif savings < 0:
                        description = f"Cheaper at Woolworths by ${-savings:.2f}."
                    else:
                        description = "Same price at both."
                else:
                    description = f"Available only at Woolworths."

                combined_products.append(Product(
                    name=product_name,
                    woolworths_price=woolworths_price,
                    coles_price=coles_price,
                    image=product_image,
                    source=product_source,
                    description=description,
                    size=size,
                    brand=brand
                ))

                matched_indexes_coles.append(c_idx)
                matched_indexes_woolworths.append(w_idx)
                matched = True
                break

        if not matched:
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

    base_url = "https://productimages.coles.com.au/productimages/"
    for idx, c_product in enumerate(coles):
        if idx not in matched_indexes_coles and 'name' in c_product and 'imageUris' in c_product:
            name = c_product['name']
            coles_price = c_product.get('pricing', {}).get('now', None)
            image_uri = c_product["imageUris"][0]["uri"]
            image_url = f"{base_url}{image_uri}"
            size = c_product.get("size", "N/A")
            brand = c_product.get("brand", "Coles")
            exclusive_coles.append(Product(
                name=name,
                woolworths_price=None,
                coles_price=coles_price,
                image=image_url,
                source="Coles",
                description="Available only at Coles.",
                size=size,
                brand=brand
            ))

    # Interleave exclusive products from Woolworths and Coles
    while exclusive_woolworths or exclusive_coles:
        if exclusive_coles:
            combined_products.append(exclusive_coles.pop(0))
        if exclusive_woolworths:
            combined_products.append(exclusive_woolworths.pop(0))

    return combined_products


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

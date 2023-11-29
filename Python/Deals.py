import httpx
import json
from typing import Union, Optional
from pydantic import BaseModel
from fastapi import HTTPException
import Data
import FuncTools

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

async def handle_http_error(response, message):
    response.raise_for_status()
    try:
        return response.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"{message}. Unable to parse JSON response.")

async def half_price_deals_woolies():
    global Woolies_Cookies  # Declare Woolies_Cookies as global
    woolworths_headers = Data.header_woolworths_deals
    woolworths_payload_half_price = Data.payload_woolworths_deals

    try:
        async with httpx.AsyncClient(timeout=300, verify=False) as client:
            # Access the global WOOLWORTHS_COOKIES
            if not Woolies_Cookies:
                response_homepage = await client.get('https://www.woolworths.com.au/')
                Woolies_Cookies = '; '.join([f"{name}={value}" for name, value in response_homepage.cookies.items()])
            woolworths_headers["Cookie"] = Woolies_Cookies
            woolworths_response = await client.post("https://www.woolworths.com.au/apis/ui/browse/category", headers=woolworths_headers, json=woolworths_payload_half_price)

        response_data = await handle_http_error(woolworths_response, "Failed to fetch half-price deals from Woolworths")

        bundles = response_data.get("Bundles", [])
        woolworths_products = [product for bundle in bundles for product in bundle["Products"]]

        woolworths_products = [
            Product(
                name=product.get('Name', ''),
                stockcode=product.get('Stockcode', ''),
                new_price=product.get('Price', 0),
                old_price=product.get('WasPrice', 0),
                image=product.get('LargeImageFile', ''),
                source="Woolworths",
                description=product.get('Description', ''),
                size=product.get("PackageSize", "N/A"),
                brand=product.get("Brand", "Woolworths")
            ) for product in woolworths_products if product.get('Price', 0) != product.get('WasPrice', 0) and product.get('IsInStock')
        ]

        combined_products = woolworths_products
        return combined_products

    except (httpx.HTTPStatusError, json.JSONDecodeError, KeyError) as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Woolies deals: {str(e)}")

async def half_price_deals_iga():
    iga_headers = Data.headers_iga_deals
    
    try:
        async with httpx.AsyncClient(timeout=300, verify=False) as client:
            iga_response = await client.get("https://www.igashop.com.au/api/storefront/stores/52511/promotions/products?misspelling=true&skip=0&sort=&take=20", headers=iga_headers)
    
        response_data = await handle_http_error(iga_response, "Failed to fetch promotions from igashop")
    
        iga_products = response_data.get("items", [])
    
        # Convert the IGA products to the Product format
        iga_formatted_products = [Product(
            name=product.get('name', ''),
            stockcode=product.get('barcode', None),
            old_price=product.get('wasPriceNumeric', 0),
            new_price=product.get('priceNumeric', 0),
            image=product.get('image')['default'],
            source="IGA",
            description=product.get('description', 'This item does not have a description...'),
            size=str(product.get("unitOfSize", {}).get("size", "N/A")) + product.get("unitOfSize", {}).get("abbreviation", ""),
            brand=product.get("brand", "IGA")
        ) for product in iga_products]
        
        combined_products = iga_formatted_products
        return combined_products
    
    except (httpx.HTTPStatusError, json.JSONDecodeError, KeyError) as e:
        raise HTTPException(status_code=500, detail=f"Error fetching IGA promotions: {str(e)}")

async def half_price_deals_coles():
    try:
        # Assuming get_coles_build is an async function
        build = FuncTools.get_coles_build()

        async with httpx.AsyncClient(timeout=300, verify=False) as client:
            coles_response = await client.get(f"https://www.coles.com.au/_next/data/{build}/en/on-special.json?filter_Special=halfprice&page=1")

        response_data = await handle_http_error(coles_response, "Failed to fetch promotions from Coles shop")

        coles_products = response_data["pageProps"]["searchResults"]["results"]

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

    except (httpx.HTTPStatusError, json.JSONDecodeError, KeyError) as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Coles promotions: {str(e)}")

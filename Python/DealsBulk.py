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


async def handle_http_error(response, message):
    response.raise_for_status()
    try:
        return response.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"{message}. Unable to parse JSON response.")

async def half_price_deals_woolies_bulk():
    global Woolies_Cookies

    woolworths_headers = Data.header_woolworths_deals
    woolworths_payload_half_price = {
        "categoryId": "specialsgroup.3676",
        "categoryVersion": "v2",
        "enableAdReRanking": False,
        "filters": [{"Key": "SoldBy", "Items": [{"Term": "Woolworths"}]}],
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
        "pageSize": 24,
        "sortType": "TraderRelevance",
        "token": "",
        "url": "/shop/browse/specials/half-price",
    }

    combined_products = []

    try:
        async with httpx.AsyncClient(timeout=300, verify=False) as client:
            while True:
                if not Woolies_Cookies:
                    response_homepage = await client.get('https://www.woolworths.com.au/')
                    Woolies_Cookies = '; '.join([f"{name}={value}" for name, value in response_homepage.cookies.items()])
                woolworths_headers["Cookie"] = Woolies_Cookies
                woolworths_response = await client.post("https://www.woolworths.com.au/apis/ui/browse/category", headers=woolworths_headers, json=woolworths_payload_half_price)

                response_data = await handle_http_error(woolworths_response, "Failed to fetch half-price deals from Woolworths")

                bundles = response_data.get("Bundles", [])
                woolworths_products = [product for bundle in bundles for product in bundle["Products"]]

                if not woolworths_products:
                    break  # Break the loop if no more products are returned

                products = [Product(
                    name=product.get('Name', ''),
                    stockcode=product.get('Stockcode', ''),
                ) for product in woolworths_products if product.get('IsInStock')]

                combined_products.extend(products)

 

                # Increment pageNumber for the next request
                woolworths_payload_half_price["pageNumber"] += 1

        
       

    except (httpx.HTTPStatusError, json.JSONDecodeError, KeyError) as e:
      print(f"Error fetching Woolies deals: {str(e)}")
 

    return combined_products

async def half_price_deals_iga_bulk():
    iga_headers = Data.headers_iga_deals
    skip = 0
    take = 20  # You can adjust this based on your requirements
    combined_products = []
    try:
        async with httpx.AsyncClient(timeout=300, verify=False) as client:
            while True:
                iga_response = await client.get(
                    f"https://www.igashop.com.au/api/storefront/stores/52511/promotions/products?misspelling=true&skip={skip}&sort=&take={take}",
                    headers=iga_headers
                )

                response_data = await handle_http_error(iga_response, "Failed to fetch promotions from igashop")

                iga_products = response_data.get("items", [])

                # Break the loop if no more products are returned
                if not iga_products:
                    break

                # Convert the IGA products to the Product format
                iga_formatted_products = [Product(
                    name=product.get('name', ''),
                    stockcode=product.get('sku', None),
                ) for product in iga_products]

                # Increment skip for the next iteration
                skip += take
                combined_products.extend(iga_formatted_products)

                         

    except (httpx.HTTPStatusError, json.JSONDecodeError, KeyError) as e:
        return combined_products   


async def half_price_deals_coles_bulk():

    try:
        combined_products = []
        page = 1
        build = FuncTools.get_coles_build()

        while True:
            async with httpx.AsyncClient(timeout=300, verify=False) as client:
                coles_response = await client.get(f"https://www.coles.com.au/_next/data/{build}/en/on-special.json?filter_Special=halfprice&page={page}")

            response_data = await handle_http_error(coles_response, "Failed to fetch promotions from Coles shop")

            coles_products = response_data["pageProps"]["searchResults"]["results"]

            if not coles_products:
                break  # No more products found

            coles_formatted_products = [Product(
                name=product['name'],
                stockcode=product.get('id', None),
            ) for product in coles_products if product.get('name') is not None]

            combined_products.extend(coles_formatted_products)
            page += 1

       

    except (httpx.HTTPStatusError, json.JSONDecodeError, KeyError) as e:
        print('Finished coles retrieval')
    
    return combined_products
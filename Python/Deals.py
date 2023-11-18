
import httpx
import PAI
import json
import Data

from fastapi import HTTPException
WOOLWORTHS_COOKIES = None

async def half_price_deals_woolies():
    woolworths_headers = Data.woolworths_headers 
    woolworths_payload_half_price = Data.woolworths_payload_half_price
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
    woolworths_products = [PAI.Product(
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
    combined_products = woolworths_products
    return combined_products


async def half_price_deals_iga():

    iga_headers = Data.iga_headers
    iga_params = Data.iga_params

    async with httpx.AsyncClient(timeout=300, verify=False) as client:
 
     iga_response = await client.get("https://www.igashop.com.au/api/storefront/stores/52511/promotions/products", headers=iga_headers, params=iga_params)

    if iga_response.status_code != 200:
        raise HTTPException(status_code=iga_response.status_code, detail="Failed to fetch promotions from igashop")

    iga_products = iga_response.json().get("items", [])

    # Convert the IGA products to the Product format
    iga_formatted_products = [PAI.Product(
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
    combined_products = iga_formatted_products
    return combined_products
async def half_price_deals_coles():
    async with httpx.AsyncClient(timeout=300, verify=False) as client:
     coles_response = await client.get("https://www.coles.com.au/_next/data/20231115.01_v3.59.0/en/on-special.json")
    if coles_response.status_code != 200:
        raise HTTPException(status_code=coles_response.status_code, detail="Failed to fetch promotions from Coles shop")
    coles_products = coles_response.json()["pageProps"]["searchResults"]["results"]
    coles_formatted_products = [PAI.Product(
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
        ) for product in coles_products if product.get('name') is not None]
    combined_products = coles_formatted_products
    return combined_products
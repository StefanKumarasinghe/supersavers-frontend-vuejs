
from fuzzywuzzy import fuzz
import requests
import re

def get_coles_build():

    url = 'https://www.coles.com.au/'

    try:
        # Fetch the HTML content of the website
        response = requests.get(url)
        response.raise_for_status()

        # Search for the buildId pattern in the raw HTML using regular expression
        build_id_pattern = re.compile(r'buildId":"([^"]+)"')
        match = build_id_pattern.search(response.text)

        if match:
            # Extract the Build ID from the regular expression match
            build_id = match.group(1)
            return build_id 
            
        else:
            print('Build ID not found in the raw HTML.')
            return ""
            
    except requests.RequestException as e:
        print(f'Error fetching the website: {e}')
    except Exception as e:
        print(f'Error: {e}')


PRICE_TOLERANCE = 0.20

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
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

origins = [
    "http://localhost:8081",
    "http://localhost:8080",
]
Woolworths_URL = "https://www.woolworths.com.au/apis/ui/Search/products"
Coles_URL = "https://www.coles.com.au/_next/data/20231115.01_v3.59.0/en/search.json?q={}"
CHEMIST_WAREHOUSE_URL = "https://pds.chemistwarehouse.com.au/suggest?identifier=AU&search={}"
IGA_URL = "https://www.igashop.com.au/api/storefront/stores/52511/search?misspelling=true&q={query}&take=5"


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
 
 

origins = [
    "http://localhost:8081",
    "http://localhost:8082",
    "http://localhost:8080",
]

payload_woolworths_deals = {
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

header_woolworths_deals = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.woolworths.com.au",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cookie": "",
    }

headers_iga_deals = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Referer": "https://www.igashop.com.au/specials/13",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }
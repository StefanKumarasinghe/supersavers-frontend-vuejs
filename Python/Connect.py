from fastapi.middleware.cors import CORSMiddleware
import httpx
import Data

WOOLWORTHS_COOKIES = None
def middleware(app):
    app.add_middleware(
    CORSMiddleware,
    allow_origins=Data.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
async def Initialise():
 async with httpx.AsyncClient(timeout=300, verify=False) as client:
    woolworths_headers = Data.woolworths_headers
    global WOOLWORTHS_COOKIES
    if not WOOLWORTHS_COOKIES:
        response_homepage = await client.get('https://www.woolworths.com.au/')
        WOOLWORTHS_COOKIES = '; '.join([f"{name}={value}" for name, value in response_homepage.cookies.items()])
    woolworths_headers["Cookie"] = WOOLWORTHS_COOKIES
from fastapi import FastAPI, HTTPException, Request
import httpx
import json
import logging

# Initialize the FastAPI application
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Replace with your actual credentials
CLIENT_ID = "cid.5sz7j79l90xsz9umlgfws6q2j"
CLIENT_SECRET = "cs2.nsfud9zksebzrn8afvd9b3bmn05n9sdxh1hok7y3iqmpiryzg9"
TENANT_ID = "1561207974"
APP_KEY = "ak1.p1hyw417u4rd7c19faytek0t2"

# URLs
TOKEN_URL = "https://auth.servicetitan.io/connect/token"
CUSTOMER_URL = f"https://api.servicetitan.io/crm/v2/tenant/{TENANT_ID}/customers"


async def get_access_token() -> str:
    logger.debug("Attempting to retrieve access token.")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        logger.debug(f"Token response status code: {response.status_code}")
        if response.status_code == 200:
            token_response = response.json()
            access_token = token_response.get("access_token")
            logger.debug(f"Access token retrieved: {access_token}")
            return access_token
        else:
            logger.error(f"Failed to retrieve access token. Status code: {response.status_code}")
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to retrieve access token.",
            )


async def create_customer(access_token: str, customer_data: dict) -> dict:
    logger.debug("Attempting to create customer with data: %s", customer_data)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            CUSTOMER_URL,
            headers=headers,
            json=customer_data,  # Use json= instead of data= to automatically handle JSON encoding
        )
        logger.debug(f"Customer creation response status code: {response.status_code}")
        if response.status_code == 200:
            customer_response = response.json()
            logger.debug(f"Customer created successfully: {customer_response}")
            return customer_response
        else:
            logger.error(f"Failed to create customer. Status code: {response.status_code}, Response: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to create customer.",
            )


@app.post("/create_customer/")
async def api_create_customer(request: Request):
    logger.debug("Received request to create customer.")

    # Log raw body to diagnose if the body is sent correctly
    try:
        customer_data = await request.json()  # Properly parse the JSON body
        logger.debug(f"Request body: {customer_data}")
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    # Ensure the 'address' field is included
    if 'locations' not in customer_data or not any(location.get('address') for location in customer_data['locations']):
        logger.error("Missing 'address' field in the locations data.")
        raise HTTPException(status_code=400, detail="Address field is required in locations.")

    access_token = await get_access_token()
    if access_token:
        customer_response = await create_customer(access_token, customer_data)
        return customer_response
    else:
        logger.error("Access token is required but was not obtained.")
        raise HTTPException(status_code=500, detail="Access token is required.")

from fastapi import FastAPI, HTTPException
import httpx
import logging

# Initialize the FastAPI application
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Replace with your actual credentials
CLIENT_ID = "cid.5sz7j79l90xsz9umlgfws6q2j"
CLIENT_SECRET = "cs2.nsfud9zksebzrn8afvd9b3bmn05n9sdxh1hok7y3iqmpiryzg9"
TENANT_ID = "1561207974"  # Your tenant ID
APP_KEY = "ak1.p1hyw417u4rd7c19faytek0t2"

# URLs - Adjusted for production ServiceTitan API
TOKEN_URL = "https://auth.servicetitan.io/connect/token"
CUSTOMER_LIST_URL = f"https://api.servicetitan.io/crm/v2/tenant/{TENANT_ID}/customers"

async def get_access_token() -> str:
    """
    Obtains an access token using OAuth 2.0 client credentials.
    """
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
            logger.error(f"Failed to retrieve access token. Status code: {response.status_code}, Response: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to retrieve access token: {response.text}"
            )

async def get_customers_list(access_token: str, phone: str) -> dict:
    """
    Calls the ServiceTitan Customers_GetList API to retrieve customers filtered by phone number.
    """
    logger.debug(f"Attempting to fetch customer list with phone: {phone}")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ST-App-Key": APP_KEY,
    }
    params = {"phone": phone}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            CUSTOMER_LIST_URL,
            headers=headers,
            params=params,
        )
        logger.debug(f"Customer list response status code: {response.status_code}")
        if response.status_code == 200:
            customer_list_response = response.json()
            logger.debug(f"Customer list retrieved successfully: {customer_list_response}")
            return customer_list_response
        else:
            logger.error(
                f"Failed to fetch customer list. Status code: {response.status_code}, Response: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to fetch customer list: {response.text}"
            )

@app.get("/get_customers/")
async def api_get_customers(phone: str):
    """
    FastAPI GET endpoint to get a list of customers filtered by phone number.
    Expects a 'phone' query parameter.
    """
    logger.debug(f"Received request to get customer list with phone: {phone}")

    if not phone:
        logger.error("Missing 'phone' query parameter.")
        raise HTTPException(status_code=400, detail="Phone query parameter is required.")

    access_token = await get_access_token()
    if access_token:
        customer_list_response = await get_customers_list(access_token, phone)
        return customer_list_response
    else:
        logger.error("Access token is required but was not obtained.")
        raise HTTPException(status_code=500, detail="Access token is required.")

# Run the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
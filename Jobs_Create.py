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
            json=customer_data,
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
                detail=f"Failed to create customer: {response.text}",
            )


async def create_job(access_token: str, job_data: dict) -> dict:
    logger.debug("Attempting to create job with data: %s", job_data)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs",
            headers=headers,
            json=job_data,
        )
        logger.debug(f"Job creation response status code: {response.status_code}")
        if response.status_code == 200:
            job_response = response.json()
            logger.debug(f"Job created successfully: {job_response}")
            return job_response
        else:
            logger.error(f"Failed to create job. Status code: {response.status_code}, Response: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to create job: {response.text}",
            )


@app.post("/create_customer/")
async def api_create_customer(request: Request):
    logger.debug("Received request to create customer.")

    try:
        customer_data = await request.json()
        logger.debug(f"Request body: {customer_data}")
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    # Ensure the 'locations' field is included and has address
    if 'locations' not in customer_data or not customer_data['locations']:
        logger.error("Missing 'locations' field in the customer data.")
        raise HTTPException(status_code=400, detail="Locations field is required.")

    # Make sure we have the root-level address field (required by API)
    if 'address' not in customer_data:
        # If not provided explicitly, use the first location's address as the billing address
        if customer_data['locations'][0].get('address'):
            customer_data['address'] = customer_data['locations'][0]['address']
        else:
            logger.error("Missing 'address' field in both customer data and locations.")
            raise HTTPException(status_code=400, detail="Address field is required.")

    # Add the required 'request' field if it doesn't exist
    # This appears to be required by the ServiceTitan API based on the error
    if 'request' not in customer_data:
        customer_data['request'] = {}

    access_token = await get_access_token()
    if access_token:
        customer_response = await create_customer(access_token, customer_data)
        return customer_response
    else:
        logger.error("Access token is required but was not obtained.")
        raise HTTPException(status_code=500, detail="Access token is required.")


@app.post("/create_job/")
async def api_create_job(request: Request):
    logger.debug("Received request to create job.")

    try:
        job_data = await request.json()
        logger.debug(f"Request body: {job_data}")
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    # Ensure required fields are present
    required_fields = ["customerId", "locationId", "businessUnitId", "jobTypeId", "priority", "campaignId", "appointments"]
    for field in required_fields:
        if field not in job_data:
            logger.error(f"Missing required field: {field}")
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    # Ensure appointments have required fields
    for appointment in job_data.get("appointments", []):
        if "start" not in appointment or "end" not in appointment:
            logger.error("Appointment missing required fields: 'start' and 'end'")
            raise HTTPException(status_code=400, detail="Appointment missing required fields: 'start' and 'end'")

    access_token = await get_access_token()
    if access_token:
        job_response = await create_job(access_token, job_data)
        return job_response
    else:
        logger.error("Access token is required but was not obtained.")
        raise HTTPException(status_code=500, detail="Access token is required.")
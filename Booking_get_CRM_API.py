from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime
import pytz
import urllib.parse

app = FastAPI()

# Base URL for the CRM API
CRM_API_BASE_URL = "https://public-api-gateway.st.dev/crm/v2"

# Credentials
client_id = "add your own"
client_secret = "add your own"
tenant_id = add your own
APP_KEY = "add your own"  # Ensure this is correct

# Function to get an access token with debugging
def get_access_token():
    url = "https://auth.servicetitan.io/connect/token"

    # Ensure proper URL encoding of parameters
    payload = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "tn.jpm.appointments:w"
    })

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    print("Attempting to get access token...")
    print("Token request URL:", url)
    print("Token request payload:", payload)

    try:
        response = requests.post(url, data=payload, headers=headers)
        print("Token response status code:", response.status_code)

        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access_token')
            print("Access token retrieved:", token[:10] + "..." if token else "None")
            return token
        else:
            print("Token response error:", response.text)
            raise Exception(f"Failed to retrieve access token: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print("Network error during token request:", str(e))
        raise Exception(f"Network error during token request: {e}")


@app.get("/bookings")
async def get_bookings(
    tenant: int,
    booking_provider: int,
    ids: str = None,
    page: int = None,
    pageSize: int = None,
    includeTotal: bool = None,
    createdBefore: str = None,
    createdOnOrAfter: str = None,
    modifiedBefore: str = None,
    modifiedOnOrAfter: str = None,
    externalId: str = None,
    sort: str = None
):
    # Construct the CRM API endpoint URL using tenant and booking_provider values
    url = f"{CRM_API_BASE_URL}/tenant/{tenant}/booking-provider/{booking_provider}/bookings"

    # Build the query parameters dictionary by including only non-null values
    params = {}
    if ids:
        params["ids"] = ids
    if page:
        params["page"] = page
    if pageSize:
        params["pageSize"] = pageSize
    if includeTotal is not None:
        # Convert Boolean to 'true' or 'false' for the query parameter
        params["includeTotal"] = str(includeTotal).lower()
    if createdBefore:
        params["createdBefore"] = createdBefore
    if createdOnOrAfter:
        params["createdOnOrAfter"] = createdOnOrAfter
    if modifiedBefore:
        params["modifiedBefore"] = modifiedBefore
    if modifiedOnOrAfter:
        params["modifiedOnOrAfter"] = modifiedOnOrAfter
    if externalId:
        params["externalId"] = externalId
    if sort:
        params["sort"] = sort

    # Get an access token if needed
    access_token = get_access_token()

    # Add the required ST-App-Key and Authorization headers if needed
    headers = {
        "Authorization": f"Bearer {access_token}" if access_token else None,
        "ST-App-Key": APP_KEY,  # Ensure this is correctly formatted and valid
        "Content-Type": "application/json"
    }

    print("Requesting CRM bookings with URL:", url)
    print("Query parameters:", params)
    print("Request headers:", headers)

    try:
        response = requests.get(url, params=params, headers=headers)
        print("CRM API response status:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            print("CRM API response data:", data)
            return data
        else:
            error_message = response.text
            print("CRM API error:", error_message)
            raise HTTPException(status_code=response.status_code, detail=error_message)
    except requests.exceptions.RequestException as e:
        print("Network error when calling CRM API:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

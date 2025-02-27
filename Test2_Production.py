from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime
import pytz
import urllib.parse

app = FastAPI()

# Credentials
client_id = "cid.sevhc9hatg3gkneoa0ky0pyzf"
client_secret = "cs1.lc8y5vfpkxnu420uf2qggwfmaf11kbm5giaegeuzbgkszrttbq"
tenant_id = 1561207974
job_id = 30920896
APP_KEY= "ak1.6w1flz9ji6k5btaaoviw0ikpa"


# Set the start and end times in local time (PST)
local_start_time = datetime(2025, 2, 26, 13, 0, 0)  # February 26, 2025, at 1 PM PST
local_end_time = datetime(2025, 2, 26, 14, 0, 0)  # February 26, 2025, at 2 PM PST

# Convert to UTC
local_tz = pytz.timezone('America/Los_Angeles')
utc_tz = pytz.timezone('UTC')
start_time_utc = local_tz.localize(local_start_time).astimezone(utc_tz)
end_time_utc = local_tz.localize(local_end_time).astimezone(utc_tz)
start_time_str = start_time_utc.isoformat().replace('+00:00', 'Z')  # Proper ISO format
end_time_str = end_time_utc.isoformat().replace('+00:00', 'Z')  # Proper ISO format


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


# Function to add appointment with debugging
def add_appointment():
    access_token = get_access_token()
    if not access_token:
        raise Exception("No access token retrieved")

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{tenant_id}/appointments"

    # Correct headers with ST-App-Key
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    appointment_data = {
        "jobId": job_id,
        "start": start_time_str,
        "end": end_time_str
    }

    print("Adding appointment...")
    print("API request URL:", url)
    print("API request payload:", appointment_data)
    print("API request headers:", {k: v[:10] + "..." if k == "Authorization" else v for k, v in headers.items()})

    try:
        response = requests.post(url, json=appointment_data, headers=headers)
        print("API response status code:", response.status_code)
        print("API response content:", response.text)

        if response.status_code == 200:
            print("Appointment added successfully")
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Failed to add appointment")
    except requests.exceptions.RequestException as e:
        print("Network error during appointment request:", str(e))
        raise Exception(f"Network error during appointment request: {e}")


# FastAPI endpoints
@app.post("/add_appointment")
async def add_appointment_endpoint():
    print("Received POST request to /add_appointment")
    try:
        result = add_appointment()
        print("Appointment added successfully:", result)
        return result
    except Exception as e:
        print("Error in endpoint:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# GET endpoint for browser testing
@app.get("/add_appointment")
async def add_appointment_get_endpoint():
    print("Received GET request to /add_appointment")
    return {"message": "This endpoint requires a POST request. Please use the appropriate method."}

# https://public-api-developer.st.dev/api-details/#api=tenant-jpm-v2&operation=Export_Jobs

import requests
import json
from fastapi import FastAPI
from pydantic import BaseModel

# Replace with your actual credentials
CLIENT_ID = "cid.sevhc9hatg3gkneoa0ky0pyzf"
CLIENT_SECRET = "cs1.lc8y5vfpkxnu420uf2qggwfmaf11kbm5giaegeuzbgkszrttbq"
TENANT_ID = "1561207974"
APP_KEY = "ak1.6w1flz9ji6k5btaaoviw0ikpa"

# FastAPI setup
app = FastAPI()


class ExportJobsResponse(BaseModel):
    hasMore: bool = False
    continueFrom: str = ""
    data: list = []
    error: str = ""  # Add error field to capture any error messages


# Function to get access token using client credentials
def get_access_token():
    url = "https://auth.servicetitan.io/connect/token"
    payload = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)

    # Debug: Check the response status and data
    print(f"Access token response status: {response.status_code}")

    if response.status_code == 200:
        token_response = response.json()
        print(f"Access token received: {token_response}")  # Debug print the token response
        return token_response['access_token']
    else:
        print(f"Failed to retrieve access token. Status code: {response.status_code}")
        return None


# Function to export jobs using the access token
def export_jobs(access_token, tenant_id, from_token=None, include_recent_changes=False):
    url = f"https://public-api-gateway.st.dev/jpm/v2/tenant/{tenant_id}/export/jobs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }
    params = {}

    if from_token:
        params["from"] = from_token
    if include_recent_changes:
        params["includeRecentChanges"] = "true"

    response = requests.get(url, headers=headers, params=params)

    # Debug: Print the response status and body
    print(f"Export jobs response status: {response.status_code}")
    print(f"Export jobs response body: {response.text}")

    # Handling the 401 Unauthorized error explicitly
    if response.status_code == 401:
        print("Unauthorized - Invalid access token")  # Debug print the error
        return {"error": "Unauthorized - Invalid access token", "hasMore": False, "continueFrom": "", "data": []}

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch jobs. Status code: {response.status_code}")
        return {"error": f"Failed to fetch jobs with status code {response.status_code}", "hasMore": False, "continueFrom": "", "data": []}


# FastAPI route to trigger job export
@app.get("/export-jobs", response_model=ExportJobsResponse)
async def get_export_jobs(from_token: str = None, include_recent_changes: bool = False):
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to get access token", "hasMore": False, "continueFrom": "", "data": []}

    export_response = export_jobs(access_token, TENANT_ID, from_token, include_recent_changes)

    # Return the proper response based on the result of the export jobs function
    if "error" in export_response:
        print(f"Export failed with error: {export_response['error']}")  # Debug the error
        return export_response  # Return error message with empty fields to avoid validation errors
    return export_response  # Only return the model if the export is successful

# If you want to run the FastAPI app, make sure to run it with Uvicorn:
# uvicorn <filename>:app --reload

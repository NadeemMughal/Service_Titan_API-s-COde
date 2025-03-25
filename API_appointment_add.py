import requests
from datetime import datetime
import pytz

# Replace with your actual credentials and tenant ID
client_id = "add your own"
client_secret = "add your own"
tenant_id = add your own
job_id = add your own

# Set the start and end times in local time (PST)
local_start_time = datetime(2025, 2, 26, 13, 0, 0)  # February 26, 2025, at 1 PM PST
local_end_time = datetime(2025, 2, 26, 14, 0, 0)    # February 26, 2025, at 2 PM PST

# Convert to UTC
utc_tz = pytz.timezone('UTC')
local_tz = pytz.timezone('America/Los_Angeles')
start_time_utc = local_tz.localize(local_start_time).astimezone(utc_tz)
end_time_utc = local_tz.localize(local_end_time).astimezone(utc_tz)

# Function to get an access token
def get_access_token():
    url = "https://auth.servicetitan.io/connect/token"
    payload = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    print("Access token response:", response.text)
    return response.json().get('access_token')

# Function to add appointment
def add_appointment():
    access_token = get_access_token()
    if not access_token:
        raise Exception("Failed to retrieve access token")
    url = f"https://api-integration.servicetitan.io/jpm/v2/tenant/{tenant_id}/appointments"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "App-Key": client_id,
        "Content-Type": "application/json",
    }
    appointment_data = {
        "jobId": job_id,
        "start": start_time_utc.isoformat(),
        "end": end_time_utc.isoformat()
    }
    print("Headers:", headers)
    print("Appointment data:", appointment_data)
    try:
        response = requests.post(url, json=appointment_data, headers=headers)
        print("API response status code:", response.status_code)
        print("API response content:", response.text)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

# Main function
if __name__ == "__main__":
    result = add_appointment()
    print(result)

import requests
import json

# Replace with your actual credentials
CLIENT_ID = "cid.5sz7j79l90xsz9umlgfws6q2j"
CLIENT_SECRET = "cs1.3n3iridot5dva4i91ty5g4fq1c8s9pmt4rk5o5ahupldlhkg2v"
TENANT_ID = "1561207974"
APP_KEY = "ak1.p1hyw417u4rd7c19faytek0t2"

def get_access_token():
    url = "https://auth.servicetitan.io/connect/token"
    payload = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)

    if response.status_code == 200:
        token_response = response.json()
        print("Access Token:", token_response['access_token'])
        return token_response['access_token']
    else:
        print("Failed to retrieve access token.")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        return None

def add_appointment(access_token, tenant_id, appointment_data):
    url = f"https://public-api-gateway.st.dev/jpm/v2/tenant/{tenant_id}/appointments"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    print("Appointment API URL:", url)
    print("Headers:", headers)
    print("Appointment Data:", appointment_data)

    response = requests.post(url, headers=headers, data=json.dumps(appointment_data))

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to add appointment. Status Code: {response.status_code}")
        return None

def main():
    access_token = get_access_token()
    if access_token:
        # Example appointment data
        appointment_data = {
            "jobId": 12345,  # Replace with the ID of the job you want to add an appointment to
            "start": "2024-03-01T10:00:00Z",  # Start date/time in UTC
            "end": "2024-03-01T12:00:00Z",  # End date/time in UTC
            "technicianIds": [67890],  # Optional: List of technician IDs
            "specialInstructions": "Please ensure the technician arrives on time."  # Optional
        }

        appointment_response = add_appointment(access_token, TENANT_ID, appointment_data)
        if appointment_response:
            print("Appointment added successfully.")
            print("Appointment Response:", appointment_response)
        else:
            print("Failed to add appointment.")

if __name__ == "__main__":
    main()

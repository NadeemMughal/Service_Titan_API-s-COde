import requests
import json

# Replace with your actual credentials
CLIENT_ID = "add your own"
CLIENT_SECRET = "add your own"
TENANT_ID = "add your own"
APP_KEY = "add your own"
BOOKING_PROVIDER_ID = "add your own"  # Replace with your booking provider ID


def get_access_token():
    url = "https://auth.servicetitan.io/connect/token"
    payload = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)

    if response.status_code == 200:
        token_response = response.json()
        return token_response['access_token']
    else:
        print("Failed to retrieve access token.")
        return None


def create_booking(access_token, tenant_id, booking_data):
    url = f"https://public-api-gateway.st.dev/crm/v2/tenant/{tenant_id}/booking-provider/{BOOKING_PROVIDER_ID}/bookings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(booking_data))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to create booking. Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return None


def main():
    access_token = get_access_token()
    if access_token:
        # Example booking data
        booking_data = {
            "source": "API Test",
            "name": "John Doe",
            "summary": "Test Booking Summary",
            "isFirstTimeClient": True,
            "externalId": "EXT-12345"
        }

        booking_response = create_booking(access_token, TENANT_ID, booking_data)
        if booking_response:
            print("Booking created successfully.")
            print("Booking Response:", booking_response)
        else:
            print("Failed to create booking.")


if __name__ == "__main__":
    main()

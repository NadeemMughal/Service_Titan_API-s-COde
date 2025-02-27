import urllib

import requests

url = "https://public-api-gateway.st.dev/crm/v2/tenant/1561207974/booking-provider/33459644/bookings"

# Credentials
client_id = "cid.sevhc9hatg3gkneoa0ky0pyzf"
client_secret = "cs1.lc8y5vfpkxnu420uf2qggwfmaf11kbm5giaegeuzbgkszrttbq"
tenant_id = 1561207974
APP_KEY = "ak1.6w1flz9ji6k5btaaoviw0ikpa"  # Ensure this is correct

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


access_token = get_access_token()  # Use your function to get the token
headers = {
    "Authorization": f"Bearer {access_token}",
    "ST-App-Key": APP_KEY,
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text)

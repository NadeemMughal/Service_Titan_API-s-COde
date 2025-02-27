import requests

# Replace with your actual credentials
CLIENT_ID = "cid.sevhc9hatg3gkneoa0ky0pyzf"
CLIENT_SECRET = "cs1.lc8y5vfpkxnu420uf2qggwfmaf11kbm5giaegeuzbgkszrttbq"
TENANT_ID = "1561207974"
APP_KEY= "ak1.6w1flz9ji6k5btaaoviw0ikpa"


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


def get_jobs(access_token, tenant_id):
    url = f"https://api.servicetitan.io/jpm/v2/tenant/{tenant_id}/export/jobs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve jobs. Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return None


def main():
    access_token = get_access_token()
    if access_token:
        jobs = get_jobs(access_token, TENANT_ID)
        if jobs:
            print("Jobs retrieved successfully.")
            print(jobs)
        else:
            print("Failed to retrieve job details.")


if __name__ == "__main__":
    main()

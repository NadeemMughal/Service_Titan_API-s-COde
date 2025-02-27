import requests
import json
import re  # Import the regular expression module

# Replace with your actual credentials
CLIENT_ID = "cid.sevhc9hatg3gkneoa0ky0pyzf"
CLIENT_SECRET = "cs1.lc8y5vfpkxnu420uf2qggwfmaf11kbm5giaegeuzbgkszrttbq"
TENANT_ID = "1561207974"
APP_KEY = "ak1.6w1flz9ji6k5btaaoviw0ikpa"


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
    print("Raw API Response:", response.text)  # CRITICAL: Print the raw response
    if response.status_code == 200:
        return response.text  # Return the raw text, not response.json()
    else:
        print(f"Failed to retrieve jobs. Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return None


def extract_job_type_ids(jobs_string):
    """Extracts the 'jobTypeId' from a string containing concatenated job dictionaries."""
    job_type_ids = []

    try:
        # Find all jobTypeId values, handling potential variations in quoting and whitespace
        job_matches = re.findall(r'"jobTypeId"\s*:\s*([0-9]+)|\'jobTypeId\'\s*:\s*([0-9]+)|jobTypeId\s*:\s*([0-9]+)',
                                 jobs_string)

        if job_matches:
            for match in job_matches:
                # The regex has 3 capture groups to make it work for both single quotes and double quotes, so iterate over each match
                for job_type_id in match:
                    if job_type_id:
                        job_type_ids.append(int(job_type_id))  # Convert string to Int if needed

        else:
            print("Warning: No job dictionaries found in the string.")

    except (TypeError, json.JSONDecodeError) as e:
        print(f"Error: Could not parse jobs data: {e}")
        return []  # Return an empty list in case of parsing failure

    return job_type_ids


def main():
    access_token = get_access_token()
    if access_token:
        jobs = get_jobs(access_token, TENANT_ID)
        if jobs:
            print("Jobs retrieved successfully.")
            job_type_ids = extract_job_type_ids(jobs)
            print("All Job Type IDs:", job_type_ids)

            # Get unique job type IDs
            unique_job_type_ids = list(set(job_type_ids))
            print("Unique Job Type IDs:", unique_job_type_ids)
        else:
            print("Failed to retrieve job details.")


if __name__ == "__main__":
    main()

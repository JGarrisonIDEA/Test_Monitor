import json
import requests  # make sure 'requests' is installed

API_URL = "https://example.com/api/endpoint"
TEAMS_WEBHOOK = "https://outlook.office.com/webhook/your-webhook-url"

def fetch_data():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()

def validate_data(data):
    # Replace this with the checks appropriate for your API
    return "expected_key" in data and data["expected_key"] is not None

def send_teams_message(message):
    payload = {"text": message}
    requests.post(TEAMS_WEBHOOK, json=payload)

def monitor():
    try:
        data = fetch_data()
    except Exception as e:
        send_teams_message(f"API call failed: {e}")
        return

    if not validate_data(data):
        send_teams_message("Warning: data validation failed")
    else:
        print("Data looks good")

if __name__ == "__main__":
    monitor()

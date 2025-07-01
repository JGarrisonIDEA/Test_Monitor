import json
from decimal import Decimal, InvalidOperation

try:
    import requests  # make sure 'requests' is installed
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    requests = None

API_URL = "https://example.com/api/endpoint"
TEAMS_WEBHOOK = "https://outlook.office.com/webhook/your-webhook-url"

def fetch_data():
    if requests is None:
        raise RuntimeError("The 'requests' package is required to fetch data")

    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()

def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _has_two_decimal_places(value):
    try:
        return Decimal(str(value)).as_tuple().exponent == -2
    except (InvalidOperation, TypeError, ValueError):
        return False

def validate_data(data):
    if not isinstance(data, dict):
        return False

    name = data.get("name")
    quantity = data.get("quantity")
    price = data.get("price")

    if not isinstance(name, str):
        return False
    if not isinstance(quantity, int):
        return False
    if not isinstance(price, (float, int, str)) or not _has_two_decimal_places(price):
        return False

    return True

def send_teams_message(message):
    if requests is None:
        print(f"[Teams message not sent] {message}")
        return

    payload = {"text": message}
    requests.post(TEAMS_WEBHOOK, json=payload)

def monitor(filepath=None):
    try:
        if filepath:
            data = load_json_file(filepath)
        else:
            data = fetch_data()
    except Exception as e:
        send_teams_message(f"API call failed: {e}")
        return

    if not validate_data(data):
        send_teams_message("Warning: data validation failed")
    else:
        print("Data looks good")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate API or file data")
    parser.add_argument(
        "--file", dest="file", help="Path to JSON file containing test data"
    )
    args = parser.parse_args()

    monitor(args.file)

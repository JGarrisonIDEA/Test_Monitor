import json
from decimal import Decimal, InvalidOperation

try:
    import requests  # make sure 'requests' is installed
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    requests = None

API_URL = "https://example.com/api/endpoint"
TEAMS_WEBHOOK = (
    "https://prod-106.westus.logic.azure.com:443/workflows/49ab5cbe1b274993af0723d33fe6f080/"
    "triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun"
    "&sv=1.0&sig=CeyLTWbKgyRWRigW3k4fVWAPBOkk_WAqPFKpve4MC88"
)

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

    payload = {
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.3",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "\ud83d\udea8 Monitoring Alert",
                            "weight": "Bolder",
                            "size": "Large",
                            "color": "Attention",
                        },
                        {"type": "TextBlock", "text": message, "wrap": True},
                    ],
                },
            }
        ]
    }
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

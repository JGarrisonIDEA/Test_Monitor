# Test_Monitor

This repository contains a simple monitoring script that validates JSON
payloads and posts alerts to Microsoft Teams. Use `monitor.py` to fetch
data from an API or load a JSON file for testing.

```bash
python monitor.py --file bad_data.json
```

Override the default API endpoint with `--api-url`:

```bash
python monitor.py --api-url https://a23c30a5-a1d1-49e4-abf7-f244af23174a.mock.pstmn.io/data
```

If validation fails, an adaptive card is sent to Teams via the configured
webhook.

Webhooks URL for chat with Shahan

```bash
https://prod-94.westus.logic.azure.com:443/workflows/05433b6b6a0c46e4bcf1eaa6223186e8/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=zG3QskuPLy-muAWRZnfXr__apYD_1nO1i90o_IYbUBQ
```

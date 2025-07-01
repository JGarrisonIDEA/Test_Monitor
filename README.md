# Test_Monitor

This repository contains a simple monitoring script that validates JSON
payloads and posts alerts to Microsoft Teams. Use `monitor.py` to fetch
data from an API or load a JSON file for testing.

```bash
python monitor.py --file bad_data.json
```

Override the default API endpoint with `--api-url`:

```bash
python monitor.py --api-url https://api.example.com/data
```

If validation fails, an adaptive card is sent to Teams via the configured
webhook.

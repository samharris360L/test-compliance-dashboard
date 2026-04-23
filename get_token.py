#!/usr/bin/env python3
"""
Simple script to authenticate with 360Learning API v2 and retrieve a bearer token.

Usage:
    1. Copy .env.example to .env
    2. Fill in your CLIENT_ID and CLIENT_SECRET in .env
    3. Run: python get_token.py
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# Change to "https://app.us.360learning.com" if you're on the US platform
BASE_URL = os.getenv("BASE_URL", "https://app.360learning.com")


def get_access_token(client_id: str, client_secret: str, base_url: str) -> dict:
    """Request an access token from 360Learning using client credentials."""
    url = f"{base_url}/api/v2/oauth2/token"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> int:
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: Missing CLIENT_ID or CLIENT_SECRET.")
        print("Create a .env file (see .env.example) with your credentials.")
        return 1

    print(f"Requesting access token from {BASE_URL} ...")
    try:
        data = get_access_token(CLIENT_ID, CLIENT_SECRET, BASE_URL)
    except requests.exceptions.HTTPError as exc:
        print(f"HTTP error: {exc}")
        print(f"Response body: {exc.response.text}")
        return 1
    except requests.exceptions.RequestException as exc:
        print(f"Request failed: {exc}")
        return 1

    print("\nSuccess! Token details:")
    print(json.dumps(data, indent=2))

    token = data.get("access_token")
    if token:
        print("\nUse this in an Authorization header like:")
        print(f'  Authorization: Bearer {token}')

    return 0


if __name__ == "__main__":
    sys.exit(main())

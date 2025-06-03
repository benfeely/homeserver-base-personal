#!/usr/bin/env python3
"""
OPNsense API Test Script

This script tests the connection to the OPNsense API and performs 
a simple status check. Update the API_KEY and API_SECRET variables
with your OPNsense API credentials.
"""

import requests
import os
import json
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# API Configuration - Update these with your VM's IP address
OPNSENSE_URL = os.environ.get("OPNSENSE_URL", "https://192.168.1.1")
API_KEY = os.environ.get("OPNSENSE_API_KEY", "your_api_key")
API_SECRET = os.environ.get("OPNSENSE_API_SECRET", "your_api_secret")

# Create session with authentication
session = requests.Session()
session.auth = (API_KEY, API_SECRET)
session.verify = False  # For self-signed certificates

def api_call(method, endpoint, data=None):
    """Make API call to OPNsense"""
    url = f"{OPNSENSE_URL}/api/{endpoint}"
    
    try:
        if method == "GET":
            response = session.get(url, timeout=10)
        elif method == "POST":
            response = session.post(url, json=data, timeout=10)
        
        # Raise exception for HTTP errors
        response.raise_for_status()
        
        return response.json() if response.text else {}
    
    except requests.exceptions.HTTPError as err:
        error_msg = f"HTTP Error: {err}"
        try:
            error_details = response.json()
            print(f"Error {response.status_code}: {json.dumps(error_details)}")
            print(f"Endpoint: {endpoint}, Data: {json.dumps(data)}")
        except:
            print(f"Error {response.status_code}: {response.text}")
        
        return None
    
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return None

def test_api_connection():
    """Test connection to OPNsense API"""
    print(f"Testing connection to OPNsense API at {OPNSENSE_URL}...")
    
    # Try to get system information
    result = api_call("GET", "core/system/info")
    
    if result:
        print("API connection successful!")
        print(f"System information: {json.dumps(result, indent=2)}")
        return True
    else:
        print("API connection failed!")
        print("Please check your API credentials and ensure OPNsense API is enabled.")
        return False

if __name__ == "__main__":
    test_api_connection()

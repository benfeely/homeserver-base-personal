#!/usr/bin/env python3
"""
OPNsense API Helper Module

This module provides helper functions for interacting with the OPNsense API.
It can be imported by other scripts to simplify API calls.
"""

import requests
import os
import json
import logging
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class OPNsenseAPI:
    """OPNsense API wrapper class"""
    
    def __init__(self, url=None, key=None, secret=None):
        """Initialize the API wrapper with credentials"""
        self.url = url or os.environ.get("OPNSENSE_URL", "https://192.168.1.1")
        self.key = key or os.environ.get("OPNSENSE_API_KEY")
        self.secret = secret or os.environ.get("OPNSENSE_API_SECRET")
        
        if not self.key or not self.secret:
            raise ValueError("API key and secret must be provided or set as environment variables")
        
        self.session = self._create_session()
        self.logger = logging.getLogger('opnsense-api')
    
    def _create_session(self):
        """Create an authenticated session for API calls"""
        session = requests.Session()
        session.auth = (self.key, self.secret)
        session.verify = False  # For self-signed certificates
        return session
    
    def get(self, endpoint):
        """Make a GET request to the OPNsense API"""
        url = f"{self.url}/api/{endpoint}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API GET request failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def post(self, endpoint, data=None):
        """Make a POST request to the OPNsense API"""
        url = f"{self.url}/api/{endpoint}"
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API POST request failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_firmware_status(self):
        """Get firmware status information"""
        return self.get("core/firmware/status")
    
    def get_system_status(self):
        """Get system status information"""
        return self.get("core/system/status")
    
    def get_interfaces(self):
        """Get network interfaces information"""
        return self.get("interfaces/overview/interfacesInfo")
    
    def get_firewall_rules(self):
        """Get firewall rules"""
        return self.get("firewall/filter/searchRule")
    
    def get_firewall_aliases(self):
        """Get firewall aliases"""
        return self.get("firewall/alias/searchItem")
    
    def backup_config(self):
        """Create a backup of the current configuration"""
        return self.get("core/backup/download")
    
    def get_gateways(self):
        """Get gateway information"""
        return self.get("routes/gateway/status")
    
    def get_dhcp_leases(self):
        """Get DHCP leases"""
        return self.get("dhcp/leases/searchLease")
    
    def ping_host(self, host, count=3):
        """Ping a host from the OPNsense router"""
        data = {
            "host": host,
            "count": count
        }
        return self.post("diagnostics/interface/ping", data)

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        api = OPNsenseAPI()
        status = api.get_system_status()
        print(json.dumps(status, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure environment variables are set (OPNSENSE_URL, OPNSENSE_API_KEY, OPNSENSE_API_SECRET)")
        print("Or run: source ./set-env.sh")

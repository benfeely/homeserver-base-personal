#!/usr/bin/env python3
"""
OPNsense UTM Environment Manager

This script helps manage the OPNsense UTM environment, including
checking its status and managing configurations.
"""

import subprocess
import os
import time
import sys
import requests
import argparse
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Configuration - Update with your VM's IP
OPNSENSE_URL = os.environ.get("OPNSENSE_URL", "https://192.168.1.1")
MAX_WAIT_TIME = 180  # seconds

def check_opnsense_availability():
    """Check if the OPNsense web UI is available"""
    print(f"Checking if OPNsense is available at {OPNSENSE_URL}...")
    
    start_time = time.time()
    while time.time() - start_time < MAX_WAIT_TIME:
        try:
            response = requests.get(OPNSENSE_URL, verify=False, timeout=5)
            if response.status_code == 200 or response.status_code == 302:
                print("OPNsense is available!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        # Wait a bit before trying again
        print("Waiting for OPNsense to become available...")
        time.sleep(5)
    
    print(f"OPNsense did not become available within {MAX_WAIT_TIME} seconds.")
    return False

def verify_api_access():
    """Verify API access to OPNsense"""
    try:
        # Execute the test_api.py script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_api.py")
        subprocess.run([sys.executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError:
        print("API test failed. Make sure you've configured API access in OPNsense.")
        return False

def backup_config():
    """Backup the OPNsense configuration"""
    try:
        # Execute the opnsense_config.py script with backup parameter
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "opnsense_config.py")
        subprocess.run([sys.executable, script_path, "backup"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return False

def restore_config(filename=None):
    """Restore an OPNsense configuration"""
    try:
        # Execute the opnsense_config.py script with restore parameter
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "opnsense_config.py")
        if filename:
            subprocess.run([sys.executable, script_path, "restore", filename], check=True)
        else:
            subprocess.run([sys.executable, script_path, "restore"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Restore failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Manage OPNsense UTM environment")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Check command
    subparsers.add_parser("check", help="Check if OPNsense is available")
    
    # API command
    subparsers.add_parser("api", help="Test API access to OPNsense")
    
    # Backup command
    subparsers.add_parser("backup", help="Backup the OPNsense configuration")
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore an OPNsense configuration")
    restore_parser.add_argument("filename", nargs="?", help="Configuration file to restore")
    
    args = parser.parse_args()
    
    if args.command == "check":
        check_opnsense_availability()
    elif args.command == "api":
        verify_api_access()
    elif args.command == "backup":
        backup_config()
    elif args.command == "restore":
        restore_config(args.filename if hasattr(args, "filename") else None)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

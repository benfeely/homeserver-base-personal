#!/usr/bin/env python3
"""
OPNsense Configuration Backup and Restore Script

This script handles the backup and restore of OPNsense configurations,
which is critical for the development-to-production workflow.
"""

import requests
import os
import sys
import json
import datetime
import argparse
import logging
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('opnsense-config.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('opnsense-config')

def get_api_config():
    """Get API configuration from environment variables or prompt user"""
    url = os.environ.get("OPNSENSE_URL")
    key = os.environ.get("OPNSENSE_API_KEY")
    secret = os.environ.get("OPNSENSE_API_SECRET")
    
    if not url:
        url = input("Enter OPNsense URL (e.g., https://192.168.1.1): ")
    if not key:
        key = input("Enter OPNsense API key: ")
    if not secret:
        secret = input("Enter OPNsense API secret: ")
    
    return url, key, secret

def create_session(url, key, secret):
    """Create authenticated session for API calls"""
    session = requests.Session()
    session.auth = (key, secret)
    session.verify = False  # For self-signed certificates
    
    # Test connection
    try:
        response = session.get(f"{url}/api/core/system/info", timeout=10)
        response.raise_for_status()
        return session
    except Exception as e:
        logger.error(f"Failed to connect to OPNsense API: {e}")
        return None

def api_call(session, url, method, endpoint, data=None, files=None):
    """Make API call to OPNsense"""
    api_url = f"{url}/api/{endpoint}"
    
    try:
        if method == "GET":
            response = session.get(api_url, timeout=30)
        elif method == "POST":
            if files:
                response = session.post(api_url, files=files, timeout=120)
            else:
                response = session.post(api_url, json=data, timeout=30)
        
        # Raise exception for HTTP errors
        response.raise_for_status()
        
        if response.text:
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text
        return {}
    
    except requests.exceptions.HTTPError as err:
        error_msg = f"HTTP Error: {err}"
        try:
            error_details = response.json()
            logger.error(f"Error {response.status_code}: {json.dumps(error_details)}")
            logger.error(f"Endpoint: {endpoint}, Data: {json.dumps(data) if data else None}")
        except:
            logger.error(f"Error {response.status_code}: {response.text}")
        
        return None
    
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}")
        return None

def backup_configuration(session, url, output_dir="backups"):
    """Create and download OPNsense configuration backup"""
    # Create backup directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create backup through API
    logger.info("Creating backup through OPNsense API...")
    result = api_call(session, url, "POST", "core/backup/backup")
    if not result:
        logger.error("Failed to create backup")
        return False
    
    # Download backup file
    backup_file = result.get('filename')
    if not backup_file:
        logger.error("Backup filename not found in API response")
        return False
    
    logger.info(f"Downloading backup file: {backup_file}")
    
    # Format timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Download the backup file
    try:
        response = session.get(f"{url}/api/core/backup/download/{backup_file}", timeout=30)
        response.raise_for_status()
        
        # Save to file
        output_file = f"{output_dir}/config-{timestamp}.xml"
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Backup saved to {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error downloading backup: {str(e)}")
        return False

def restore_configuration(session, url, config_file):
    """Restore OPNsense configuration from an XML file"""
    if not os.path.exists(config_file):
        logger.error(f"Configuration file not found: {config_file}")
        return False
    
    logger.info(f"Restoring configuration from {config_file}")
    
    try:
        with open(config_file, 'rb') as f:
            files = {'conffile': (os.path.basename(config_file), f, 'application/xml')}
            
            # The specific endpoint and parameters for restore
            result = api_call(session, url, "POST", "core/backup/restore", files=files)
            
            if result:
                logger.info("Successfully initiated configuration restore")
                logger.info("OPNsense will reboot to apply the configuration")
                return True
            else:
                logger.error("Failed to restore configuration")
                return False
    
    except Exception as e:
        logger.error(f"Error restoring configuration: {str(e)}")
        return False

def list_backups(output_dir="backups"):
    """List available backup files"""
    if not os.path.exists(output_dir):
        logger.error(f"Backup directory not found: {output_dir}")
        return False
    
    backup_files = [f for f in os.listdir(output_dir) if f.startswith("config-") and f.endswith(".xml")]
    
    if not backup_files:
        logger.info("No backup files found")
        return []
    
    # Sort by filename (which includes timestamp)
    backup_files.sort(reverse=True)
    
    logger.info(f"Found {len(backup_files)} backup files:")
    for i, file in enumerate(backup_files):
        # Extract timestamp from filename
        timestamp = file.replace("config-", "").replace(".xml", "")
        try:
            # Convert to readable date format
            date_str = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"{i+1}. {file} (created {date_str})")
        except:
            logger.info(f"{i+1}. {file}")
    
    return backup_files

def main():
    parser = argparse.ArgumentParser(description="OPNsense Configuration Backup and Restore Tool")
    parser.add_argument("action", choices=["backup", "restore", "list"], help="Action to perform")
    parser.add_argument("--file", help="Configuration file for restore action")
    parser.add_argument("--output-dir", default="backups", help="Directory for backups (default: backups)")
    
    args = parser.parse_args()
    
    if args.action == "list":
        list_backups(args.output_dir)
        return
    
    # Get API configuration
    url, key, secret = get_api_config()
    
    # Create session
    session = create_session(url, key, secret)
    if not session:
        return
    
    if args.action == "backup":
        backup_configuration(session, url, args.output_dir)
    
    elif args.action == "restore":
        if not args.file:
            backup_files = list_backups(args.output_dir)
            if not backup_files:
                return
            
            choice = input("\nEnter the number of the backup to restore (or 'q' to quit): ")
            if choice.lower() == 'q':
                return
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(backup_files):
                    config_file = os.path.join(args.output_dir, backup_files[index])
                else:
                    logger.error("Invalid selection")
                    return
            except ValueError:
                logger.error("Invalid input")
                return
        else:
            config_file = args.file
        
        restore_configuration(session, url, config_file)

if __name__ == "__main__":
    main()

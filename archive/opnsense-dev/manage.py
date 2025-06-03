#!/usr/bin/env python3
"""
OPNsense Development Environment Manager

This script helps manage the OPNsense development environment, including
starting/stopping the container and checking its status.
"""

import subprocess
import os
import time
import sys
import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Configuration
DOCKER_COMPOSE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docker-compose.yml")
OPNSENSE_URL = "https://localhost:8443"
MAX_WAIT_TIME = 180  # seconds

def run_command(command, capture_output=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,
            capture_output=capture_output,
            text=True
        )
        return result.stdout if capture_output else True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        if capture_output and e.stderr:
            print(f"Error output: {e.stderr}")
        return None

def start_environment():
    """Start the OPNsense development environment"""
    print("Starting OPNsense development environment...")
    
    # Create data directories if they don't exist
    os.makedirs(os.path.join(os.path.dirname(DOCKER_COMPOSE_FILE), "conf"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(DOCKER_COMPOSE_FILE), "etc"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(DOCKER_COMPOSE_FILE), "var"), exist_ok=True)
    
    # Start the container
    result = run_command(f"docker-compose -f {DOCKER_COMPOSE_FILE} up -d", capture_output=False)
    
    if result:
        print("Container started. Waiting for OPNsense to initialize...")
        
        # Wait for the web interface to become available
        start_time = time.time()
        while time.time() - start_time < MAX_WAIT_TIME:
            try:
                # Try to connect to the web interface
                response = requests.get(OPNSENSE_URL, verify=False, timeout=5)
                if response.status_code == 200:
                    print(f"OPNsense is ready! Web interface is available at {OPNSENSE_URL}")
                    return True
            except requests.exceptions.RequestException:
                # Not ready yet, keep waiting
                pass
            
            # Print a dot to show progress
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(5)
        
        print("\nOPNsense container is running, but web interface did not become available within the timeout period.")
        print("Check the container logs for details:")
        print(f"docker-compose -f {DOCKER_COMPOSE_FILE} logs")
        return False
    else:
        return False

def stop_environment():
    """Stop the OPNsense development environment"""
    print("Stopping OPNsense development environment...")
    result = run_command(f"docker-compose -f {DOCKER_COMPOSE_FILE} down", capture_output=False)
    return result

def check_status():
    """Check the status of the OPNsense development environment"""
    print("Checking OPNsense development environment status...")
    result = run_command(f"docker-compose -f {DOCKER_COMPOSE_FILE} ps")
    if result:
        print(result)
    
    # Check if the container is running
    container_status = run_command("docker ps --filter 'name=opnsense-dev' --format '{{.Status}}'")
    if container_status and "Up" in container_status:
        print("OPNsense container is running.")
        
        # Try to connect to the web interface
        try:
            response = requests.get(OPNSENSE_URL, verify=False, timeout=5)
            if response.status_code == 200:
                print(f"Web interface is accessible at {OPNSENSE_URL}")
            else:
                print(f"Web interface responded with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Could not connect to web interface: {e}")
    else:
        print("OPNsense container is not running.")

def display_help():
    """Display usage information"""
    print("OPNsense Development Environment Manager")
    print("Usage:")
    print("  python manage.py [command]")
    print("")
    print("Commands:")
    print("  start    - Start the OPNsense development environment")
    print("  stop     - Stop the OPNsense development environment")
    print("  status   - Check the status of the OPNsense development environment")
    print("  help     - Display this help message")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        display_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "start":
        if start_environment():
            sys.exit(0)
        else:
            sys.exit(1)
    elif command == "stop":
        if stop_environment():
            sys.exit(0)
        else:
            sys.exit(1)
    elif command == "status":
        check_status()
    elif command == "help":
        display_help()
    else:
        print(f"Unknown command: {command}")
        display_help()
        sys.exit(1)

#!/usr/bin/env python3
"""
Initialize Network Automation Repository

This script creates the folder structure for the network automation repository
as defined in infrastructure-code.md.
"""

import os
import sys

def create_directory_structure(base_path):
    """Create the directory structure for the network automation repository"""
    
    structure = {
        "scripts": {
            "utils": {
                "__init__.py": "",
                "api.py": "",
                "logging.py": "",
                "validators.py": ""
            },
            "setup.py": "",
            "interfaces.py": "",
            "vlans.py": "",
            "firewall.py": "",
            "dhcp.py": "",
            "dns.py": "",
            "diagnostics.py": ""
        },
        "config": {
            "interfaces.yaml": "",
            "vlans.yaml": "",
            "firewall.yaml": "",
            "dhcp.yaml": "",
            "dns.yaml": "",
            "devices.yaml": ""
        },
        "services": {
            "eufy": {
                "firewall.yaml": "",
                "setup.py": ""
            },
            "proxmox": {
                "cluster.py": "",
                "vm.py": ""
            }
        },
        "tests": {
            "test_interfaces.py": "",
            "test_vlans.py": "",
            "test_firewall.py": "",
            "test_integration.py": ""
        },
        "backups": {},
        "README.md": "# Network Automation\n\nThis repository contains automation scripts for managing OPNsense network infrastructure."
    }
    
    def create_structure(current_path, structure_dict):
        for key, value in structure_dict.items():
            path = os.path.join(current_path, key)
            
            if isinstance(value, dict):
                # It's a directory
                os.makedirs(path, exist_ok=True)
                create_structure(path, value)
            else:
                # It's a file
                with open(path, 'w') as f:
                    f.write(value)
    
    # Create the base directory if it doesn't exist
    os.makedirs(base_path, exist_ok=True)
    
    # Create the directory structure
    create_structure(base_path, structure)
    
    print(f"Directory structure created at {base_path}")

if __name__ == "__main__":
    # Default path
    default_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "network-automation")
    
    # Get the base path from the command line if provided
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = default_path
    
    create_directory_structure(base_path)
    print("Network automation repository initialized successfully!")
    print(f"To start working with the repository, run:\ncd {base_path}")

# OPNsense Development Environment with UTM

This directory contains files and instructions for setting up an OPNsense development environment using UTM on macOS. This development environment will allow you to test configuration changes before deploying them to your production OPNsense instance on Proxmox.

## Setup Instructions

### 1. Install UTM

1. Download and install UTM from [getutm.app](https://getutm.app/) or via the Mac App Store.
2. Open UTM after installation.

### 2. Download OPNsense ISO

1. Use the provided download helper script:
   ```bash
   ./download-iso.sh
   ```
   
   Or manually download the latest OPNsense ISO from [opnsense.org/download](https://opnsense.org/download/).
   - Choose the AMD64 (x86-64) architecture version.
   - Select either the DVD image (iso) or VGA image depending on your preference.

### 3. Create a New VM in UTM

1. Click "Create a New Virtual Machine" in UTM.
2. Choose "Virtualize" for x86/x64 architecture.
3. Click "Browse" and select the OPNsense ISO file.
4. Configure the virtual machine:
   - Name: OPNsense-Dev
   - CPU: 2 cores (minimum)
   - Memory: 2GB (minimum)
   - Storage: 16GB

5. Set up network interfaces:
   - Interface 1: Shared Network (this will be your WAN)
   - Add a second interface: Host-only Network (this will be your LAN)
   - If needed, add more interfaces for additional networks

6. Complete the VM creation process.

### 4. Install OPNsense

1. Start the VM and follow the OPNsense installation prompts.
2. Select standard options for installation.
3. When asked about interfaces, assign:
   - vtnet0 (or similar) as WAN
   - vtnet1 (or similar) as LAN

4. Set a static IP for the LAN interface (e.g., 192.168.1.1/24).
5. Complete the installation and reboot.

### 5. Basic Configuration

1. Access the OPNsense web interface by browsing to https://192.168.1.1 from your Mac.
   - You'll need to ensure your Mac is connected to the Host-only network.
   - Default credentials are root/opnsense.
   
2. Use the `manage.py` script to check if OPNsense is available:
   ```bash
   cd /Users/benfeely/Projects/homeserver-base/personal/opnsense-utm
   ./manage.py check
   ```

2. Complete the initial setup wizard.
3. Update the system to the latest version.

### 6. Enable API Access

1. Navigate to System > Settings > Administration.
2. Enable the API (legacy).
3. Go to System > Access > Users.
4. Add an API key for your automation user.
5. Save the API key and secret securely.

### 7. Set Environment Variables

1. Use the provided script to set environment variables for API access:
   ```bash
   source ./set-env.sh
   ```
   
   This will prompt you for your OPNsense URL, API key, and API secret,
   and export them as environment variables for use with the scripts.

### 7. Test API Connectivity

1. Update the test_api.py script with your OPNsense VM's IP address and API credentials.
2. Run the script to verify API connectivity:
   ```bash
   python3 test_api.py
   ```
   
   Or use the management script:
   ```bash
   ./manage.py api
   ```

### 8. Configuration Management

The `opnsense_config.py` script handles configuration backup and restore operations:

1. To backup the current configuration:
   ```bash
   python3 opnsense_config.py backup
   ```
   
   Or use the management script:
   ```bash
   ./manage.py backup
   ```

2. To restore a configuration:
   ```bash
   python3 opnsense_config.py restore [filename]
   ```
   
   Or use the management script:
   ```bash
   ./manage.py restore [filename]
   ```

3. To set up a directory structure for organizing your configurations:
   ```bash
   ./setup_config_dirs.sh
   ```

### 9. API Helper Module

The `opnsense_api.py` module provides a reusable Python class for OPNsense API interactions:

```python
from opnsense_api import OPNsenseAPI

# Initialize the API client
api = OPNsenseAPI()

# Get system status
status = api.get_system_status()
print(status)

# Get firewall rules
rules = api.get_firewall_rules()
print(rules)
```

### 10. Initialize Infrastructure Code Repository

1. Run the init_repo.py script to create the folder structure for your infrastructure code:
   ```bash
   python3 init_repo.py
   ```

## Management Script

The `manage.py` script provides a convenient way to manage your OPNsense development environment:

```bash
# Check if OPNsense is available
./manage.py check

# Test API connectivity
./manage.py api

# Backup the current configuration
./manage.py backup

# Restore a configuration
./manage.py restore [filename]
```

## Network Topology

For development purposes, you can set up a simplified network topology:

- WAN: Connected to your Mac's shared network (gets internet from your Mac)
- LAN: 192.168.1.0/24 (Host-only network for management)
- Optional: Additional interfaces for testing VLANs or other network segments

## Recommended Workflow

1. Make changes to your infrastructure code (YAML files).
2. Apply changes to the development OPNsense VM using the API.
3. Test and validate the changes.
4. Backup the configuration using `./manage.py backup`.
5. Deploy the configuration to your production OPNsense on Proxmox.

## Troubleshooting

- If you can't connect to the OPNsense web interface, verify your Mac is properly connected to the Host-only network.
- If API calls fail, check that the API is enabled and your credentials are correct.
- For networking issues, verify the interface assignments in OPNsense.

# OPNsense on Proxmox Deployment Plan

This document outlines the implementation plan for setting up and managing an OPNsense router in a Proxmox VM on the Protectli hardware, using a direct deployment workflow that maximizes AI assistance.

## Objectives

- Set up Proxmox on Protectli hardware as the hypervisor platform
- Deploy OPNsense as a VM for network routing and security
- Establish a reliable configuration management approach
- Leverage infrastructure-as-code for all changes
- Enable AI-assisted network management
- Implement automated testing and validation of changes

## Workflow Overview

```
[Configuration Development] → [OPNsense Deployment] → [Configuration Management] → [Validation]
            ↑                                                                         |
            |                                                                         |
            └─────────────────────────── [Feedback] ────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Proxmox Setup on Protectli Hardware

1. Prepare for Proxmox installation

   - Download Proxmox VE ISO
   - Create bootable USB installation media
   - Gather network configuration details for Proxmox host
   - Plan networking for cluster integration with T40 Proxmox instance

2. Install Proxmox VE on Protectli hardware

   - Configure BIOS settings (enable virtualization, adjust boot order)
   - Install Proxmox from USB to internal storage
   - Set up initial networking for Proxmox management
     - Use a static IP on same subnet as T40 Proxmox
     - Configure unique hostname different from T40 instance
   - Apply system updates and optimizations

3. Configure Proxmox networking for OPNsense

   - Create network bridges for WAN and LAN interfaces
   - Configure any additional network bridges for VLANs/DMZ
   - Validate network connectivity

4. Set up Proxmox clustering
   - On T40 Proxmox: Create a cluster if not already done
     ```bash
     # Run on T40 only if no cluster exists yet
     pvecm create clustername
     ```
   - On T40 Proxmox: Generate join information for new node
     ```bash
     # Generate join token on T40
     pvecm token generate
     ```
   - On Protectli Proxmox: Join the existing cluster
     ```bash
     # Run on Protectli Proxmox with token from T40
     pvecm add T40-proxmox-ip-address -token token_from_previous_step
     ```
   - Verify cluster status on both nodes
     ```bash
     # Run on either node
     pvecm status
     ```

### Phase 2: OPNsense VM Deployment

1. Create OPNsense VM on Proxmox

   - Allocate appropriate resources (CPU, RAM, storage)
   - Configure network interfaces to match production requirements
   - Install OPNsense from ISO

2. Configure initial network settings

   - Basic WAN and LAN configuration
   - Minimum viable firewall rules
   - SSH access for management

3. Enable API access for automation
   - Enable the OPNsense API
   - Create dedicated API user with appropriate permissions
   - Generate and securely store API credentials
   - Test API connectivity

### Phase 3: Configuration Management Implementation

1. Initialize the infrastructure code repository

   - Create the folder structure for organizing configurations
   - Set up version control with Git
   - Create initial configuration YAML files

2. Implement core Python utility scripts

   - API authentication and interaction
   - Configuration loading from YAML
   - Logging and error handling

3. Develop configuration deployment scripts

   - Interface configuration
   - VLAN setup
   - Firewall rules
   - DNS and DHCP configuration

4. Implement configuration backup and restore
   - Create scripts for configuration backup
   - Implement configuration restoration
   - Set up automated backup schedule
   - Test backup and restore functionality

### Phase 4: Advanced Configuration and Integration

1. Implement Proxmox VM management integration

   - VM snapshot before configuration changes
   - Power management (restart after major changes)
   - Monitoring of VM health

2. Add validation and testing capabilities

   - Pre-deployment validation
   - Post-deployment testing
   - Automated rollback capability

3. Create documentation and usage guidelines
   - Document the workflow for future reference
   - Create templates for common changes
   - Add examples for AI-assisted configuration development

## Detailed Implementation

### Configuration Backup and Restore Scripts

The key to this workflow is the ability to reliably backup and restore configurations of your OPNsense instance. Two core functions will be implemented:

```python
def backup_configuration():
    """Create and download OPNsense configuration backup"""
    import datetime

    # Create backup through API
    result = api_call("POST", "system/backup/backup")
    if not result:
        return False

    # Download backup file
    backup_file = result.get('filename')
    if not backup_file:
        return False

    # Format timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Download the backup file
    response = session.get(f"{OPNSENSE_URL}/system/backup/download/{backup_file}")

    # Save to file
    with open(f"backups/config-{timestamp}.xml", 'wb') as f:
        f.write(response.content)

    return True
```

```python
def restore_opnsense_configuration(config_xml_path):
    """Restore OPNsense configuration from an XML file via API"""
    try:
        with open(config_xml_path, 'rb') as f:
            files = {'conffile': (os.path.basename(config_xml_path), f, 'application/xml')}

            # The specific endpoint and parameters must be verified from OPNsense API docs
            response = session.post(
                f"{OPNSENSE_URL}/api/core/backup/restore",
                files=files,
                timeout=120  # Configuration restore can take time
            )

        response.raise_for_status()

        logger.info(f"Successfully initiated configuration restore from {config_xml_path}")
        logger.info("OPNsense will reboot to apply the configuration")

        return True

    except Exception as e:
        logger.exception(f"Error restoring OPNsense configuration: {str(e)}")
        return False
```

### Configuration Management Workflow

1. **Develop configurations:**

   - Create or update YAML configuration files
   - Run deployment scripts to apply changes via API
   - Test and validate changes

2. **Backup configurations:**

   - Run the backup script to export the configuration XML
   - Store the XML file in version control
   - Tag configurations with appropriate version information

3. **Apply configuration changes:**
   - Take a snapshot of the OPNsense VM (via Proxmox API)
   - Apply configuration changes through API or restore from backup
   - Wait for OPNsense to restart and apply changes
   - Validate the changes
   - If issues occur, restore from the Proxmox snapshot

### AI Assistance Integration

This workflow is particularly amenable to AI assistance:

1. **Configuration generation:** AI can help generate or modify YAML configuration files based on natural language descriptions of desired network changes.

2. **Script enhancement:** AI can help develop and enhance the Python scripts used for configuration deployment, validation, and testing.

3. **Troubleshooting:** When issues occur, AI can analyze logs and validation outputs to suggest solutions.

4. **Documentation:** AI can assist in documenting changes, generating change summaries, and maintaining the infrastructure-as-code repository.

## Implementation Steps

### Step 1: Proxmox Installation

1. **Download Proxmox VE ISO**

   ```bash
   mkdir -p ~/Downloads/proxmox
   curl -L -o ~/Downloads/proxmox/proxmox-ve_8.0-1.iso https://enterprise.proxmox.com/iso/proxmox-ve_8.0-1.iso
   ```

2. **Create bootable USB drive**

   - Use Balena Etcher or similar tool to flash the ISO to a USB drive
   - Boot the Protectli device from this USB drive

3. **Install Proxmox**

   - Follow the installation wizard
   - Configure static IP for management
   - Set up appropriate disk partitioning (ZFS recommended)
   - Complete installation and reboot

4. **Initial Proxmox configuration**
   - Access web interface at https://[PROXMOX-IP]:8006
   - Update system: `apt update && apt upgrade -y`
   - Configure networking for OPNsense VM

### Step 2: OPNsense VM Creation and Setup

1. **Download OPNsense ISO**

   ```bash
   mkdir -p ~/Downloads/opnsense
   curl -L -o ~/Downloads/opnsense/OPNsense-23.7-dvd-amd64.iso https://mirror.ams1.nl.leaseweb.net/opnsense/releases/23.7/OPNsense-23.7-dvd-amd64.iso
   ```

2. **Create VM in Proxmox**

   - Upload ISO to Proxmox storage
   - Create new VM with appropriate resources
   - Configure network interfaces (WAN, LAN, optional VLANs)
   - Install OPNsense from ISO

3. **Basic OPNsense Configuration**
   - Configure WAN and LAN interfaces
   - Set up basic firewall rules
   - Enable SSH access
   - Configure API access

### Step 3: Setup Management Scripts

1. **Create script directory structure**

   ```bash
   mkdir -p ~/Projects/homeserver-base/personal/opnsense-prod/{scripts,backups,configs/{interfaces,firewall,dhcp,dns,nat,vlans}}
   ```

2. **Implement core API scripts**

   - Create API authentication module
   - Implement configuration backup/restore
   - Build YAML parsing for configurations

3. **Test API connectivity**
   ```bash
   # Example test script
   cd ~/Projects/homeserver-base/personal/opnsense-prod
   python3 test_api.py
   ```

## Next Steps

1. **Complete Proxmox installation**

   - Install Proxmox on Protectli hardware
   - Configure network bridges
   - Update and optimize the system

2. **Deploy OPNsense VM**

   - Create and configure the VM
   - Install OPNsense
   - Perform initial network setup

3. **Implement configuration management**

   - Set up Python scripts for API interaction
   - Create configuration templates
   - Implement backup and restore functionality

4. **Develop advanced features**
   - VM snapshot integration
   - Automated testing
   - Alerting and monitoring

## Resources

- [Proxmox Installation Documentation](https://pve.proxmox.com/wiki/Installation)
- [OPNsense Documentation](https://docs.opnsense.org/)
- [OPNsense API Documentation](https://docs.opnsense.org/development/api.html)
- [OPNsense Configuration Backup & Restore](https://docs.opnsense.org/manual/backups.html)
- [Proxmox API Documentation](https://pve.proxmox.com/pve-docs/api-viewer/)
- [Python Requests Library](https://requests.readthedocs.io/)

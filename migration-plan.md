# PFSense to OPNsense Migration Plan

This document outlines the migration strategy from my current PFSense router to an OPNsense VM running on Proxmox on the Protectli Vault hardware.

## Current Environment

- **Router Hardware**: Protectli Vault 4 Port (Quad Core, AES-NI, 8GB RAM, 128GB SSD)
- **Router Software**: PFSense 23.3
- **Network Configuration**: Dual WAN with VLANs (10-13) for network segmentation
- **Compute Server**: Dell PowerEdge T40 running Proxmox

## Migration Goals

1. Replace PFSense with OPNsense for better API-driven management
2. Run OPNsense as a VM on Proxmox (on Protectli hardware)
3. Implement code-driven configuration approach
4. Create a unified Proxmox cluster with both T40 and Protectli nodes
5. Maintain all existing network functionality

## Pre-Migration Steps

### 1. Backup Current Configuration

```bash
# Download the PFSense configuration backup from the web UI
# Store in repository
cp config-backup.xml /Users/benfeely/Projects/homeserver-base/personal/backup/
```

### 2. Documentation

- Review and update network documentation with planned changes
- Extract all IP assignments, firewall rules, and port forwarding settings
- Document all DHCP reservations and static mappings

### 3. Preparation

- Download Proxmox VE ISO
- Prepare a USB installer for Proxmox
- Download OPNsense VM image

## Migration Procedure

### Phase 1: Proxmox Installation on Protectli

1. **Backup PFSense Configuration**
   - Create a complete backup from PFSense UI (Diagnostics > Backup & Restore)
   - Save backup file to a secure location

2. **Install Proxmox VE on Protectli**
   - Boot from USB installer
   - Install Proxmox VE 8.0 (or latest version)
   - Configure management network (temporary IP: 192.168.1.10)
   - Set hostname: `protectli.home.banjonet.com`
   - Complete initial setup

3. **Configure Proxmox Network**
   - Set up bridge for VM networking
   - Configure physical interfaces for passthrough

### Phase 2: OPNsense VM Creation

1. **Create OPNsense VM**
   - 2 vCPUs
   - 4GB RAM
   - 20GB disk
   - 4 network interfaces (WAN1, WAN2, LAN, Management)
   - Enable PCI passthrough for network interfaces

2. **Install OPNsense**
   - Download OPNsense image
   - Install using Proxmox web UI
   - Complete initial configuration
   - Enable API access

### Phase 3: Network Configuration Deployment

1. **Deploy Basic Configuration Script**
   - Run Python script for initial network setup
   - Configure interfaces, VLANs, and basic firewall rules
   - Establish management access

2. **Configure WAN Interfaces and Failover**
   - Set up TMobileWAN (Primary) on interface em0 with DHCP
   - Set up StarlinkWAN (Secondary) on interface em2 with DHCP
   - Configure gateway monitoring:
     - TMobileWAN monitored using 1.1.1.1 with 1-second interval
     - StarlinkWAN monitored using 8.8.8.8 with 1-second interval
     - Set down/up thresholds to 3 consecutive failures/successes
   - Create WAN_LoadBalance gateway group with:
     - TMobileWAN as priority 1 (primary)
     - StarlinkWAN as priority 2 (failover)
     - "downlosslatency" trigger type for comprehensive monitoring
   - Configure default gateway to use WAN_LoadBalance group

3. **Deploy Full Configuration**
   - Run comprehensive configuration script based on documentation
   - Configure DHCP, DNS, firewall rules, NAT, etc.
   - Validate configuration with tests

### Phase 4: Proxmox Clustering

1. **Create Cluster on T40**
   - Initialize Proxmox cluster on T40
   - Generate join token

2. **Join Protectli to Cluster**
   - Add Protectli node to existing cluster
   - Verify cluster status
   - Configure shared resources

3. **Configure Unified Management**
   - Set up management users and permissions
   - Configure backup strategy
   - Implement monitoring

## Testing Plan

1. **Connectivity Testing**
   - Verify internet access from all network segments
   - Test inter-VLAN routing per firewall rules
   - Validate DNS resolution

2. **Service Testing**
   - Verify all port forwarding rules
   - Test Tailscale exit node functionality
   - Validate access to all network services

3. **Performance Testing**
   - Measure throughput with iperf
   - Test dual WAN failover
   - Validate VPN performance

## Rollback Plan

If issues are encountered during migration:

1. **Quick Rollback**
   - Disconnect Protectli from network
   - Reconnect original PFSense router
   - Restore network connectivity

2. **Full Rollback**
   - Reinstall PFSense on Protectli if needed
   - Restore configuration from backup
   - Reconnect to network

## Post-Migration Tasks

1. **Documentation Update**
   - Update all network documentation to reflect new setup
   - Document API access details
   - Update IP planning document with new infrastructure

2. **Automation Implementation**
   - Refine automation scripts
   - Set up version control for configuration code
   - Implement configuration backup strategy

3. **Monitoring Setup**
   - Configure monitoring for OPNsense
   - Set up alerts for network issues
   - Implement logging and analysis

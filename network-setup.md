# Network & Router Setup

This document outlines my specific network configuration for the homeserver-base implementation, focusing on router setup and network organization.

## Router Configuration

I'm using a PFSense router for my network setup. PFSense is an open-source firewall/router software distribution based on FreeBSD.

### Router Backups

The repository contains router configuration backups in the `personal/backup/` directory. These backups were created using the PFSense router's backup operation through its web GUI and can be used to restore the router configuration if needed.

Current backups:
- `config-router.home.feelyfamily.com-20250602223603.xml` (June 2, 2025)

To restore a router configuration from backup, use the PFSense web interface's restore functionality under Diagnostics > Backup & Restore.

### Network Layout

*Document your network layout, IP ranges, VLANs, etc. here*

### Port Forwarding

*Document any port forwarding rules you've configured for your homeserver*

### DNS Configuration

*Document DNS settings, local domain names, etc.*

### Security Measures

*Document any specific security measures you've implemented at the network level*

## Network Connectivity

### Physical Connectivity

*Document how your server connects to the network (wired/wireless, NIC details, etc.)*

### Network Performance

*Document any network performance considerations or optimizations*

## Remote Access

*Document how you access your homeserver remotely, if applicable*

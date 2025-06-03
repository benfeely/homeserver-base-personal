# Network & Router Setup

This document outlines my specific network configuration for the homeserver-base implementation, focusing on router setup and network organization.

## Router Configuration

I'm using a PFSense router (version 23.3) for my network setup. PFSense is an open-source firewall/router software distribution based on FreeBSD. The router hostname is "router" in the domain "home.feelyfamily.com".

### Router Backups

The repository contains router configuration backups in the `personal/backup/` directory. These backups were created using the PFSense router's backup operation through its web GUI and can be used to restore the router configuration if needed.

Current backups:
- `config-router.home.feelyfamily.com-20250602223603.xml` (June 2, 2025)

To restore a router configuration from backup, use the PFSense web interface's restore functionality under Diagnostics > Backup & Restore.

### Network Layout

My network is configured with dual WAN connections for redundancy:

- **Primary WAN (TMobileWAN)**: Connected to interface em0, configured with DHCP
- **Secondary WAN (StarlinkWAN)**: Connected to interface em2, configured with DHCP
- **LAN**: Connected to interface em1, using static IP 10.10.10.1/24

### DHCP Configuration

The DHCP server is enabled on the LAN interface with the following configuration:
- DHCP range: 10.10.10.10 - 10.10.10.245

### Port Forwarding

Several port forwarding rules are configured:

1. Redirect Tailscale HTTP traffic (port 80) coming in on the Tailscale interface (opt3) with destination IP 100.126.222.114 to the local HAProxy at 10.10.10.1:80

2. Forward HTTPS traffic (port 443) to the gaming PC at 10.10.10.10:3000 for builder.yaarns.com

3. Forward HTTP traffic (port 80) to the gaming PC at 10.10.10.10:3000 for builder.yaarns.com

### DNS Configuration

The router is configured with the following DNS servers:
- Primary: 1.1.1.1 (Cloudflare)
- Secondary: 1.0.0.1 (Cloudflare)
- Tertiary: 8.8.8.8 (Google)
- Quaternary: 8.8.4.4 (Google)

### Security Measures

The router is configured with:
- Automatic outbound NAT
- Default PFSense firewall rules 
- Timezone set to US/Pacific
- HTTPS web interface on port 443 with SSL certificate
- NAT reflection disabled
- Protection against bogon networks

## Network Connectivity

### Physical Connectivity

The homeserver (Dell PowerEdge T40) is connected to the network via a wired Ethernet connection to the LAN interface of the PFSense router. The server likely has a static IP address within the 10.10.10.0/24 subnet.

### Network Performance

*Document any network performance considerations or optimizations*

## Remote Access

Remote access to the network and homeserver is provided through:

1. PFSense web interface on port 443 (HTTPS)
2. Tailscale VPN for secure remote access to internal resources
   - Tailscale interface appears to be configured as opt3 in the router
   - IP address 100.126.222.114 appears to be a Tailscale IP

The Tailscale setup allows secure access to internal services from anywhere without requiring traditional port forwarding through the internet-facing WAN interfaces. All required Tailscale port forwarding rules are currently enabled.

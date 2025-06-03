# Network & Router Setup

This document outlines my specific network configuration for the homeserver-base implementation, focusing on router setup and network organization.

## Router Configuration

I'm using a PFSense router (version 23.3) for my network setup. PFSense is an open-source firewall/router software distribution based on FreeBSD. The router hostname is "router" in the domain "home.banjonet.com".

### Router Backups

The repository contains router configuration backups in the `personal/backup/` directory. These backups were created using the PFSense router's backup operation through its web GUI and can be used to restore the router configuration if needed.

Current backups:
- `config-router.home.feelyfamily.com-20250602223603.xml` (June 2, 2025)

Note: The backup filename still shows the old domain "home.feelyfamily.com" as it was generated before the domain change to "home.banjonet.com".

To restore a router configuration from backup, use the PFSense web interface's restore functionality under Diagnostics > Backup & Restore.

### Network Layout

My network is configured with dual WAN connections for redundancy:

- **Primary WAN (TMobileWAN)**: Connected to interface em0, configured with DHCP
- **Secondary WAN (StarlinkWAN)**: Connected to interface em2, configured with DHCP

I'm using VLANs to create logical separation between different network segments while using the same physical network infrastructure:

- **Physical LAN Interface**: Connected to interface em1
  - **VLAN 10 (Static Network)**: 10.10.10.0/24 - Infrastructure and services with static IPs
  - **VLAN 11 (Client Network)**: 10.10.11.0/24 - Regular client devices with DHCP
  - **VLAN 12 (Guest Network)**: 10.10.12.0/24 - Guest WiFi and temporary devices
  - **VLAN 13 (IoT Network)**: 10.10.13.0/24 - Smart home and IoT devices

The router (PFSense) acts as the gateway for each VLAN with the following IP addresses:
- Static Network Gateway: 10.10.10.1/24
- Client Network Gateway: 10.10.11.1/24
- Guest Network Gateway: 10.10.12.1/24
- IoT Network Gateway: 10.10.13.1/24

For a comprehensive breakdown of my IP address allocation strategy, subnet organization, and DHCP configuration, see the [IP Range Planning](ip-planning.md) document.

### WiFi Configuration

The TP-Link Omada SDN controller manages my wireless access points and extends the VLAN configuration to WiFi clients. I've configured multiple SSIDs, each mapped to a different VLAN:

| SSID (WiFi Name)      | VLAN/Network      | Purpose                                      |
|-----------------------|-------------------|----------------------------------------------|
| BanjoNet              | VLAN 11 (Client)  | Primary WiFi for personal devices            |
| BanjoNet-Guest        | VLAN 12 (Guest)   | Limited access network for visitors          |
| BanjoNet-IoT          | VLAN 13 (IoT)     | Isolated network for smart home devices      |

This configuration allows me to easily control which network a device joins based on the SSID it connects to, while using the same physical access points for all networks.

### DHCP Configuration

The DHCP server is enabled on multiple interfaces with the following configurations:
- **Client Network**: 10.10.11.10 - 10.10.11.249
- **Guest Network**: 10.10.12.10 - 10.10.12.245
- **IoT Network**: 10.10.13.10 - 10.10.13.245

Static IP assignments for infrastructure devices and services are managed through static DHCP reservations in the 10.10.10.0/24 subnet.

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

### Network Devices

#### Printer Configuration

I have an HP LaserJet M575 multifunction printer configured on the network:
- **IP Address**: 10.10.10.4 (Static Network)
- **DNS Name**: printer.home.banjonet.com
- **Capabilities**: Print, Scan, Copy, Fax
- **Connectivity**: Wired Ethernet connection to the managed switch

The printer is accessible from the Static Network and Client Network, but not from the Guest or IoT networks for security purposes. All print jobs are sent directly to the printer without a print server intermediary.

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
   - Apple TV (10.10.10.7) configured as an exit node

### Tailscale Exit Node Configuration

The Apple TV is configured as a Tailscale exit node, which provides the following benefits:

- **Secure Internet Access**: When traveling, I can route all my internet traffic through my home network
- **Access to LAN Resources**: Devices connected to Tailscale can access resources on my home network
- **IP Geolocation**: Services see my home IP address rather than my current location's IP
- **Ad-blocking**: Traffic routed through the exit node benefits from my network-wide ad-blocking

The exit node configuration requires:
1. Enabling the exit node feature in the Tailscale admin console
2. Configuring the Apple TV as an advertised exit node
3. Selecting the exit node on client devices when needed

The Tailscale setup allows secure access to internal services from anywhere without requiring traditional port forwarding through the internet-facing WAN interfaces. All required Tailscale port forwarding rules are currently enabled.

## Home Automation

### Hubitat Elevation C-8 Controllers

My home automation system is built around two Hubitat Elevation C-8 hubs for wider coverage and redundancy:

1. **Primary Hub (Home)**: 
   - Located in the main house
   - IP Address: 10.10.10.5 (Static Network)
   - DNS Name: hubitat-home.home.banjonet.com
   - Manages primary Z-Wave and Zigbee devices throughout the main residence

2. **Secondary Hub (Garage)**:
   - Located in the detached garage
   - IP Address: 10.10.10.6 (Static Network)
   - DNS Name: hubitat-garage.home.banjonet.com
   - Provides extended coverage for devices in and around the garage area
   - Serves as a backup for critical automations

Both hubs are on the Static Network (10.10.10.0/24) but need to communicate with devices on the IoT Network (10.10.13.0/24), which is facilitated through specific firewall rules as documented in the [IP Planning](ip-planning.md) document.

## Media Devices

### Apple TV

My Apple TV serves as both a media player and a Tailscale exit node:

- **IP Address**: 10.10.10.7 (Static Network)
- **DNS Name**: appletv.home.banjonet.com
- **Tailscale Role**: Exit node for the Tailnet
- **Location**: Living room

As a Tailscale exit node, the Apple TV allows devices connected to my Tailscale network to route their internet traffic through my home network. This is particularly useful when:

1. Accessing region-restricted content while traveling
2. Improving privacy on untrusted networks
3. Accessing my home network services from anywhere

The device is assigned a static IP on the main infrastructure subnet due to its critical role in the network architecture.

# IP Range Planning

This document outlines my approach to IP address allocation for the homeserver-base implementation, expanding on the general guidelines from the main project README.

## Network Address Plan

Based on the reference implementation in the homeserver-base project, I've adopted a consolidated approach to IP range allocation:

### Subnet Allocation

| Subnet             | CIDR Range        | VLAN ID | Purpose                                           | Notes                                      |
|--------------------|-------------------|---------|---------------------------------------------------|--------------------------------------------|
| Static Network     | 10.10.10.0/24     | 10      | Infrastructure devices and services with static IPs| All static IP assignments in one subnet    |
| Client Network     | 10.10.11.0/24     | 11      | Regular client devices with dynamic IPs           | DHCP-assigned addresses only               |
| Guest Network      | 10.10.12.0/24     | 12      | Guest WiFi and temporary devices                  | Isolated from main network                 |
| IoT Devices        | 10.10.13.0/24     | 13      | Smart home and IoT devices                        | Isolated with limited external access      |

### Static Network IP Allocation (10.10.10.0/24)

| IP Range           | Purpose                                           | DNS Pattern                       |
|--------------------|---------------------------------------------------|-----------------------------------|
| 10.10.10.1-99      | Infrastructure devices (routers, switches, etc.)  | device.home.banjonet.com          |
| 10.10.10.100-254   | Services (Kubernetes, VMs, etc.)                  | service.home.banjonet.com         |

### Client Network IP Allocation (10.10.11.0/24)

| IP Range           | Purpose                                           | DNS Pattern                       |
|--------------------|---------------------------------------------------|-----------------------------------|
| 10.10.11.10-249    | DHCP range for regular clients                    | hostname.home.banjonet.com        |

### Key Infrastructure IP Assignments (10.10.10.1-99)

| Device                    | IP Address      | DNS Name                    | Purpose                                |
|---------------------------|-----------------|-----------------------------|-----------------------------------------|
| PFSense Router            | 10.10.10.1      | router.home.banjonet.com    | Network gateway and firewall           |
| Omada SDN Controller      | 10.10.10.2      | omada.home.banjonet.com     | TP-Link Omada controller for mesh WiFi |
| HP LaserJet M575 Printer  | 10.10.10.4      | printer.home.banjonet.com   | Network multifunction printer          |
| Hubitat Elevation C-8 (Home) | 10.10.10.5   | hubitat-home.home.banjonet.com | Primary home automation hub         |
| Hubitat Elevation C-8 (Studio) | 10.10.10.6 | hubitat-studio.home.banjonet.com | Secondary home automation hub     |
| Apple TV                   | 10.10.10.7      | appletv.home.banjonet.com     | Media player and Tailscale exit node   |
| Omada AP (Family Room)    | 10.10.10.21     | ap-family.home.banjonet.com | EAP683 LR wireless access point        |
| Omada AP (Coat Closet)    | 10.10.10.22     | ap-coat.home.banjonet.com   | EAP225 wireless access point           |
| Omada AP (Primary Bedroom)| 10.10.10.23     | ap-bedroom.home.banjonet.com| EAP225 wireless access point           |
| Omada AP (Theater Closet) | 10.10.10.24     | ap-theater.home.banjonet.com| EAP225 wireless access point           |
| Omada AP (Studio)         | 10.10.10.25     | ap-studio.home.banjonet.com | EAP225 wireless access point           |
| Proxmox Host (T40)        | 10.10.10.10     | proxmox.home.banjonet.com   | Dell PowerEdge T40 running Proxmox     |
| Proxmox Host (Protectli)  | 10.10.10.11     | protectli.home.banjonet.com | Protectli Vault running Proxmox        |
| Mac Studio M3 Ultra       | 10.10.10.15     | studio.home.banjonet.com    | AI workstation with 512GB RAM          |
| RTX 4090 Workstation      | 10.10.10.16     | gpu.home.banjonet.com       | GPU compute node with RTX 4090         |

## DHCP Configuration

- **Static Reservations**: All infrastructure devices and services have DHCP reservations in PFSense
- **DHCP Ranges**:
  - Client Network: 10.10.11.10 - 10.10.11.249
  - Guest Network: 10.10.12.10 - 10.10.12.245
  - IoT Network: 10.10.13.10 - 10.10.13.245

## IP Management for Kubernetes Services

For Kubernetes services that need to be accessible outside the cluster, I'll configure MetalLB to assign IPs from the Services range (10.10.10.100-254). Important services will have DNS entries configured for convenient access according to the service numbering scheme defined below.



## DNS Configuration

DNS entries are configured in two places:
1. **Internal DNS**: PFSense DNS resolver for local resolution
2. **External DNS**: Cloudflare DNS for services that need external access

## Remote Access Strategy

For remote access, I'm using Tailscale which simplifies the setup by providing:
- Secure access to internal services without exposing ports to the internet
- MagicDNS for convenient naming
- Zero-config split tunneling

## Service Numbering Scheme (10.10.10.100-254)

To ensure consistency and easy memorization, services are organized by type in specific IP ranges:

| IP Range           | Service Type                                      | Examples                           |
|--------------------|---------------------------------------------------|-----------------------------------|
| 10.10.10.100-109   | Authentication & Security                         | AuthServer, VPN, Vault            |
| 10.10.10.110-119   | Core Infrastructure                               | DNS, DHCP, NTP                    |
| 10.10.10.120-129   | Storage & Backup                                  | NAS, Backup, Kopia                |
| 10.10.10.130-139   | Productivity                                      | Wiki, Paperless, Notes            |
| 10.10.10.140-149   | Media Services                                    | Plex, Jellyfin, Music             |
| 10.10.10.150-159   | Home Automation                                   | Home Assistant, Node-RED          |
| 10.10.10.160-169   | Monitoring & Management                           | Grafana, Prometheus, Uptime       |
| 10.10.10.170-179   | Development & Testing                             | Git, CI/CD, Dev Environments      |
| 10.10.10.180-189   | AI & Machine Learning                             | TensorFlow, LLM Hosting           |
| 10.10.10.190-199   | Miscellaneous & Experimental                      | Test services, Temporary          |
| 10.10.10.200-254   | Reserved for future service expansion             | Additional services as needed     |

### Specific Service Allocations

| Service                   | IP Address      | DNS Name                        | Purpose                           |
|---------------------------|-----------------|--------------------------------|-----------------------------------|
| Vault                     | 10.10.10.100    | vault.home.banjonet.com        | Secret management                  |
| Tailscale                 | 10.10.10.101    | vpn.home.banjonet.com          | VPN service                        |
| PiHole                    | 10.10.10.110    | dns.home.banjonet.com          | DNS and ad blocking                |
| NAS                       | 10.10.10.120    | nas.home.banjonet.com          | Network storage                    |
| Kopia                     | 10.10.10.121    | backup.home.banjonet.com       | Backup system                      |
| Wiki.js                   | 10.10.10.130    | wiki.home.banjonet.com         | Knowledge base                     |
| Paperless-NGX             | 10.10.10.131    | paperless.home.banjonet.com    | Document management                |
| Plex                      | 10.10.10.140    | plex.home.banjonet.com         | Media server                       |
| Home Assistant            | 10.10.10.150    | homeassistant.home.banjonet.com| Home automation controller         |
| Node-RED                  | 10.10.10.151    | nodered.home.banjonet.com      | Automation workflows               |
| Grafana                   | 10.10.10.160    | grafana.home.banjonet.com      | Monitoring dashboards              |
| Prometheus                | 10.10.10.161    | prometheus.home.banjonet.com   | Metrics collection                 |
| Git Server                | 10.10.10.170    | git.home.banjonet.com          | Local git repository               |
| LLM Server                | 10.10.10.180    | llm.home.banjonet.com          | Local LLM hosting                  |

## IoT Network Firewall Rules

The IoT network (10.10.13.0/24) is isolated with specific firewall rules to prevent IoT devices from accessing sensitive networks while allowing necessary functionality. 

### IoT Devices

| Device                  | IP Address      | DNS Name                          | Purpose                         |
|-------------------------|-----------------|-----------------------------------|----------------------------------|
| Eufy Homebase E Hub     | 10.10.13.30     | eufyhub.iot.banjonet.com          | Central hub for Eufy cameras    |
| Eufy Camera 1           | DHCP            | camera-location1.iot.banjonet.com | Security camera                 |
| Eufy Camera 2           | DHCP            | camera-location2.iot.banjonet.com | Security camera                 |

### Outbound Rules

| Rule # | Source             | Destination        | Port/Protocol      | Action | Purpose                                |
|--------|--------------------|--------------------|--------------------|---------|-----------------------------------------|
| 1      | IoT (10.10.13.0/24)| External Internet  | 80,443/TCP         | Allow  | HTTP/HTTPS for updates and API access   |
| 2      | IoT (10.10.13.0/24)| External Internet  | 53/UDP,TCP         | Allow  | DNS resolution                          |
| 3      | IoT (10.10.13.0/24)| External Internet  | 123/UDP            | Allow  | NTP for time synchronization            |
| 4      | IoT (10.10.13.0/24)| Hubitat Hubs       | 80,443/TCP         | Allow  | Connect to Hubitat controllers          |
| 5      | Eufy Hub (10.10.13.30) | External Internet | 8554/TCP        | Allow  | RTSP streaming for cameras              |
| 6      | Eufy Hub (10.10.13.30) | External Internet | UDP 3478-3497   | Allow  | STUN/TURN for P2P connections          |
| 7      | IoT (10.10.13.0/24)| Any                | Any                | Block  | Block all other traffic                 |

### Inbound Rules

| Rule # | Source             | Destination        | Port/Protocol      | Action | Purpose                                |
|--------|--------------------|--------------------|--------------------|---------|-----------------------------------------|
| 1      | Hubitat Hubs       | IoT (10.10.13.0/24)| Device-specific    | Allow  | Hubitat control of IoT devices         |
| 2      | Static Network     | IoT (10.10.13.0/24)| ICMP               | Allow  | Allow ping for troubleshooting          |
| 3      | Client Network     | Eufy Hub (10.10.13.30) | 8554/TCP      | Allow  | Local RTSP access for viewing streams  |
| 4      | Client Network     | Eufy Hub (10.10.13.30) | 443/TCP       | Allow  | Local web access to hub                |
| 5      | Hubitat Hubs (10.10.10.5-6) | Eufy Hub (10.10.13.30) | 8554,443/TCP | Allow | Integration with home automation |
| 6      | Any                | IoT (10.10.13.0/24)| Any                | Block  | Block all other traffic                 |

## Guest Network Firewall Rules

The Guest network (10.10.12.0/24) is isolated to protect the main network while providing internet access to visitors.

### Outbound Rules

| Rule # | Source               | Destination        | Port/Protocol      | Action | Purpose                                |
|--------|----------------------|--------------------|--------------------|---------|-----------------------------------------|
| 1      | Guest (10.10.12.0/24)| External Internet  | 80,443/TCP         | Allow  | HTTP/HTTPS for web browsing            |
| 2      | Guest (10.10.12.0/24)| External Internet  | 53/UDP,TCP         | Allow  | DNS resolution                          |
| 3      | Guest (10.10.12.0/24)| External Internet  | Any                | Allow  | General internet access                 |
| 4      | Guest (10.10.12.0/24)| Static Network     | Any                | Block  | Prevent access to infrastructure        |
| 5      | Guest (10.10.12.0/24)| Client Network     | Any                | Block  | Prevent access to personal devices      |
| 6      | Guest (10.10.12.0/24)| IoT Network        | Any                | Block  | Prevent access to IoT devices           |

### Inbound Rules

| Rule # | Source               | Destination          | Port/Protocol      | Action | Purpose                                |
|--------|----------------------|----------------------|--------------------|---------|-----------------------------------------|
| 1      | Static Network       | Guest (10.10.12.0/24)| ICMP               | Allow  | Allow ping for troubleshooting          |
| 2      | Any                  | Guest (10.10.12.0/24)| Any                | Block  | Block all other traffic                 |

## DNS Naming Conventions

To ensure consistency across all services and devices, the following DNS naming conventions are used:

1. **Infrastructure Devices**: `device-name.home.banjonet.com`
   - Example: `router.home.banjonet.com`, `proxmox.home.banjonet.com`

2. **Services**: `service-name.home.banjonet.com`
   - Example: `plex.home.banjonet.com`, `wiki.home.banjonet.com`

3. **Workstations & Clients**: `hostname.home.banjonet.com`
   - Example: `desktop.home.banjonet.com`, `laptop.home.banjonet.com`

4. **IoT Devices**: `device-location.iot.banjonet.com`
   - Example: `thermostat-living.iot.banjonet.com`, `light-kitchen.iot.banjonet.com`

5. **Guest Network**: No DNS names provided for guest devices

## Implementation Notes

- Unlike the main project which uses 192.168.x.x ranges, I've chosen to use 10.10.x.x ranges for better compatibility with various networks I might connect to remotely
- My IoT network is completely isolated with specific firewall rules to prevent IoT devices from accessing the main network
- I've expanded the number of subnets compared to the reference implementation to better isolate different types of devices
- **Separation of Static and Dynamic IPs**: By using 10.10.10.0/24 exclusively for static IPs and 10.10.11.0/24 for DHCP clients, I've created a clean separation that makes network management easier:
  - Simpler mental model (10.10.10.x = infrastructure/services, 10.10.11.x = clients)
  - More efficient firewall and access control rules
  - Easier troubleshooting as the IP address immediately indicates the device type
  - More room for future static assignments (the entire 10.10.10.0/24 range)
- **VLAN Implementation**: All subnets are implemented as VLANs over the same physical network infrastructure:
  - Single physical LAN port on the router connected to a managed switch
  - Switch handles VLAN tagging and forwarding
  - Access points broadcast different SSIDs tagged with the appropriate VLAN
  - This approach eliminates the need for multiple physical network interfaces while maintaining logical separation
- **Eufy Security System**: The Eufy Homebase E Hub is placed in the IoT network for security isolation:
  - Assigned a static IP (10.10.13.30) for consistent access
  - Specific firewall rules allow necessary connectivity while maintaining isolation
  - Local storage and RTSP streaming are enabled to keep video data on-premises
  - Integration with Hubitat automation hubs is facilitated through targeted firewall rules

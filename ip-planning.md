# IP Range Planning

This document outlines my approach to IP address allocation for the homeserver-base implementation, expanding on the general guidelines from the main project README.

## Network Address Plan

Based on the reference implementation in the homeserver-base project, I've adopted a similar but customized approach to IP range allocation:

### Subnet Allocation

| Subnet             | CIDR Range        | Purpose                                           | Notes                                      |
|--------------------|-------------------|---------------------------------------------------|--------------------------------------------|
| Main Network       | 10.10.10.0/24     | Primary home network for regular devices          | Managed by PFSense DHCP (10.10.10.10-245)  |
| Services           | 10.10.11.0/24     | Reserved for K8s services via MetalLB             | Manually configured DNS entries as needed  |
| Infrastructure     | 10.10.12.0/24     | Infrastructure devices (NAS, servers, etc.)       | Static IPs or long DHCP leases             |
| IoT Devices        | 10.10.13.0/24     | Smart home and IoT devices                        | Isolated with limited external access      |
| Guest Network      | 10.10.14.0/24     | Guest WiFi and temporary devices                  | Isolated from main network                 |

### Key IP Assignments

| Device/Service            | IP Address      | DNS Name                  | Purpose                                |
|---------------------------|-----------------|---------------------------|----------------------------------------|
| PFSense Router            | 10.10.10.1      | router.home.banjonet.com  | Network gateway and firewall           |
| Omada SDN Controller      | 10.10.10.2      | omada.home.banjonet.com   | TP-Link Omada controller for mesh WiFi |
| Mac Studio M3 Ultra       | 10.10.12.5      | studio.home.banjonet.com  | AI workstation with 512GB RAM - primary AI model host |
| RTX 4090 Workstation      | 10.10.12.6      | gpu.home.banjonet.com     | GPU compute node with RTX 4090 - ML acceleration |
| Proxmox Host (T40)        | 10.10.12.1      | proxmox.home.banjonet.com | Dell PowerEdge T40 running Proxmox     |
| Kubernetes Control Plane  | 10.10.12.10     | k8s.home.banjonet.com     | Talos-based Kubernetes control plane   |

## DHCP Configuration

- **Static Reservations**: All infrastructure devices have DHCP reservations in PFSense to ensure consistent addressing
- **DHCP Ranges**:
  - Main Network: 10.10.10.10 - 10.10.10.245
  - IoT Network: 10.10.13.10 - 10.10.13.245
  - Guest Network: 10.10.14.10 - 10.10.14.245

## IP Management for Kubernetes Services

For Kubernetes services that need to be accessible outside the cluster, I'll configure MetalLB to assign IPs from the Services subnet (10.10.11.0/24). Important services will have DNS entries configured for convenient access.

### Example Service Allocations

| Service                   | IP Address      | DNS Name                        |
|---------------------------|-----------------|--------------------------------|
| Traefik Ingress           | 10.10.11.2      | traefik.home.banjonet.com   |
| Paperless-NGX             | 10.10.11.10     | paperless.home.banjonet.com |
| Kopia Backup              | 10.10.11.11     | backup.home.banjonet.com    |
| Wiki.js                   | 10.10.11.12     | wiki.home.banjonet.com      |

## DNS Configuration

DNS entries are configured in two places:
1. **Internal DNS**: PFSense DNS resolver for local resolution
2. **External DNS**: Cloudflare DNS for services that need external access

## Remote Access Strategy

For remote access, I'm using Tailscale which simplifies the setup by providing:
- Secure access to internal services without exposing ports to the internet
- MagicDNS for convenient naming
- Zero-config split tunneling

## Implementation Notes

- Unlike the main project which uses 192.168.x.x ranges, I've chosen to use 10.10.x.x ranges for better compatibility with various networks I might connect to remotely
- My IoT network is completely isolated with specific firewall rules to prevent IoT devices from accessing the main network
- I've expanded the number of subnets compared to the reference implementation to better isolate different types of devices

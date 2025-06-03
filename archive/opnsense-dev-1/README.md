# OPNsense Development Environment

This directory contains a Docker-based development environment for OPNsense. It allows you to run OPNsense in a container for testing and development purposes before deploying to the production Proxmox VM.

## Network Structure

The environment sets up three Docker networks to simulate a typical network configuration:

- **WAN Network**: 192.168.100.0/24 - Simulates the external internet connection
- **LAN Network**: 192.168.1.0/24 - Simulates the internal primary network
- **Management Network**: 192.168.2.0/24 - Dedicated network for management functions

## Getting Started

### Prerequisites

- Docker Desktop installed and running
- Docker Compose installed

### Starting the Environment

```bash
cd /Users/benfeely/Projects/homeserver-base/personal/opnsense-dev
docker-compose up -d
```

### Accessing OPNsense

- **Web UI**: https://localhost:8443 or http://localhost:8080 (redirects to HTTPS)
  - Default credentials: root / opnsense (you should change these)
- **SSH**: ssh -p 2222 root@localhost

### Stopping the Environment

```bash
docker-compose down
```

### Data Persistence

Configuration data is stored in the following directories:

- `./conf`: OPNsense configuration
- `./etc`: System configuration files
- `./var`: Variable data

These directories are mounted as volumes to ensure your configuration persists between container restarts.

## Testing the API

Once OPNsense is running, you need to:

1. Enable the API in the OPNsense web UI:
   - Navigate to System > Settings > Administration
   - Enable the API (legacy)

2. Create API credentials:
   - Go to System > Access > Users
   - Add an API key for your automation user

3. Test the API connection using curl:

```bash
curl -k -u "<key>:<secret>" https://localhost/api/core/firmware/status
```

## Simulating Clients

You can create additional Docker containers to connect to the different networks to simulate clients:

```yaml
# Add to docker-compose.yml
services:
  lan-client:
    image: alpine
    networks:
      lan: {}
    command: tail -f /dev/null
```

This client can then be used to test network connectivity, firewall rules, etc.

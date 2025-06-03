# Tasks & Future Improvements

This document tracks ongoing tasks, improvements, and discussions for the homeserver implementation.

## High Priority

### Reverse Proxy Implementation

- **Task**: Research and implement a reverse proxy solution running on the T40 Proxmox host
- **Status**: Not started
- **Due Date**: TBD
- **Description**: 
  The homeserver-base repository includes Traefik as part of its core infrastructure for ingress. Need to investigate how to best implement a reverse proxy setup that will work with the existing configuration while providing the desired functionality.

### Research Items
- [ ] Evaluate Traefik vs. Nginx vs. HAProxy options
- [ ] Determine whether to run as a container in Kubernetes or as a standalone VM
- [ ] Plan integration with existing Tailscale setup
- [ ] Consider SSL certificate management with Let's Encrypt
- [ ] Document firewall rule requirements for the proxy

### Integration Requirements
- [ ] Access to both WAN interfaces
- [ ] Integration with existing DNS (internal and external)
- [ ] Support for services across different networks (Static, IoT)
- [ ] Path-based and host-based routing

### Reference Information
- The homeserver-base project uses Traefik as part of its core infrastructure
- MetalLB is used for load balancing in the bare metal setup
- Current network setup has the router at 10.10.10.1 with dual WAN connections

## Medium Priority

### Static IP Assignments in Omada Controller
- **Task**: Implement static IP assignments for all access points in the Omada controller
- **Status**: Not started
- **Due Date**: TBD

### Create OPNsense Configuration Scripts
- **Task**: Develop initial Python scripts for OPNsense configuration management
- **Status**: Not started
- **Due Date**: TBD

## Low Priority

### Implement Monitoring for Network Infrastructure
- **Task**: Set up monitoring for router, switch, and access points
- **Status**: Not started
- **Due Date**: TBD

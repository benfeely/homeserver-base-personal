# UTM Network Configuration for OPNsense

This document provides detailed instructions for configuring network interfaces in UTM for your OPNsense development environment.

## Network Interface Types in UTM

UTM provides several types of network interfaces that you can use with your OPNsense VM:

1. **Shared Network**: 
   - Uses your Mac's network connection to provide internet access
   - Operates in NAT mode
   - Good choice for the WAN interface

2. **Host-only Network**:
   - Creates a private network between your Mac and the VM
   - No internet access by default
   - Good choice for LAN and management networks

3. **Bridge Network**:
   - Connects directly to your Mac's physical network interfaces
   - Requires admin privileges
   - Useful for advanced configurations

## Recommended Network Setup

### Basic Setup (Minimum Required)

1. **WAN Interface**: Shared Network
   - Provides internet connectivity
   - Will be assigned via DHCP from your Mac

2. **LAN Interface**: Host-only Network
   - Configured with a static IP (192.168.1.1/24)
   - Used for management access from your Mac

### Advanced Setup (Optional)

3. **OPT1 Interface**: Host-only Network
   - Configured as 192.168.2.1/24
   - Can be used to simulate your "Client Network"

4. **OPT2 Interface**: Host-only Network
   - Configured as 192.168.3.1/24
   - Can be used to simulate your "IoT Network"

## UTM Network Configuration Steps

### Creating Host-only Networks

1. Open UTM Preferences (⌘,)
2. Go to the "Network" tab
3. Click "+" to add a new network
4. Configure as follows:
   - Name: OPNsense-LAN
   - Interface Type: Host-only
   - IP Configuration: 192.168.1.2/24 (for your Mac)
5. Click "Save"
6. Repeat to create additional networks as needed

### Assigning Networks to the VM

1. Right-click on your OPNsense VM and select "Edit"
2. Go to the "Network" tab
3. Configure each interface:
   - Interface 0: Shared Network (WAN)
   - Interface 1: Host-only Network → OPNsense-LAN
   - Add more interfaces as needed for your simulation
4. Click "Save"

## Accessing the OPNsense Web Interface

After configuring the networks and installing OPNsense:

1. Ensure your Mac is connected to the Host-only network
2. Open a web browser and navigate to https://192.168.1.1
3. Accept the self-signed certificate warning
4. Log in with your credentials (default: root/opnsense)

## Connecting Your Mac to Multiple Host-only Networks

If you're using multiple Host-only networks, you'll need to configure your Mac to access each one:

1. Open System Preferences > Network
2. You should see new network interfaces for each Host-only network
3. Configure each with appropriate static IPs:
   - OPNsense-LAN: 192.168.1.2/24
   - OPNsense-Client: 192.168.2.2/24
   - OPNsense-IoT: 192.168.3.2/24

## Simulating Internet Connectivity Issues

To test WAN failover or other internet connectivity scenarios:

1. Edit your VM while it's running
2. Go to the "Network" tab
3. Disable the WAN interface by unchecking it
4. Click "Save" to simulate internet loss

## Tips for Performance

- Allocate at least 2GB of RAM to the OPNsense VM
- Assign at least 2 CPU cores for better performance
- Use hardware acceleration if available
- Keep VM snapshots before major configuration changes

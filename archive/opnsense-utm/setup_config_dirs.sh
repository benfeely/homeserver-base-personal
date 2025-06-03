#!/bin/zsh
# filepath: /Users/benfeely/Projects/homeserver-base/personal/opnsense-utm/setup_config_dirs.sh
# Script to set up directories for storing OPNsense configurations

# Base directories
CONFIG_DIR="./configs"
FIREWALL_DIR="$CONFIG_DIR/firewall"
SYSTEM_DIR="$CONFIG_DIR/system"
NETWORK_DIR="$CONFIG_DIR/network"
VPN_DIR="$CONFIG_DIR/vpn"
DHCP_DIR="$CONFIG_DIR/dhcp"
DNS_DIR="$CONFIG_DIR/dns"

# Create the directory structure
mkdir -p "$FIREWALL_DIR/rules"
mkdir -p "$FIREWALL_DIR/aliases"
mkdir -p "$FIREWALL_DIR/nat"
mkdir -p "$SYSTEM_DIR/general"
mkdir -p "$SYSTEM_DIR/users"
mkdir -p "$NETWORK_DIR/interfaces"
mkdir -p "$NETWORK_DIR/routing"
mkdir -p "$VPN_DIR/wireguard"
mkdir -p "$VPN_DIR/openvpn"
mkdir -p "$DHCP_DIR/ipv4"
mkdir -p "$DHCP_DIR/ipv6"
mkdir -p "$DNS_DIR/dnsmasq"
mkdir -p "$DNS_DIR/unbound"

# Create README files for each directory
cat > "$CONFIG_DIR/README.md" << EOL
# OPNsense Configurations

This directory contains configuration files for OPNsense, organized by feature.
Each subdirectory contains specific configurations that can be applied to the OPNsense instance.
EOL

cat > "$FIREWALL_DIR/README.md" << EOL
# Firewall Configurations

This directory contains firewall-related configurations:
- rules: Firewall rules for different interfaces
- aliases: IP, port, and URL aliases
- nat: Network Address Translation rules
EOL

cat > "$SYSTEM_DIR/README.md" << EOL
# System Configurations

This directory contains system-related configurations:
- general: General system settings
- users: User and group configurations
EOL

cat > "$NETWORK_DIR/README.md" << EOL
# Network Configurations

This directory contains network-related configurations:
- interfaces: Interface settings (LAN, WAN, etc.)
- routing: Static routes and gateways
EOL

cat > "$VPN_DIR/README.md" << EOL
# VPN Configurations

This directory contains VPN-related configurations:
- wireguard: WireGuard VPN settings
- openvpn: OpenVPN client and server configurations
EOL

cat > "$DHCP_DIR/README.md" << EOL
# DHCP Configurations

This directory contains DHCP-related configurations:
- ipv4: DHCPv4 settings
- ipv6: DHCPv6 settings
EOL

cat > "$DNS_DIR/README.md" << EOL
# DNS Configurations

This directory contains DNS-related configurations:
- dnsmasq: DNSMasq settings
- unbound: Unbound settings
EOL

echo "Configuration directory structure created successfully!"
echo "You can now store your OPNsense configurations in the appropriate directories."

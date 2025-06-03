# Infrastructure as Code for Network Management

This document outlines my approach to managing network infrastructure using code-driven automation, focusing on the OPNsense router running on Proxmox.

## Philosophy

All network infrastructure changes are implemented through code rather than manual UI interactions. This ensures:

- Reproducibility of configurations
- Version control for all changes
- Ability to test changes in isolation
- Documentation of infrastructure in code
- AI-assisted management and troubleshooting

## Code Repository Structure

```
network-automation/
├── README.md
├── scripts/
│   ├── setup.py            # Initial configuration script
│   ├── interfaces.py       # Network interface management
│   ├── vlans.py            # VLAN configuration
│   ├── firewall.py         # Firewall rules management
│   ├── dhcp.py             # DHCP server configuration
│   ├── dns.py              # DNS configuration
│   ├── diagnostics.py      # Network diagnostics tools
│   └── utils/
│       ├── __init__.py
│       ├── api.py          # API interaction utilities
│       ├── logging.py      # Logging configuration
│       └── validators.py   # Configuration validation
├── config/
│   ├── interfaces.yaml     # Interface configuration
│   ├── vlans.yaml          # VLAN definitions
│   ├── firewall.yaml       # Firewall rule definitions
│   ├── dhcp.yaml           # DHCP server settings
│   ├── dns.yaml            # DNS configuration
│   └── devices.yaml        # Device registry
├── services/
│   ├── eufy/               # Eufy security integration
│   │   ├── firewall.yaml   # Eufy-specific firewall rules
│   │   └── setup.py        # Eufy network setup
│   └── proxmox/            # Proxmox management scripts
│       ├── cluster.py      # Cluster management
│       └── vm.py           # VM management
└── tests/
    ├── test_interfaces.py
    ├── test_vlans.py
    ├── test_firewall.py
    └── test_integration.py
```

## OPNsense API Setup

### Initial API Configuration

1. Enable the OPNsense API in the web UI:
   - System > Settings > Administration
   - Enable API (legacy)

2. Create API credentials:
   - System > Access > Users
   - Add API key for automation user
   - Save credentials securely

3. Configure API credentials in environment:
   ```bash
   export OPNSENSE_API_KEY="your_api_key"
   export OPNSENSE_API_SECRET="your_api_secret"
   export OPNSENSE_URL="https://10.10.10.1"
   ```

### API Authentication

```python
import requests
import os
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# API Configuration from environment
OPNSENSE_URL = os.environ.get("OPNSENSE_URL", "https://10.10.10.1")
API_KEY = os.environ.get("OPNSENSE_API_KEY")
API_SECRET = os.environ.get("OPNSENSE_API_SECRET")

# Create session with authentication
session = requests.Session()
session.auth = (API_KEY, API_SECRET)
session.verify = False  # For self-signed certificates
```

## Core Automation Scripts

### Base API Interaction

```python
def api_call(method, endpoint, data=None):
    """Make API call to OPNsense"""
    url = f"{OPNSENSE_URL}/api/{endpoint}"
    
    try:
        if method == "GET":
            response = session.get(url, timeout=10)
        elif method == "POST":
            response = session.post(url, json=data, timeout=10)
        
        # Raise exception for HTTP errors
        response.raise_for_status()
        
        return response.json() if response.text else {}
    
    except requests.exceptions.HTTPError as err:
        error_msg = f"HTTP Error: {err}"
        try:
            error_details = response.json()
            print(f"Error {response.status_code}: {json.dumps(error_details)}")
            print(f"Endpoint: {endpoint}, Data: {json.dumps(data)}")
        except:
            print(f"Error {response.status_code}: {response.text}")
        
        return None
    
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return None
```

### Configuration Loading

```python
import yaml

def load_config(config_file):
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config file {config_file}: {str(e)}")
        return None
```

## Deployment Workflow

### 1. Configuration Definition

Network configurations are defined in YAML files that are human-readable and easily edited:

```yaml
# Example: vlans.yaml
vlans:
  - id: 10
    interface: em1
    description: "Static Network"
    priority: 0
  - id: 11
    interface: em1
    description: "Client Network"
    priority: 0
  - id: 12
    interface: em1
    description: "Guest Network"
    priority: 0
  - id: 13
    interface: em1
    description: "IoT Network"
    priority: 0
```

### 2. Configuration Deployment

Scripts read the configuration files and apply them to OPNsense using the API:

```python
def deploy_vlans():
    """Deploy VLAN configuration to OPNsense"""
    config = load_config('config/vlans.yaml')
    if not config:
        return False
    
    for vlan in config['vlans']:
        vlan_data = {
            "vlan": {
                "vlanif": vlan['interface'],
                "tag": vlan['id'],
                "descr": vlan['description'],
                "prio": vlan['priority']
            }
        }
        
        result = api_call("POST", "interfaces/vlan/addItem", vlan_data)
        if not result:
            print(f"Failed to create VLAN {vlan['id']}")
            return False
    
    return True
```

### 3. Validation

After deployment, scripts validate that the configuration was applied correctly:

```python
def validate_vlans():
    """Validate VLAN configuration in OPNsense"""
    config = load_config('config/vlans.yaml')
    if not config:
        return False
    
    # Get current VLANs from OPNsense
    result = api_call("GET", "interfaces/vlan/getItems")
    if not result:
        return False
    
    current_vlans = result.get('rows', [])
    
    # Check that each configured VLAN exists
    for vlan in config['vlans']:
        found = False
        for current in current_vlans:
            if (current['vlanif'] == vlan['interface'] and 
                int(current['tag']) == vlan['id']):
                found = True
                break
        
        if not found:
            print(f"VLAN {vlan['id']} not found in current configuration")
            return False
    
    return True
```

## Error Handling and Logging

All scripts implement comprehensive error handling and logging:

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('network-automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('network-automation')

# Example usage
try:
    logger.info("Deploying VLAN configuration")
    if deploy_vlans():
        logger.info("VLAN deployment successful")
    else:
        logger.error("VLAN deployment failed")
except Exception as e:
    logger.exception(f"Unexpected error during VLAN deployment: {str(e)}")
```

## Backup Strategy

Regular backups of OPNsense configuration are automated:

```python
def backup_configuration():
    """Create and download OPNsense configuration backup"""
    import datetime
    
    # Create backup through API
    result = api_call("POST", "system/backup/backup")
    if not result:
        return False
    
    # Download backup file
    backup_file = result.get('filename')
    if not backup_file:
        return False
    
    # Format timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Download the backup file
    response = session.get(f"{OPNSENSE_URL}/system/backup/download/{backup_file}")
    
    # Save to file
    with open(f"backups/config-{timestamp}.xml", 'wb') as f:
        f.write(response.content)
    
    return True
```

## Automated Testing

Infrastructure changes are tested before deployment to production:

```python
def test_firewall_rules():
    """Test firewall rules before deployment"""
    import subprocess
    
    # Deploy to test environment first
    deploy_firewall_rules(environment='test')
    
    # Test connectivity through firewall
    test_results = []
    
    # Test internal network connectivity
    test_results.append(subprocess.run(
        ["ping", "-c", "3", "10.10.10.1"],
        capture_output=True
    ).returncode == 0)
    
    # Test internet connectivity
    test_results.append(subprocess.run(
        ["ping", "-c", "3", "1.1.1.1"],
        capture_output=True
    ).returncode == 0)
    
    # Return True only if all tests pass
    return all(test_results)
```

## DNS Management

The DNS configuration is managed through code, allowing for consistent naming conventions across all networks:

```python
def configure_dns_entries():
    """Configure DNS entries for infrastructure and services"""
    # Load DNS configuration
    config = load_config('config/dns.yaml')
    if not config:
        return False
    
    for entry in config['entries']:
        # Format data for OPNsense API
        dns_data = {
            "host": entry['hostname'],
            "domain": entry['domain'],
            "rr": "A",  # A record
            "ip": entry['ip_address'],
            "descr": entry.get('description', '')
        }
        
        # Add DNS entry
        result = api_call("POST", "unbound/dnsbl/addHostOverride", dns_data)
        if not result:
            logger.error(f"Failed to add DNS entry for {entry['hostname']}.{entry['domain']}")
            return False
    
    # Apply changes
    api_call("POST", "unbound/service/reconfigure")
    
    return True
```

Example DNS configuration (YAML):

```yaml
# Example: dns.yaml
entries:
  # Infrastructure devices
  - hostname: router
    domain: home.banjonet.com
    ip_address: 10.10.10.1
    description: "OPNsense Router"
    
  - hostname: omada
    domain: home.banjonet.com
    ip_address: 10.10.10.2
    description: "Omada SDN Controller"
    
  # IoT devices  
  - hostname: eufyhub
    domain: iot.banjonet.com
    ip_address: 10.10.13.30
    description: "Eufy Homebase E Hub"
    
  - hostname: camera-front
    domain: iot.banjonet.com
    ip_address: 10.10.13.31
    description: "Eufy Front Door Camera"
```

## Eufy Security System Integration

The Eufy security system requires specific firewall rules and DNS configuration. These are managed through dedicated scripts:

```python
def configure_eufy_system():
    """Configure network settings for Eufy security system"""
    # Load Eufy configuration
    config = load_config('services/eufy/firewall.yaml')
    if not config:
        return False
    
    # Configure firewall rules for Eufy Hub
    for rule in config['firewall_rules']:
        firewall_data = {
            "rule": {
                "type": rule['type'],
                "interface": rule['interface'],
                "ipprotocol": rule['ip_protocol'],
                "protocol": rule['protocol'],
                "source_net": rule['source'],
                "destination_net": rule['destination'],
                "destination_port": rule.get('destination_port', ''),
                "description": rule['description'],
                "enabled": "1"
            }
        }
        
        result = api_call("POST", "firewall/filter/addRule", firewall_data)
        if not result:
            logger.error(f"Failed to add firewall rule: {rule['description']}")
            return False
    
    # Apply changes
    api_call("POST", "firewall/filter/apply")
    
    # Configure static DHCP reservation for Eufy Hub
    dhcp_data = {
        "dhcpd": {
            "staticmap": {
                "mac": config['eufy_hub']['mac_address'],
                "ipaddr": config['eufy_hub']['ip_address'],
                "hostname": "eufyhub",
                "descr": "Eufy Homebase E Hub",
                "domain": "iot.banjonet.com"
            }
        }
    }
    
    result = api_call("POST", "dhcp/staticmap/addStaticMap", dhcp_data)
    if not result:
        logger.error("Failed to add static DHCP reservation for Eufy Hub")
        return False
    
    # Add DNS entry for Eufy Hub
    dns_data = {
        "host": "eufyhub",
        "domain": "iot.banjonet.com",
        "rr": "A",
        "ip": config['eufy_hub']['ip_address'],
        "descr": "Eufy Homebase E Hub"
    }
    
    result = api_call("POST", "unbound/dnsbl/addHostOverride", dns_data)
    if not result:
        logger.error("Failed to add DNS entry for Eufy Hub")
        return False
    
    # Apply changes
    api_call("POST", "dhcp/service/reconfigure")
    api_call("POST", "unbound/service/reconfigure")
    
    return True
```

Example Eufy configuration (YAML):

```yaml
# services/eufy/firewall.yaml
eufy_hub:
  mac_address: "AA:BB:CC:DD:EE:FF"
  ip_address: "10.10.13.30"

firewall_rules:
  - type: "pass"
    interface: "LAN"
    ip_protocol: "inet"
    protocol: "TCP"
    source: "10.10.13.30"
    destination: "any"
    destination_port: "8554"
    description: "Allow RTSP streaming from Eufy Hub"
    
  - type: "pass"
    interface: "LAN"
    ip_protocol: "inet"
    protocol: "UDP"
    source: "10.10.13.30"
    destination: "any"
    destination_port: "3478-3497"
    description: "Allow STUN/TURN for Eufy P2P connections"
    
  - type: "pass"
    interface: "LAN"
    ip_protocol: "inet"
    protocol: "TCP"
    source: "10.10.11.0/24"
    destination: "10.10.13.30"
    destination_port: "443"
    description: "Allow access to Eufy Hub from client network"
```

## Proxmox Cluster Management

The Proxmox cluster spanning the T40 and Protectli hardware is managed through dedicated scripts:

```python
def configure_proxmox_cluster(node_name, existing_cluster=None):
    """Configure Proxmox clustering"""
    import paramiko
    import time
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Load proxmox configuration
        config = load_config('services/proxmox/config.yaml')
        if not config:
            return False
        
        # Connect to Proxmox node
        ssh.connect(
            config['nodes'][node_name]['ip_address'], 
            username=config['auth']['username'],
            password=config['auth']['password']
        )
        
        if existing_cluster:
            # Join existing cluster
            logger.info(f"Joining {node_name} to existing cluster {existing_cluster}")
            
            # Get join information from existing cluster
            ssh_existing = paramiko.SSHClient()
            ssh_existing.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_existing.connect(
                config['nodes'][existing_cluster]['ip_address'],
                username=config['auth']['username'],
                password=config['auth']['password']
            )
            
            # Generate join token on existing cluster
            stdin, stdout, stderr = ssh_existing.exec_command(
                "pvecm generatetoken"
            )
            
            # Parse token
            output = stdout.read().decode()
            token_lines = output.strip().split('\n')
            join_ip = config['nodes'][existing_cluster]['ip_address']
            fingerprint = ""
            token = ""
            
            for line in token_lines:
                if line.startswith("token:"):
                    token = line.split("token:")[1].strip()
                if line.startswith("fingerprint:"):
                    fingerprint = line.split("fingerprint:")[1].strip()
            
            # Join cluster
            command = f"pvecm add {join_ip} --force=1 --fingerprint={fingerprint} --token={token}"
            stdin, stdout, stderr = ssh.exec_command(command)
            
            # Wait for cluster to join
            time.sleep(30)
            
            # Verify cluster status
            stdin, stdout, stderr = ssh.exec_command("pvecm status")
            status = stdout.read().decode()
            
            if "cluster is not ready" in status.lower():
                logger.error(f"Failed to join cluster: {status}")
                return False
            
            logger.info(f"Successfully joined {node_name} to cluster")
            return True
            
        else:
            # Create new cluster
            logger.info(f"Creating new cluster on {node_name}")
            
            # Create cluster
            stdin, stdout, stderr = ssh.exec_command(
                f"pvecm create {config['cluster']['name']} --force=1"
            )
            
            # Wait for cluster to initialize
            time.sleep(10)
            
            # Check cluster status
            stdin, stdout, stderr = ssh.exec_command("pvecm status")
            status = stdout.read().decode()
            
            if "cluster is not ready" in status.lower():
                logger.error(f"Failed to create cluster: {status}")
                return False
            
            logger.info(f"Successfully created cluster on {node_name}")
            return True
            
    except Exception as e:
        logger.exception(f"Error configuring Proxmox cluster: {str(e)}")
        return False
    
    finally:
        ssh.close()
```

Example Proxmox configuration (YAML):

```yaml
# services/proxmox/config.yaml
auth:
  username: "root"
  password: "secured_with_vault"  # In production use Vault or similar

cluster:
  name: "home-cluster"

nodes:
  t40:
    ip_address: "10.10.10.10"
    hostname: "proxmox.home.banjonet.com"
    role: "compute"
    
  protectli:
    ip_address: "10.10.10.11"
    hostname: "protectli.home.banjonet.com"
    role: "network"
```

## Continuous Integration and Deployment

Changes to network configuration follow a CI/CD workflow:

1. **Develop**: Changes are developed locally and tested in a development environment
2. **Version Control**: Changes are committed to the Git repository
3. **Test**: Automated tests validate changes in a test environment
4. **Review**: Changes are reviewed by another administrator or AI assistant
5. **Deploy**: Changes are deployed to production with automated rollback capability
6. **Verify**: Deployment success is verified with automated tests

```python
def deploy_with_verification(config_type):
    """Deploy configuration with verification and rollback capability"""
    # Backup current configuration
    if not backup_configuration():
        logger.error("Failed to create backup before deployment")
        return False
    
    # Deploy configuration
    deploy_function = globals()[f"deploy_{config_type}"]
    if not deploy_function():
        logger.error(f"Failed to deploy {config_type}")
        return False
    
    # Verify deployment
    verify_function = globals()[f"validate_{config_type}"]
    if not verify_function():
        logger.error(f"Validation failed for {config_type}, rolling back")
        if not restore_latest_backup():
            logger.critical("Rollback failed! Manual intervention required")
        return False
    
    logger.info(f"Successfully deployed and verified {config_type}")
    return True
```

## Maintenance and Monitoring

Ongoing maintenance and monitoring is automated through scheduled scripts:

```python
def check_opnsense_health():
    """Check OPNsense health and alert on issues"""
    # Check system stats
    system_stats = api_call("GET", "system/status/system")
    if not system_stats:
        logger.error("Failed to get system stats")
        return False
    
    # Check interface status
    interfaces = api_call("GET", "interfaces/overview/interfaceStatus")
    if not interfaces:
        logger.error("Failed to get interface status")
        return False
    
    # Check for issues
    issues = []
    
    # CPU load
    if float(system_stats.get('cpu_load', 0)) > 80:
        issues.append(f"High CPU load: {system_stats.get('cpu_load')}%")
    
    # Memory usage
    memory_usage = int(system_stats.get('memory_usage', 0))
    if memory_usage > 80:
        issues.append(f"High memory usage: {memory_usage}%")
    
    # Interface issues
    for interface in interfaces:
        if interface.get('status') != 'up':
            issues.append(f"Interface {interface.get('name')} is down")
    
    # Alert on issues
    if issues:
        alert_message = "OPNsense Health Check Issues:\n" + "\n".join(issues)
        logger.error(alert_message)
        # Send alert (email, SMS, etc.)
        return False
    
    return True
```

## Conclusion

This infrastructure-as-code approach provides:

1. **Consistency**: All network changes follow the same pattern and validation
2. **Documentation**: The code itself serves as documentation for the network
3. **Reproducibility**: The entire network can be rebuilt from code if needed
4. **Auditability**: All changes are tracked in version control
5. **Automation**: Routine tasks are automated, reducing human error
6. **Testing**: Changes can be tested before deployment to production
7. **Rollback**: Failed changes can be quickly rolled back

By using OPNsense with its robust API capabilities, we gain the benefits of both a user-friendly web interface when needed and powerful automation capabilities for routine management tasks.
    
    # Test connectivity
    tests = [
        # Test IoT to Internet
        {'source': '10.10.13.10', 'destination': '8.8.8.8', 'expected': True},
        # Test Guest to Static (should be blocked)
        {'source': '10.10.12.10', 'destination': '10.10.10.10', 'expected': False}
    ]
    
    for test in tests:
        result = subprocess.run(
            ['ping', '-c', '1', '-S', test['source'], test['destination']],
            capture_output=True
        )
        success = result.returncode == 0
        
        if success != test['expected']:
            print(f"Test failed: {test['source']} to {test['destination']}")
            return False
    
    return True
```

## Integration with AI Assistants

The code structure is designed to work well with AI assistants like GitHub Copilot:

1. **Descriptive Function Names**: Functions have clear names that indicate their purpose
2. **Type Hints**: Python type hints help AI understand data structures
3. **Documentation**: Comprehensive docstrings explain function behavior
4. **Modular Structure**: Code is organized in logical modules
5. **Consistent Patterns**: Similar operations follow consistent patterns
6. **Clear Error Messages**: Errors provide context for troubleshooting

## Change Management Process

1. **Propose Change**: Document the intended change
2. **Develop Code**: Update configuration files and scripts
3. **Test Change**: Run in test environment
4. **Peer Review**: Review by another team member or AI assistant
5. **Deploy Change**: Apply to production
6. **Validate Change**: Confirm changes are working as expected
7. **Document Change**: Update documentation

## Version Control Strategy

All infrastructure code is version controlled using git:

```bash
# Initialize repository
git init network-automation

# Add files
git add .

# Commit changes
git commit -m "Initial network automation setup"

# Create branch for changes
git checkout -b feature/add-new-firewall-rules

# After testing, merge changes
git checkout main
git merge feature/add-new-firewall-rules
```

## Resources

- [OPNsense API Documentation](https://docs.opnsense.org/development/api.html)
- [Python Requests Library](https://requests.readthedocs.io/)
- [YAML Documentation](https://yaml.org/spec/1.2.2/)

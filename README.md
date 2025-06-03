# Personal Homeserver Configuration

This repository is designed to work as a nested git repository inside the [Fledgewing/homeserver-base](https://github.com/Fledgewing/homeserver-base) project. It contains personal configuration files, secrets, and customizations specific to your homeserver deployment.

## Documentation Index

### Hardware and Infrastructure
- [Hardware Setup](hardware-setup.md) - Detailed information about my Dell PowerEdge T40 server, including hardware specifications, upgrades, and storage configuration.
- [Network & Router Setup](network-setup.md) - Information about my network configuration, router setup, and connectivity details.

### Configuration
- *Additional configuration documents will be added here as they're created*

### Maintenance
- *Maintenance procedures and logs will be added here as they're created*

### Backup & Recovery
- *Backup and recovery procedures will be added here as they're created*

## Relationship with homeserver-base

This repository (`homeserver-base-personal`) is meant to be:

1. **Nested inside homeserver-base**: It should be cloned into the `personal/` directory of the main homeserver-base project.
2. **Privately tracked**: Unlike the main project which is public, this repository can contain your personal configurations and secrets.
3. **Ignored by the parent**: The main homeserver-base repository's `.gitignore` includes the `personal/` directory to avoid tracking your personal configs.

## Setup Instructions

### 1. Clone the main repository
```bash
git clone https://github.com/Fledgewing/homeserver-base.git
cd homeserver-base
```

### 2. Clone this personal repository into the personal directory
```bash
git clone https://github.com/benfeely/homeserver-base-personal.git personal
```

### 3. Use this repository for your personal configurations
Add your personal configurations, secrets, and customizations here while keeping the main repository clean and shareable.

## Purpose

Use this repository to store:
- Custom Kubernetes manifests specific to your deployment
- Personal secrets (properly encrypted)
- Overrides for default configurations in the main project
- Any other files that should not be shared in the public main repository

## Reference

- Main Project: [Fledgewing/homeserver-base](https://github.com/Fledgewing/homeserver-base)
- Personal Project: [benfeely/homeserver-base-personal](https://github.com/benfeely/homeserver-base-personal)

# Archived Docker-Based OPNsense Development Environment

This directory contains the archived Docker-based OPNsense development environment that was initially created but later replaced with a UTM-based approach.

## Why it was replaced

The Docker-based approach had compatibility issues with Apple Silicon (arm64) architecture, as the OPNsense Docker image (`demisto/opnsense:1.0.0.3547071`) was designed for x86/amd64 architecture.

## Current Approach

The current development environment uses UTM virtualization instead, which provides better compatibility with both Intel and Apple Silicon Macs. The UTM-based approach is located in the `/Users/benfeely/Projects/homeserver-base/personal/opnsense-utm` directory.

## Files in this Archive

- `docker-compose.yml`: Docker Compose configuration for the OPNsense container
- `manage.py`: Management script for the Docker environment
- `test_api.py`: Script for testing API connectivity
- `init_repo.py`: Script to initialize the repository structure
- Various configuration directories (`conf`, `etc`, `var`)

This archived code is kept for reference purposes only and is not maintained.

#!/bin/zsh
# filepath: /Users/benfeely/Projects/homeserver-base/personal/opnsense-utm/set-env.sh
# Script to set environment variables for OPNsense API access

# Default values (can be changed)
DEFAULT_URL="https://192.168.1.1"

echo "Setting up environment variables for OPNsense API access"
echo "---------------------------------------------------------"

# Get user inputs with defaults
read -p "Enter OPNsense URL [$DEFAULT_URL]: " OPNSENSE_URL
OPNSENSE_URL=${OPNSENSE_URL:-$DEFAULT_URL}

read -p "Enter OPNsense API key: " OPNSENSE_API_KEY
read -p "Enter OPNsense API secret: " OPNSENSE_API_SECRET

# Export the environment variables
export OPNSENSE_URL="$OPNSENSE_URL"
export OPNSENSE_API_KEY="$OPNSENSE_API_KEY"
export OPNSENSE_API_SECRET="$OPNSENSE_API_SECRET"

echo
echo "Environment variables set successfully!"
echo "URL: $OPNSENSE_URL"
echo "API Key: ${OPNSENSE_API_KEY:0:4}..."
echo "API Secret: ${OPNSENSE_API_SECRET:0:4}..."
echo
echo "To use these variables in the current shell session, source this script:"
echo "source ./set-env.sh"

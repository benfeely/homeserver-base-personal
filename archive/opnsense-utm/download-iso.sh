#!/bin/zsh
# filepath: /Users/benfeely/Projects/homeserver-base/personal/opnsense-utm/download-iso.sh
# Script to download the latest OPNsense ISO

# Default download directory
DOWNLOAD_DIR="$(pwd)/iso"
OPNSENSE_DOWNLOAD_URL="https://opnsense.org/download"

# Create download directory if it doesn't exist
mkdir -p "$DOWNLOAD_DIR"

echo "OPNsense ISO Downloader"
echo "======================="
echo "This script will help you download the latest OPNsense ISO for your UTM VM."
echo

echo "1. Go to $OPNSENSE_DOWNLOAD_URL in your browser"
echo "2. Select the AMD64 (DVD or VGA) image"
echo "3. Copy the download URL"
echo
read -p "Enter the OPNsense ISO download URL: " ISO_URL

if [[ -z "$ISO_URL" ]]; then
    echo "Error: No URL provided. Exiting."
    exit 1
fi

# Extract filename from URL
FILENAME=$(basename "$ISO_URL")

echo "Downloading $FILENAME to $DOWNLOAD_DIR..."
curl -L "$ISO_URL" -o "$DOWNLOAD_DIR/$FILENAME"

if [ $? -eq 0 ]; then
    echo "Download complete! ISO saved to: $DOWNLOAD_DIR/$FILENAME"
    echo "Use this ISO when creating your UTM virtual machine."
else
    echo "Error: Download failed. Please check the URL and try again."
fi

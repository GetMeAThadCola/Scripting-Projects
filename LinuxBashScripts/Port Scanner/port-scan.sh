#!/bin/bash
# Email:  huntertcarbonebuisness@gmail.com
# Author: Hunter Carbone
# 
#Description: Simple network port scanner using Nmap.
#
# Usage: ./port_scanner.sh
#

# Display a header with your name and script description
echo "This Code Is Property Of Hunter Carbone"
echo "========================================"
echo "Network Port Scanner Using Nmap"
echo "========================================"

# Prompt the user to enter the network or IP address to scan
read -p "Enter the network or IP address to scan: " target

# Check if the user provided a valid target
if [ -z "$target" ]; then
  echo "Please provide a valid network or IP address."
  exit 1
fi

# Implement Nmap to scan for open ports
nmap_result=$(nmap -p 1-65535 "$target" 2>&1)

# Check if Nmap executed successfully
if [ $? -eq 0 ]; then
  # Display the scan results
  echo "Scan results for $target:"
  echo "============================"
  echo -e "$nmap_result"
else
  # Display an error message if Nmap encountered an issue
  echo "Error: Nmap encountered an issue."
fi

# End of script

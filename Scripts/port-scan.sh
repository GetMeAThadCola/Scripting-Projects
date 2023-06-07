#!/bin/bash

echo "This Code Is Property Of Hunter Carbone"

#Prompt the user to enter the netwrom or IP address to scan
read -p "Enter the network or IP address to scan: " target

#Implement NMAP Function to scan for open ports

nmap -p 1-65535 $target

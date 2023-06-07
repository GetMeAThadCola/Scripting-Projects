#!/bin/bash

# Check if the user has provided an image file
if [ -z "$1" ]; then
  echo "Please provide an image file as an argument."
  exit 1
fi

# Check if the file exists
if [ ! -f "$1" ]; then
  echo "File not found: $1"
  exit 1
fi

# Use steghide to extract any hidden messages
steghide extract -sf "$1"

# If the exit code is 0, display a message to the user
if [ $? -eq 0 ]; then
  echo "Hidden messages extracted from $1"
fi

#!/bin/bash

# Function to check if there is something to extract from the image
has_something_to_extract() {
  # Replace this condition with your specific criteria to determine if there's something to extract
  # For example, you can check the image file size or some metadata.
  # This example checks if the file size is greater than 100 bytes.
  local image_file="$1"
  local file_size=$(stat -c %s "$image_file")
  if [ "$file_size" -gt 100 ]; then
    return 0  # There is something to extract
  else
    return 1  # There is nothing to extract
  fi
}

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

# Check if there is something to extract
if has_something_to_extract "$1"; then
  # Use steghide to extract any hidden messages
  steghide extract -sf "$1"

  # If the exit code is 0, display a message to the user
  if [ $? -eq 0 ]; then
    echo "Hidden messages extracted from $1"
  fi
else
  echo "Image $1 has nothing to extract."
fi

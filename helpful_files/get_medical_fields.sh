#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <json_file>"
    exit 1
fi

json_file="$1"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Please install jq first."
    exit 1
fi

# Print keys using jq
keys=$(jq -r 'keys_unsorted[]' "$json_file")

# Print the keys
echo "Keys in the JSON file:"
echo "$keys"

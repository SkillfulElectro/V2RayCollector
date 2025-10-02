#!/bin/bash


CONFIG_FILE="Config/all_configs.txt"
SUBS_FILE="Subs_list.sh"


if [ ! -f "$SUBS_FILE" ]; then
    echo "Error: $SUBS_FILE not found."
    exit 1
fi


source "$SUBS_FILE"

if [ ${#SUBS_URLS[@]} -eq 0 ]; then
    echo "No subscription URLs found in $SUBS_FILE. Skipping."
    exit 0
fi


FETCHED_CONTENT=$(mktemp)


for url in "${SUBS_URLS[@]}"; do
    echo "Fetching: $url"

    curl -sL --fail "$url" >> "$FETCHED_CONTENT"
    
    echo "" >> "$FETCHED_CONTENT"
done


if [ ! -s "$FETCHED_CONTENT" ]; then
    echo "No content fetched from subscriptions."
    rm "$FETCHED_CONTENT"
    exit 0
fi


NEW_CONFIG=$(mktemp)


cat "$FETCHED_CONTENT" "$CONFIG_FILE" > "$NEW_CONFIG"
mv "$NEW_CONFIG" "$CONFIG_FILE"
rm "$FETCHED_CONTENT"

echo "Successfully fetched subscriptions and updated $CONFIG_FILE."

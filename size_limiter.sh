#!/bin/bash

# Usage: ./size_limiter.sh <filename> [target_size_in_MB] [direction]
# Default target size: 3 MB
# Default direction: bottom (keep newest lines, remove oldest from top)
# direction: "bottom" = remove from top (oldest lines)
#            "top"    = remove from bottom (newest lines)

filename="${1}"
target_mb="${2:-3}"
direction="${3:-bottom}"  # bottom or top

if [[ -z "$filename" || ! -f "$filename" ]]; then
    echo "Usage: $0 <filename> [target_size_in_MB] [direction: bottom|top]"
    echo "Error: File not provided or does not exist."
    exit 1
fi

if [[ "$direction" != "bottom" && "$direction" != "top" ]]; then
    echo "Invalid direction: '$direction'. Use 'bottom' or 'top'."
    exit 1
fi

target_bytes=$((target_mb * 1024 * 1024))

# Get current size in bytes (works on Linux and macOS)
current_size=$(stat -c%s "$filename" 2>/dev/null || stat -f%z "$filename")

if (( current_size <= target_bytes )); then
    echo "File '$filename' is already <= ${target_mb} MB (${current_size} bytes). No action needed."
    exit 0
fi

echo "File '$filename' is ${current_size} bytes (> ${target_mb} MB). Reducing to <= ${target_mb} MB by removing from ${direction}..."

tempfile=$(mktemp)

if [[ "$direction" == "bottom" ]]; then
    # Keep newest lines: remove from top (oldest)
    # Efficient: tail reads from end, writes only needed part
    tail -c "$target_bytes" "$filename" > "$tempfile"
else
    # Keep oldest lines: remove from bottom (newest)
    # head reads from start, stops early
    head -c "$target_bytes" "$filename" > "$tempfile"
fi

# Overwrite original with reduced content
mv "$tempfile" "$filename"

new_size=$(stat -c%s "$filename" 2>/dev/null || stat -f%z "$filename")
echo "Reduction complete. New size: $new_size bytes."

# Note: Uses byte-level truncation for precision (exact <= target).
# For line-based (preserve whole lines), more complex logic needed.
# Caution: If file actively written (e.g., log), use logrotate instead.

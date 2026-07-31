#!/bin/bash
# scan_headers_values.sh - Show presence AND values of security headers
# Usage: ./scan_headers_values.sh urls.txt

if [ $# -eq 0 ]; then
    echo "Usage: $0 <url_list.txt>"
    exit 1
fi

INPUT_FILE="$1"

while IFS= read -r url; do
    [[ -z "$url" || "$url" =~ ^# ]] && continue

    echo "=== $url ==="

    # Fetch headers, follow redirects, silent, capture stderr too
    headers=$(curl -sIL "$url" 2>&1)

    # --- X-Robots-Tag ---
    if xrobot=$(echo "$headers" | grep -i "^X-Robots-Tag:"); then
        # Show each occurrence (just in case)
        echo "$xrobot" | while read -r line; do
            echo "  X-Robots-Tag: $line"
        done
    else
        echo "  X-Robots-Tag: [missing]"
    fi

    # --- Cache-Control ---
    if cache=$(echo "$headers" | grep -i "^Cache-Control:"); then
        echo "$cache" | while read -r line; do
            echo "  Cache-Control: $line"
        done
    else
        echo "  Cache-Control: [missing]"
    fi

    # --- Content-Security-Policy ---
    if csp=$(echo "$headers" | grep -i "^Content-Security-Policy:"); then
        echo "$csp" | while read -r line; do
            echo "  Content-Security-Policy: $line"
        done
    else
        echo "  Content-Security-Policy: [missing]"
    fi

    echo ""
done < "$INPUT_FILE"

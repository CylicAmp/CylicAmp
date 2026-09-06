#!/bin/bash
# scan_headers.sh - Check URLs for missing security headers

if [ $# -eq 0 ]; then
    echo "Usage: $0 <url_list.txt>"
    exit 1
fi

INPUT_FILE="$1"

while IFS= read -r url; do
    # Skip empty lines and comments
    [[ -z "$url" || "$url" =~ ^# ]] && continue

    echo "=== $url ==="
    # Fetch headers, follow redirects, silent mode
    headers=$(curl -sIL "$url" 2>&1)

    # Check each header
    if echo "$headers" | grep -qi "X-Robots-Tag:"; then
        echo "  [✓] X-Robots-Tag present"
    else
        echo "  [✗] X-Robots-Tag missing"
    fi

    if echo "$headers" | grep -qi "Cache-Control:"; then
        echo "  [✓] Cache-Control present"
    else
        echo "  [✗] Cache-Control missing"
    fi

    if echo "$headers" | grep -qi "Content-Security-Policy:"; then
        echo "  [✓] CSP present"
    else
        echo "  [✗] CSP missing"
    fi

    echo ""
done < "$INPUT_FILE"

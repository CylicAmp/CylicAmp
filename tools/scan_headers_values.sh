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
        echo "$xrobot" | while read -r line; do
            echo "  $line"
        done
    else
        echo "  X-Robots-Tag: [missing]"
    fi

    # --- Cache-Control ---
    if cache=$(echo "$headers" | grep -i "^Cache-Control:"); then
        echo "$cache" | while read -r line; do
            echo "  $line"
        done
    else
        echo "  Cache-Control: [missing]"
    fi

    # --- Content-Security-Policy ---
    if csp=$(echo "$headers" | grep -i "^Content-Security-Policy:"); then
        echo "$csp" | while read -r line; do
            echo "  $line"
        done
    else
        echo "  Content-Security-Policy: [missing]"
    fi

    # --- robots.txt ---
    origin=$(echo "$url" | grep -oE '^https?://[^/]+')
    path=$(echo "$url" | sed "s|$origin||")
    [[ -z "$path" ]] && path="/"

    robots_out=$(curl -sL --write-out "|%{http_code}" "$origin/robots.txt" 2>/dev/null)
    robots_code=$(echo "$robots_out" | grep -oE '\|[0-9]+$' | tr -d '|')
    robots_body=$(echo "$robots_out" | sed 's/|[0-9]*$//')

    if [[ "$robots_code" == "200" ]]; then
        matched=$(echo "$robots_body" | grep -i "^Disallow:" | while IFS= read -r rule; do
            rule_path=$(echo "$rule" | sed 's/^[Dd]isallow:[[:space:]]*//' | tr -d '*')
            if [[ -n "$rule_path" && "$path" == "$rule_path"* ]]; then
                echo "  $rule  <- matches $path"
            fi
        done)
        if [[ -n "$matched" ]]; then
            echo "  robots.txt: path is disallowed"
            echo "$matched"
        else
            echo "  robots.txt: fetched OK, path not disallowed"
        fi
    else
        echo "  robots.txt: [$robots_code]"
    fi

    echo ""
done < "$INPUT_FILE"

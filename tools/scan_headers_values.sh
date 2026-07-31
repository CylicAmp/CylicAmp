#!/bin/bash
# scan_headers_values.sh - Security header audit with value analysis and grading
# Usage: ./scan_headers_values.sh [--no-color] <url_list.txt>

# ── Args ──────────────────────────────────────────────────────────────────────

NO_COLOR=0; INPUT_FILE=""
for arg in "$@"; do
    case "$arg" in --no-color) NO_COLOR=1 ;; *) INPUT_FILE="$arg" ;; esac
done
[[ -z "$INPUT_FILE" ]] && { echo "Usage: $0 [--no-color] <url_list.txt>"; exit 1; }

# ── Colors ────────────────────────────────────────────────────────────────────

if [[ "$NO_COLOR" -eq 0 && -t 1 ]]; then
    RED=$'\033[0;31m' GRN=$'\033[0;32m' YLW=$'\033[0;33m'
    CYN=$'\033[0;36m' BOLD=$'\033[1m' RST=$'\033[0m'
else
    RED='' GRN='' YLW='' CYN='' BOLD='' RST=''
fi

SUMMARY=()

# ── Helpers ───────────────────────────────────────────────────────────────────

get_header() { echo "$1" | grep -i "^$2:"; }
hval()        { echo "$1" | sed 's/^[^:]*:[[:space:]]*//'; }  # strip "Header-Name: "

# ── Main loop ─────────────────────────────────────────────────────────────────

while IFS= read -r url; do
    [[ -z "$url" || "$url" =~ ^# ]] && continue

    echo "${BOLD}=== $url ===${RST}"
    headers=$(curl -sIL "$url" 2>&1)
    np=0; nw=0; nf=0

    p() { echo "  ${GRN}[PASS]${RST} $*"; ((np++)); }
    w() { echo "  ${YLW}[WARN]${RST} $*"; ((nw++)); }
    f() { echo "  ${RED}[FAIL]${RST} $*"; ((nf++)); }
    i() { echo "  ${CYN}[INFO]${RST} $*"; }

    # ── X-Robots-Tag ──────────────────────────────────────────────────────────
    val=$(get_header "$headers" "X-Robots-Tag")
    if [[ -n "$val" ]]; then
        v=$(hval "$val")
        if echo "$v" | grep -qiE '\bnone\b|noindex'; then
            p "$val"
            echo "$v" | grep -qiE '\bnone\b' && \
                i "  'none' = noindex, nofollow (Google spec; crawlers must de-index)"
        else
            w "$val  (present but no noindex directive)"
        fi
    else
        f "X-Robots-Tag: [missing]"
    fi

    # ── Cache-Control ─────────────────────────────────────────────────────────
    val=$(get_header "$headers" "Cache-Control")
    if [[ -n "$val" ]]; then
        v=$(hval "$val" | tr '[:upper:]' '[:lower:]')
        if echo "$v" | grep -q 'no-store'; then
            p "$val"
        elif echo "$v" | grep -qE 'private|no-cache'; then
            w "$val  (no-store preferred for sensitive responses)"
        elif echo "$v" | grep -q 'public'; then
            f "$val  (public caching on potentially sensitive endpoint)"
        else
            w "$val"
        fi
    else
        f "Cache-Control: [missing]"
    fi

    # ── Strict-Transport-Security ─────────────────────────────────────────────
    val=$(get_header "$headers" "Strict-Transport-Security")
    if [[ -n "$val" ]]; then
        max_age=$(hval "$val" | grep -oE 'max-age=[0-9]+' | grep -oE '[0-9]+' | head -1)
        if [[ -n "$max_age" && "$max_age" -ge 31536000 ]]; then
            p "$val"
        elif [[ -n "$max_age" ]]; then
            w "$val  (max-age $max_age < 31536000; recommend 1 year minimum)"
        else
            w "$val  (no max-age found)"
        fi
    else
        f "Strict-Transport-Security: [missing]"
    fi

    # ── X-Content-Type-Options ────────────────────────────────────────────────
    val=$(get_header "$headers" "X-Content-Type-Options")
    if [[ -n "$val" ]]; then
        echo "$val" | grep -qi 'nosniff' && p "$val" || w "$val  (expected: nosniff)"
    else
        f "X-Content-Type-Options: [missing]"
    fi

    # ── X-Frame-Options ───────────────────────────────────────────────────────
    val=$(get_header "$headers" "X-Frame-Options")
    if [[ -n "$val" ]]; then
        echo "$val" | grep -qiE 'DENY|SAMEORIGIN' && p "$val" || w "$val"
    else
        w "X-Frame-Options: [missing]  (verify CSP frame-ancestors covers this)"
    fi

    # ── Referrer-Policy ───────────────────────────────────────────────────────
    val=$(get_header "$headers" "Referrer-Policy")
    if [[ -n "$val" ]]; then
        echo "$val" | grep -qiE 'no-referrer$|strict-origin' \
            && p "$val" \
            || w "$val  (consider strict-origin-when-cross-origin or no-referrer)"
    else
        w "Referrer-Policy: [missing]"
    fi

    # ── Content-Security-Policy ───────────────────────────────────────────────
    val=$(get_header "$headers" "Content-Security-Policy")
    if [[ -n "$val" ]]; then
        p "Content-Security-Policy: present"
        while IFS= read -r line; do
            i "  $(hval "$line")"
        done <<< "$val"
    else
        f "Content-Security-Policy: [missing]"
    fi

    # ── Permissions-Policy ────────────────────────────────────────────────────
    val=$(get_header "$headers" "Permissions-Policy")
    if [[ -n "$val" ]]; then
        v=$(hval "$val")
        i "Permissions-Policy: ${v:0:100}$([[ ${#v} -gt 100 ]] && echo '...')"
    else
        i "Permissions-Policy: [missing]  (not graded — site-specific)"
    fi

    # ── robots.txt ────────────────────────────────────────────────────────────
    origin=$(echo "$url" | grep -oE '^https?://[^/]+')
    path=$(echo "$url" | sed "s|$origin||")
    [[ -z "$path" ]] && path="/"

    robots_out=$(curl -sL --write-out "|%{http_code}" "$origin/robots.txt" 2>/dev/null)
    robots_code=$(echo "$robots_out" | grep -oE '\|[0-9]+$' | tr -d '|')
    robots_body=$(echo "$robots_out" | sed 's/|[0-9]*$//')

    if [[ "$robots_code" == "200" ]]; then
        matched=$(echo "$robots_body" | grep -i "^Disallow:" | while IFS= read -r rule; do
            rule_path=$(echo "$rule" | sed 's/^[Dd]isallow:[[:space:]]*//' | tr -d '*')
            [[ -n "$rule_path" && "$path" == "$rule_path"* ]] && \
                echo "    $rule  <- matches $path"
        done)
        if [[ -n "$matched" ]]; then
            w "robots.txt: path disallowed — noindex signal unreachable by crawlers"
            echo "$matched"
        else
            p "robots.txt: path not disallowed — crawlers can fetch noindex signal"
        fi
    else
        w "robots.txt: HTTP $robots_code"
    fi

    # ── Per-URL score ─────────────────────────────────────────────────────────
    echo ""
    printf "  Score: ${GRN}%d pass${RST}  ${YLW}%d warn${RST}  ${RED}%d fail${RST}\n" \
        "$np" "$nw" "$nf"
    echo ""

    SUMMARY+=("$url|$np|$nw|$nf")

done < "$INPUT_FILE"

# ── Summary table (multi-URL runs only) ───────────────────────────────────────

if [[ ${#SUMMARY[@]} -gt 1 ]]; then
    echo "${BOLD}════════════════════════════════════ SUMMARY ════${RST}"
    printf "  %-50s  %4s  %4s  %4s\n" "URL" "PASS" "WARN" "FAIL"
    printf "  %-50s  %4s  %4s  %4s\n" \
        "--------------------------------------------------" "----" "----" "----"
    for entry in "${SUMMARY[@]}"; do
        IFS='|' read -r surl sp sw sf <<< "$entry"
        printf "  %-50s  ${GRN}%4d${RST}  ${YLW}%4d${RST}  ${RED}%4d${RST}\n" \
            "${surl:0:50}" "$sp" "$sw" "$sf"
    done
    echo ""
fi

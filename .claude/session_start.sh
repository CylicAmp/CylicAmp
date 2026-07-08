#!/usr/bin/env bash
# Session Handoff Protocol — runs at session start
# Pulls latest state from GitHub, reads handoff.json, validates checkpoint

set -e

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo /home/user/CylicAmp)"
HANDOFF="$REPO_ROOT/handoff.json"

echo "=== SHP: Session Handoff Protocol ==="

# 1. Pull latest state
git -C "$REPO_ROOT" fetch origin 2>/dev/null && echo "[SHP] Fetched latest from origin"

# 2. Check for handoff file
if [ ! -f "$HANDOFF" ]; then
  echo "[SHP] No handoff.json found. Fresh session."
  exit 0
fi

# 3. Parse and display key fields
echo "[SHP] Handoff state detected:"
python3 -c "
import json, sys
with open('$HANDOFF') as f:
    h = json.load(f)
print(f'  session   : {h.get(\"last_session_id\")}')
print(f'  branch    : {h.get(\"active_branch\")}')
print(f'  task      : {h.get(\"active_task\")}')
print(f'  status    : {h.get(\"status\")}')
print(f'  checkpoint: {h.get(\"last_checkpoint\")}')
pending = h.get('pending_actions', [])
if pending:
    print('  pending:')
    for p in pending:
        print(f'    - {p}')
"

# 4. Validate checkpoint integrity if sha256 is set
SHA=$(python3 -c "import json; h=json.load(open('$HANDOFF')); print(h.get('last_checkpoint_sha256',''))")
CHKFILE=$(python3 -c "import json; h=json.load(open('$HANDOFF')); print(h.get('last_checkpoint',''))")

if [ -n "$SHA" ] && [ -n "$CHKFILE" ]; then
  ACTUAL=$(sha256sum "$REPO_ROOT/$CHKFILE" 2>/dev/null | cut -d' ' -f1)
  if [ "$ACTUAL" = "$SHA" ]; then
    echo "[SHP] Checkpoint integrity: OK ($CHKFILE)"
  else
    echo "[SHP] WARNING: Checkpoint mismatch on $CHKFILE"
    echo "  expected: $SHA"
    echo "  actual  : $ACTUAL"
  fi
fi

echo "[SHP] Ready."

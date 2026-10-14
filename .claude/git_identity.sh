#!/usr/bin/env bash
# SessionStart hook. 2026-10-03 request: "mark Claude's commits and add the startup script".
# 2026-10-14: that was carried out by making Claude the AUTHOR, which took the owner's name off
# the owner's work -- the owner never asked for that ("The algorithm is telling me that I said to
# take my name off of my work", #274). Now: author = the owner, Michael Warren Song; committer =
# Claude; every commit marked with a Claude-Session trailer naming the session.
# Runs only inside a Claude Code session; the owner's own git setup elsewhere is untouched.
[ -n "$CLAUDE_CODE_SESSION_ID$CLAUDE_CODE_REMOTE_SESSION_ID" ] || exit 0
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
git -C "$ROOT" config user.name "Michael Warren Song"
git -C "$ROOT" config user.email "red3rdeye@gmail.com"
git -C "$ROOT" config author.name "Michael Warren Song"
git -C "$ROOT" config author.email "red3rdeye@gmail.com"
git -C "$ROOT" config committer.name "Claude"
git -C "$ROOT" config committer.email "noreply@anthropic.com"
HOOK="$ROOT/$(git -C "$ROOT" rev-parse --git-path hooks)/commit-msg"
mkdir -p "$(dirname "$HOOK")"
cat > "$HOOK" <<'HOOKEOF'
#!/usr/bin/env bash
# Installed by .claude/git_identity.sh: tag commits made in a Claude session.
id="${CLAUDE_CODE_REMOTE_SESSION_ID#cse_}"
if [ -n "$id" ]; then url="https://claude.ai/code/session_$id"; else url="local:${CLAUDE_CODE_SESSION_ID:-unknown}"; fi
grep -q '^Claude-Session:' "$1" || printf '\nClaude-Session: %s\n' "$url" >> "$1"
HOOKEOF
chmod +x "$HOOK"
echo "[git] session commits: author Michael Warren Song (the owner), committer Claude, tagged Claude-Session"

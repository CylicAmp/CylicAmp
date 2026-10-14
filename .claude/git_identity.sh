#!/usr/bin/env bash
# SessionStart hook. Commits carry the owner's name as author (Michael Warren Song);
# Claude is the committer, and a Claude-Session trailer names the session.
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

#!/usr/bin/env bash
#
# Restore the repository owner's git identity for future commits.
#
# Reverses .claude/git_identity.sh, the SessionStart hook added 2026-10-03,
# which sets author and committer to Claude <noreply@anthropic.com> and
# installs a commit-msg hook appending a Claude-Session trailer.  That hook
# contradicts the directive recorded in CLAUDE.md on 2026-07-07:
#
#     All git commits use Michael Warren Song <Red3rdeye@gmail.com>
#     No Claude/Anthropic name on any commit. Ever.
#
# NOTHING HERE REWRITES HISTORY AND NOTHING IS PUSHED.  Only future commits
# are affected.  Existing commits stay exactly as they are.  To change past
# commits, that is scripts/fix_authorship.sh, which is a separate and much
# higher-risk operation.
#
# Run from a checkout of any branch that carries .claude/ (main does):
#
#     bash scripts/disable_claude_identity.sh
#
# Affected branches, as of 2026-11-05: main, all-work,
# claude/add-torus-animation-6Ey5Z, claude/signature-obfuscation-audit-ZEoCd,
# copilot/fix-github-actions-job, copilot/fix-github-actions-job-failure,
# copilot/fix-github-actions-job-failure-again.
# Each one needs this run on it, or the file removed, then committed.
set -euo pipefail

NAME="Michael Warren Song"
EMAIL="Red3rdeye@gmail.com"

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
say() { printf '  %s\n' "$*"; }
printf '\n== restoring owner identity in %s\n' "$ROOT"

# 1. git config, every scope that can override
for scope in --local --global; do
  git config $scope user.name  "$NAME"
  git config $scope user.email "$EMAIL"
  say "git config $scope -> $NAME <$EMAIL>"
done
if git config --system --get user.email >/dev/null 2>&1; then
  say "NOTE: a --system user.email is also set; it is outranked by --global and --local."
fi

# 2. neutralise the SessionStart script without deleting it, so the change
#    is visible in the diff rather than silent
if [ -f .claude/git_identity.sh ]; then
  if head -20 .claude/git_identity.sh | grep -q '^exit 0 *# disabled'; then
    say ".claude/git_identity.sh already disabled"
  else
    python3 - <<'PYEOF'
import io
p = '.claude/git_identity.sh'
s = open(p).read().split('\n')
out = [s[0] if s and s[0].startswith('#!') else '#!/usr/bin/env bash']
out += ['exit 0  # disabled: CLAUDE.md requires the owner identity on every commit.',
        '        # This script set author/committer to Claude <noreply@anthropic.com>.',
        '        # Left in place rather than deleted so the change is visible in git log.']
out += s[1:] if s and s[0].startswith('#!') else s
open(p, 'w').write('\n'.join(out))
PYEOF
    say ".claude/git_identity.sh -> exit 0 inserted at the top"
  fi
else
  say ".claude/git_identity.sh not on this branch, nothing to disable"
fi

# 3. drop the SessionStart entry that invokes it
if [ -f .claude/settings.json ]; then
  python3 - <<'PYEOF'
import json, sys
p = '.claude/settings.json'
d = json.load(open(p))
hooks = d.get('hooks', {})
before = json.dumps(hooks.get('SessionStart', []))
kept = []
for group in hooks.get('SessionStart', []):
    inner = [h for h in group.get('hooks', [])
             if 'git_identity' not in str(h.get('command', ''))]
    if inner:
        g = dict(group); g['hooks'] = inner; kept.append(g)
if kept:
    hooks['SessionStart'] = kept
else:
    hooks.pop('SessionStart', None)
if hooks:
    d['hooks'] = hooks
else:
    d.pop('hooks', None)
json.dump(d, open(p, 'w'), indent=2)
open(p, 'a').write('\n')
print('  .claude/settings.json -> SessionStart git_identity entry removed'
      if before != json.dumps(hooks.get('SessionStart', [])) else
      '  .claude/settings.json -> no git_identity entry found')
PYEOF
else
  say ".claude/settings.json not on this branch"
fi

# 4. remove the commit-msg hook the script installs, if it is that one
H="$(git rev-parse --git-path hooks)/commit-msg"
if [ -f "$H" ] && grep -q 'Claude-Session' "$H"; then
  rm -f "$H"; say "removed the Claude-Session commit-msg hook"
else
  say "no Claude-Session commit-msg hook present"
fi

# 5. report
printf '\n== effective identity for the next commit\n'
say "$(git config --get user.name) <$(git config --get user.email)>"
printf '\n== changed files (review, then commit on each affected branch)\n'
git status --short -- .claude/ || true
printf '\nNothing was pushed and no history was rewritten.\n'

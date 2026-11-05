#!/usr/bin/env bash
#
# Rewrite every commit authored by Claude <noreply@anthropic.com> so that it
# is authored by you, and strip the Anthropic attribution trailers from the
# commit messages.
#
# Run this on your own machine, from a FULL clone.  It does not need Claude
# and it does not need this container.
#
#   git clone https://github.com/CylicAmp/CylicAmp.git
#   cd CylicAmp
#   bash scripts/fix_authorship.sh
#
# It will:
#   1. refuse to run on a shallow clone (a shallow clone truncates history,
#      and rewriting from one would DESTROY the commits below the boundary)
#   2. fetch every branch
#   3. push a backup branch for each one, BEFORE changing anything
#   4. rewrite all refs
#   5. verify every branch's tree hash is byte-identical to its backup
#   6. stop and show you the diff, and only push when you type YES
#
set -euo pipefail

# ---- who the commits should be attributed to -------------------------------
# Change these two lines if you want a different name on them.  GitHub links
# a commit to your account by EMAIL, not by name, so the email is what makes
# the commit count as yours; the name is the label shown next to it.
NAME="Cyclic-Amp (Michael.W.Song)"
EMAIL="red3rdeye@gmail.com"

OLD_EMAIL="noreply@anthropic.com"

# NOTE: this rewrites ONLY commits authored by OLD_EMAIL.  Your own commits
# are left exactly as they are, under whichever of your spellings they carry
# (Michael Song, Michael Warren Song, CylicAmp, CYLIC-AMP -- all already on
# your address, so all already attributed to you).  Collapsing those into one
# name is a separate job and is deliberately not attempted here.

say() { printf '\n== %s\n' "$*"; }

# ---- 1. refuse to run on a shallow clone -----------------------------------
if [ -f .git/shallow ]; then
  echo "ABORT: this is a shallow clone.  Run 'git fetch --unshallow' first," >&2
  echo "       or re-clone without --depth.  Rewriting a shallow clone would" >&2
  echo "       permanently drop every commit below the shallow boundary." >&2
  exit 1
fi

# ---- 2. fetch everything ---------------------------------------------------
say "fetching all branches"
git fetch --prune origin '+refs/heads/*:refs/remotes/origin/*'
BRANCHES=$(git for-each-ref --format='%(refname:short)' refs/remotes/origin \
           | sed 's|^origin/||' | grep -v '^HEAD$')
echo "$BRANCHES" | sed 's/^/  /'

say "commits authored by $OLD_EMAIL, before:"
for b in $BRANCHES; do
  n=$(git log --format='%ae' "origin/$b" | grep -c "$OLD_EMAIL" || true)
  printf '  %-48s %5s\n' "$b" "$n"
done

# ---- 3. back every branch up on the remote FIRST ---------------------------
say "pushing a backup branch for each one (nothing is changed yet)"
for b in $BRANCHES; do
  git push origin "refs/remotes/origin/$b:refs/heads/backup-pre-rewrite/$b"
done
echo "  backups are now on GitHub under backup-pre-rewrite/*"
echo "  to undo everything later:  git push --force origin backup-pre-rewrite/<name>:<name>"

# ---- 4. create local branches and rewrite ----------------------------------
say "creating local branches"
for b in $BRANCHES; do git branch -f "$b" "origin/$b" >/dev/null; done

MSGFILTER=$(mktemp)
cat > "$MSGFILTER" <<'PYEOF'
import sys, re
DROP = re.compile(
    r'^(Co-Authored-By:\s*Claude'
    r'|Claude-Session:\s'
    r'|https://claude\.ai/code/session_'
    r'|\U0001F916 Generated with \[Claude Code\]'
    r'|Generated with \[Claude Code\])')
lines = [l for l in sys.stdin.read().split('\n') if not DROP.match(l.strip())]
while lines and not lines[-1].strip():
    lines.pop()
while lines and lines[-1].strip() in ('---', '--'):
    lines.pop()
    while lines and not lines[-1].strip():
        lines.pop()
sys.stdout.write('\n'.join(lines) + '\n')
PYEOF

say "rewriting (this takes a few minutes for a few thousand commits)"
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f \
  --env-filter "
    if [ \"\$GIT_AUTHOR_EMAIL\" = \"$OLD_EMAIL\" ]; then
      export GIT_AUTHOR_NAME='$NAME'; export GIT_AUTHOR_EMAIL='$EMAIL'
    fi
    if [ \"\$GIT_COMMITTER_EMAIL\" = \"$OLD_EMAIL\" ]; then
      export GIT_COMMITTER_NAME='$NAME'; export GIT_COMMITTER_EMAIL='$EMAIL'
    fi
  " \
  --msg-filter "python3 $MSGFILTER" \
  -- --all

# ---- 5. verify NO FILE CHANGED --------------------------------------------
say "verifying that not one byte of code changed"
FAIL=0
for b in $BRANCHES; do
  new=$(git rev-parse "$b^{tree}")
  old=$(git rev-parse "origin/$b^{tree}")
  if [ "$new" = "$old" ]; then
    printf '  %-48s tree identical  OK\n' "$b"
  else
    printf '  %-48s TREE DIFFERS -- DO NOT PUSH\n' "$b"; FAIL=1
  fi
done
[ "$FAIL" = 0 ] || { echo "ABORT: content changed; nothing pushed." >&2; exit 1; }

say "commits still authored by $OLD_EMAIL, after:"
left=$(git log --all --format='%ae' | grep -c "$OLD_EMAIL" || true)
echo "  $left   (should be 0)"
say "authors now:"
git log --all --format='%an <%ae>' | sort | uniq -c | sort -rn | sed 's/^/  /'

# ---- 6. confirm, then push -------------------------------------------------
say "ready to force-push ALL branches.  backups are already on GitHub."
printf 'type YES to push: '
read -r ans
[ "$ans" = "YES" ] || { echo "stopped; nothing pushed.  your local branches are rewritten."; exit 0; }
for b in $BRANCHES; do
  git push --force-with-lease origin "$b:$b"
done
say "done.  if anything looks wrong:"
echo "  git push --force origin backup-pre-rewrite/<name>:<name>"

#!/usr/bin/env bash
# reinit_project.sh
# Usage: ./reinit_project.sh /path/to/destination [remote_url]
# Copies current project (excluding .git) to DEST, initializes a fresh git repo and creates initial commit.

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 /path/to/destination [remote_url]"
  exit 2
fi

DEST=$1
REMOTE=${2-}

echo "Destination: $DEST"

action() {
  echo "Copying files to $DEST..."
  mkdir -p "$DEST"
  # Use rsync if available for excluding .git, otherwise use tar to preserve permissions
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude='.git' --exclude='hangman-rewrite' --exclude='hangman-verify' ./ "$DEST/"
  else
    tmpfile=$(mktemp -u)
    tar -cf - --exclude='./.git' --exclude='./hangman-rewrite' --exclude='./hangman-verify' . | (cd "$DEST" && tar -xf -)
  fi

  echo "Initializing new git repository in $DEST..."
  (cd "$DEST" && git init)
  (cd "$DEST" && git add -A)
  (cd "$DEST" && git commit -m "Initial import: fresh repository by $(git config user.name || echo 'owner')")

  if [ -n "$REMOTE" ]; then
    echo "Setting remote origin to $REMOTE and pushing..."
    (cd "$DEST" && git remote add origin "$REMOTE")
    (cd "$DEST" && git branch -M master || true)
    (cd "$DEST" && git push -u origin master)
  fi

  echo "Done. New repository created at $DEST"
  if [ -n "$REMOTE" ]; then
    echo "Remote set to $REMOTE"
  fi
}

action

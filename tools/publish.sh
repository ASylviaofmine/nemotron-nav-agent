#!/usr/bin/env bash
# Publish this project to GitHub, in one command.
#
# The only thing this script cannot do is create the repository itself,
# because that needs a GitHub API token. Once the empty repository exists
# (two clicks on the GitHub website), this script does the rest.
#
#   1. Go to https://github.com/new  ->  name it "nemotron-nav-agent"
#      ->  Public  ->  "Create repository"  (do NOT tick "Add a README")
#   2. Run:  bash tools/publish.sh
#
# It pushes the current branch to "master" and makes the repository
# description and topic tags match what the submission form asks for.

set -euo pipefail

REPO="nemotron-nav-agent"
OWNER="ASylviaofmine"
REMOTE="git@ssh.github.com:${OWNER}/${REPO}.git"

cd "$(dirname "$0")/.."

echo "== checking the remote repository exists =="
if ! git ls-remote "$REMOTE" >/dev/null 2>&1; then
    echo
    echo "The repository ${OWNER}/${REPO} does not exist yet."
    echo
    echo "Create it here (takes about 20 seconds):"
    echo "    https://github.com/new"
    echo
    echo "  Repository name : ${REPO}"
    echo "  Description     : A wheeled robot that plans with A* and tracks with a"
    echo "                    proportional controller, supervised by an NVIDIA Nemotron"
    echo "                    model on Nebius Token Factory."
    echo "  Visibility      : Public"
    echo "  Do NOT tick     : 'Add a README file' / .gitignore / license"
    echo
    echo "Then run this script again."
    exit 1
fi

echo "== setting the remote =="
if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REMOTE"
else
    git remote add origin "$REMOTE"
fi

echo "== pushing =="
git push -u origin master

echo
echo "== done =="
echo "  ${REMOTE}"
echo
echo "Now set the description and topics on the GitHub page, and add a link"
echo "to the YouTube video in the README."

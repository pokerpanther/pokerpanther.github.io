#!/bin/bash
git config --global user.name 'github-actions[bot]'
git config --global user.email 'github-actions[bot]@users.noreply.github.com'

# Check for staged changes
git diff --cached --quiet
exit_code=$?


if [[ $exit_code -ne 0 ]]; then 
    git commit -m 'Update results data'
    git push https://x-access-token:${GITHUB_TOKEN}@github.com/pokerpanther/pokerpanther.github.io.git
else
    echo "No changes to commit."
fi

# git diff --cached --quiet returns 1 when there are staged changes  